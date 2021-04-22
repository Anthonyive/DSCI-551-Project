from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from bson.json_util import loads, dumps
import json
import re

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

@app.route('/livesearch', methods=["POST", "GET"])
def live_search():
    query = request.form.get("keyword")
    result = mongo.db.products.find( { "$text": {"$search": query} } ).limit(100)
    data = dumps(result)
    return jsonify(items=json.loads(data))

if __name__ == '__main__':
    app.run(debug=True)