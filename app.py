from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from bson.json_util import loads, dumps

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://DSCI551:Dsci551@cluster0.ydii8.mongodb.net/Walmart?retryWrites=true&w=majority"
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/livesearch', methods=["POST", "GET"])
def livesearch():
    query = request.form.get("query")
    result = mongo.db.taxonomy.find()
    return jsonify(dumps(result))

if __name__ == '__main__':
    app.run(debug=True)