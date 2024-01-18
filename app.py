from flask import Flask
from routes.routes import expenses
from models import db  

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(expenses)

db.init_app(app)

with app.app_context():
    #db.drop_all()
    db.create_all()

if __name__ == "__main__":
    app.run(port=5000, debug=True)
