from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

db = SQLAlchemy()

@dataclass
class Expense(db.Model):    
    __tablename__ = 'Expenses'

    id: int = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=80), nullable=False)
    description: str = db.Column(db.String(255), nullable=False)
    amount: float =  db.Column(db.Float, nullable=False)
    date: date = db.Column(db.Date, nullable=False, default=date.today)

    def __repr__(self):
        return f"<Expense(id={self.id}, description={self.description}, amount={self.amount}, date={self.date})>"
    
    def as_dict(self):
        return {    
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "amount": self.amount,
            "date": str(self.date) 
        }