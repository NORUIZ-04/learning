from flask import Flask
from flask_sqlalchemy import SQLAlchemy  #ORM 

app = Flask(__name__)

#creating data base
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///travel.db"
db = SQLAlchemy(app)

#created the model for the database
class Destination(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  Destination = db.Column(db.String(50), nullable=False)
  country = db.Column(db.String(25), nullable=False)
  rating = db.Column(db.Float , nullable=False)

  #creating a method inside the class to covert the data into dict format  which wwill be helpfull for us to handle the json formation 
  def to_dict(self):
    return{
      "id": self.id,
      "destination":self.Destination,
      "country": self.country,
      "rating": self.rating
    }

#context manager
with app.app_context():
  db.create_all()

#create routes

@app.route ("/") #the slash will used for home route
def home():
  return  "hello"



if __name__=="__main__":   #this make our api run alawyas constantly (so constant referhsing)
  app.run(debug=True)