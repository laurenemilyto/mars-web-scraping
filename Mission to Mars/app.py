# Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find a record from the mongo database
    mars_dict = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars_dict=mars_dict)

# Route to trigger the scrape function
@app.route("/scrape")
def scrape():

    print("beginning scraping")
    
    # Define collection
    mars = mongo.db.mars

    # Run scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)