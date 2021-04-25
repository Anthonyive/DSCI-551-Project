from flask import Flask, render_template, request, jsonify, Blueprint
from flask_pymongo import PyMongo
from bson.json_util import loads, dumps
import json, re, ast

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://DSCI551:Dsci551@cluster0.ydii8.mongodb.net/Walmart?retryWrites=true&w=majority"
mongo = PyMongo(app)

@app.route('/')
def index():
    docCount = mongo.db.products.count()
    catCount = mongo.db.products.aggregate([
                        {
                            '$group': {'_id': "$categoryNode"}
                        },
                        {
                            '$group': {
                                '_id': 1, 
                                'count': {'$sum' : 1 }
                            }
                        }])
    catCount = [i.get('count') for i in catCount][0]

    avgReviewCount = mongo.db.products.aggregate([
        {"$group": {"_id": None, "reviewAvg": {"$avg": "$numReviews"}}}
    ])

    avgReviewCount = list(avgReviewCount)[0]['reviewAvg']
    avgReviewCount = round(avgReviewCount, 1)

    # filter items count
    filterItems = ["ninetySevenCentShipping", "marketplace", "shipToStore", "bundle", "clearance", "freeShippingOver35Dollars"]
    filterItemsHRNames = ["97&#162; Shipping", "Marketplace", "Ship to store", "Bundle", "Clearance", "Free Shipping over 35 dollars"]
    filterItemsIndexCounts = dict()
    for item in filterItems:
        result = mongo.db.products.aggregate(
            [
                { "$match": {item: True}},
                { "$count": item }
            ]
        )
        pyResult = next(iter(list(result)), {item: 0})
        
        filterItemsIndexCounts[item] = pyResult[item]
        # filterItemsCounts[item] = dict(result)['c']
    
    for k,v in filterItemsIndexCounts.items():
        filterItemsIndexCounts[k] = str(v)

    return render_template('index.html', docCount=docCount, catCount=catCount, avgReviewCount=avgReviewCount, filterItemsIndexCounts=filterItemsIndexCounts, filterItemsHRNames=filterItemsHRNames)

@app.route('/search', methods=["POST", "GET"])
def search(filter=False):
    query = request.form.get("keyword")
    filterCheckboxes = request.form.get('filterCheckboxes')
    filterCheckboxes = ast.literal_eval(filterCheckboxes)
    print(filterCheckboxes)
    result = mongo.db.products.aggregate(
        [ 
            { "$match": { "$text": {"$search": query} }},
            { "$sort": { "score": { "$meta": "textScore" } } },
            { "$match": dict.fromkeys(filterCheckboxes, {"$eq": True})},
            { "$limit": 200}
        ]
    )
    print(dict.fromkeys(filterCheckboxes, {"$eq": True}))
    data = dumps(result)

    # filter items count
    filterItems = ["ninetySevenCentShipping", "marketplace", "shipToStore", "bundle", "clearance", "freeShippingOver35Dollars"]
    filterItemsCounts = {'filterItemsCounts': dict()}
    for item in filterItems:
        result = mongo.db.products.aggregate(
            [ 
                { "$match": { "$text": {"$search": query} }},
                { "$match": {item: True}},
                { "$count": item }
            ]
        )
        pyResult = next(iter(list(result)), {item: 0})
        
        filterItemsCounts['filterItemsCounts'][item] = pyResult[item]
        # filterItemsCounts[item] = dict(result)['c']
    
    for k,v in filterItemsCounts['filterItemsCounts'].items():
        filterItemsCounts[k] = str(v)
    print(filterItemsCounts)
    print(type(json.loads(data)))
        
    return jsonify(items=json.loads(data), filterItemsCounts=filterItemsCounts)

if __name__ == '__main__':
    app.run(debug=True)