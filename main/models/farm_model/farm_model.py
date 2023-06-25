from ...config import db
import uuid


class FarmModel(db.Model):
    """Farm model"""
    __tablename__ = "farms"

    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fertilizers = db.relationship('FertilizerModel', backref='farms', lazy=True)
