from main.models.user_model.user import User
from ..config import db


def save_changes(data: User) -> None:
    """Helper function to store new user."""
    db.session.add(data)
    db.session.commit()
