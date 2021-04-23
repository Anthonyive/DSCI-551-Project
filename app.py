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

    return render_template('index.html', docCount=docCount, catCount=catCount)

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
        
    return jsonify(items=json.loads(data))

if __name__ == '__main__':
    app.run(debug=True)