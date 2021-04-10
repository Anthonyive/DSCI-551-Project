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
    return render_template('index.html')

@app.route('/livesearch', methods=["POST", "GET"])
def live_search():
    query = request.form.get("keyword")
    kind = request.form.get("kind")
    print(query, kind)
    if kind == 'products':
        result = mongo.db.products.find( { "$text": {"$search": query} } ).limit(5)
    else:
        result = mongo.db.products.find( { "$text": {"$search": query} } ).limit(5)
    
    data = dumps(result)
    print(type(data))
    return jsonify(items=json.loads(data))

if __name__ == '__main__':
    app.run(debug=True)