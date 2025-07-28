from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FundType(db.Model):
    __tablename__ = 'fund_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(256))
    
    products = db.relationship('FundProduct', backref='type', lazy=True)

class FundManager(db.Model):
    __tablename__ = 'fund_managers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    bio = db.Column(db.Text)
    company = db.Column(db.String(128))
    experience_years = db.Column(db.Integer)
    
    products = db.relationship('FundProduct', backref='manager', lazy=True)

class FundProduct(db.Model):
    __tablename__ = 'fund_products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    code = db.Column(db.String(32), unique=True, nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('fund_types.id'), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('fund_managers.id'), nullable=False)
    inception_date = db.Column(db.Date)
    description = db.Column(db.Text) 