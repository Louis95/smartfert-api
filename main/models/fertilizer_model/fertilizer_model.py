from flask_sqlalchemy import SQLAlchemy

from ...config import db
from geoalchemy2 import Geometry


class FertilizerModel(db.Model):
    """Fertilizer model"""
    __tablename__ = "fertilizers"
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(Geometry('POINT'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    nit = db.Column(db.Float, nullable=False)
    farm_id = db.Column(db.String, db.ForeignKey('farms.id'), nullable=False)
