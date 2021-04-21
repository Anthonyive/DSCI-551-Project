from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from bson.json_util import loads, dumps
import json
import re

from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
sc = SparkContext('local')
spark = SparkSession(sc)

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://DSCI551:Dsci551@cluster0.ydii8.mongodb.net/Walmart?retryWrites=true&w=majority"
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/livesearch', methods=["POST", "GET"])
def live_search():
    query = request.form.get("keyword")
    result = mongo.db.products.find( { "$text": {"$search": query} } ).limit(1000)
    
    data = dumps(result)
    print(len(data))

    default = False
    ninetySevenCentShipping = request.form.get("ninetySevenCentShipping", default)
    marketplace = request.form.get("marketplace", default)
    shipToStore = request.form.get("shipToStore", default)
    freeShipToStore = request.form.get("freeShipToStore", default)
    bundle = request.form.get("bundle", default)
    clearance = request.form.get("clearance", default)
    preOrder = request.form.get("preOrder", default)
    freeShippingOver35Dollars = request.form.get("freeShippingOver35Dollars", default)
    availableOnline = request.form.get("availableOnline", default)

    print(request.form)

    df = spark.read.json(sc.parallelize([data]))

    options = {"ninetySevenCentShipping": ninetySevenCentShipping,"marketplace": marketplace,"shipToStore": shipToStore,"freeShipToStore": freeShipToStore,"bundle": bundle,"clearance": clearance,"preOrder": preOrder,"freeShippingOver35Dollars": freeShippingOver35Dollars,"availableOnline": availableOnline}
    filterColumns = options.keys()
    columns = list(set(filterColumns) & set(df.columns))

    matches = df
    for c in columns:
        matches = matches.filter(matches[c] == options[c])

    filteredData = df.toJSON().map(lambda j: json.loads(j)).collect()

    return jsonify(items=filteredData)

if __name__ == '__main__':
    app.run(debug=True)