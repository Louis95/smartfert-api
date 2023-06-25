
from ...config import db, flask_bcrypt


class User(db.Model):
    """
    User Model for storing user related details.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    farms = db.relationship('FarmModel', backref='users', lazy=True)
    password_hash = db.Column(db.String(100), nullable=False)

    @property
    def password(self):
        """
        Raise AttributeError when attempting to read the password attribute directly.

        This is a write-only field and should not be read directly.
        """
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        """
        Set the password attribute.

        This method sets the password hash based on the provided password.
        It uses the flask_bcrypt library to generate the password hash.

        Args:
            password (str): The password to be set.

        Returns:
            None
        """
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """
        Check if the provided password matches the user's password hash.

        This method verifies if the provided password matches the password hash
        stored in the user's password_hash attribute.

        Args:
            password (str): The password to be checked.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        """
        Return a string representation of the User object.

        Returns:
            str: A string representation of the User object.
        """
        return "<User '{}'>".format(self.username)
