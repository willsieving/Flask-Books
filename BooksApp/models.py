from BooksApp import db
from datetime import datetime


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    image_file = db.Column(db.String)
    author = db.Column(db.String, nullable=False)
    link = db.Column(db.String)
    def __repr__(self):
        return f"Post('{self.title}', '{self.rating}')"

