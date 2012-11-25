from flask.ext.login import UserMixin
import auth
import db


class User(UserMixin):
    """This represents a user in our system."""

    def __init__(self, email=None, password=None, id=None):
        """Constructor. If id is provided, the user is loaded from the db."""
        if id:
            self.id = id
            self.load()
        else:
            self.id = None
        self.email = email
        if password:
            self.password = auth.encode_password(password)
        else:
            self.password = None

    def __repr__(self):
        return '<User: %r>' % self.email

    def check_password(self, password):
        return auth.check_password(password, self.password)

    def load(self):
        """Load the user denoted by self.id"""
        cur_doc = db.load_user(self.id)
        self.email = cur_doc['email']
        self.password = cur_doc['password']

    def load_by_email(self, email=None):
        """Load the user denoted by self.email"""
        if email:
            self.email = email
        cur_doc = db.load_user_by_email(self.email)
        if cur_doc:
            self.id = cur_doc['_id']
            self.password = cur_doc['password']
            return True
        else:
            return False

    def save(self):
        """Save the user to the database (or create if it is not present)"""
        if self.id:
            db.save_user(self.id, self.email, self.password)
        else:
            self.id = db.create_user(self.email, self.password)

    @staticmethod
    def check_existence_by_email(email):
        cur_doc = db.load_user_by_email(email)
        return cur_doc != None
