from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Define the route for the HTML page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# Set up scraping route - button to scrape updated data when we tell it to
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars #create new variable to point to Mongo db
   mars_data = scraping.scrape_all() #use scraping.py script
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302) #add a redirect after successfully scraping data so can see updated content

# Tell Flask to run
if __name__ == "__main__":
   app.run(debug=True)