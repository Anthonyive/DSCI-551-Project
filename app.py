from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://DSCI551:Dsci551@cluster0.ydii8.mongodb.net/Walmart?retryWrites=true&w=majority"

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)