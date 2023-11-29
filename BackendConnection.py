# app.py
import traceback

import pymongo
from flask import Flask, render_template, jsonify
from pymongo import MongoClient

from flask_cors import CORS  # Import the CORS module

app = Flask(__name__, static_url_path='/templates', static_folder='templates')
CORS(app)  # Enable CORS for all routes in your Flask app


def connectDataBase():
    try:
        client = pymongo.MongoClient(host="localhost", port=27017)
        # database connection is localhost client.[databaseName]
        db = client.CatDB
        print(f"DB : CONNECTED")
        return db
    except Exception as error:
        traceback.print_exc()
        print("Database not connected successfully.. rawr")


# connection to database
datab = connectDataBase()
collection = datab.OrganizedCatWords


@app.route('/')
def index():
    return render_template('catPage.html')  # Render catPage.html


@app.route('/api/data')
def get_data():
    try:
        all_data_cursor = collection.find({}, {'_id': 0})

        fetched_data = list(all_data_cursor)

        print('Fetched Data:', fetched_data)

        return jsonify(fetched_data)
    except Exception as error:
        # Print the error to the console
        print("Mongo DB Error:", str(error))

        # Return an error response with a more detailed error message
        return jsonify({'error': f'Failed to retrieve data from MongoDB. {str(error)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
