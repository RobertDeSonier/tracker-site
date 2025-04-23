from mongoengine import Document, StringField, DateTimeField, ReferenceField, BooleanField, ObjectIdField
from werkzeug.security import generate_password_hash, check_password_hash

# Define the User model
class User(Document):
    id = ObjectIdField(primary_key=True)  # Explicitly define the id field as ObjectId
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    created_at = DateTimeField()
    password = StringField(required=True)
    is_active = BooleanField(default=True)  # Indicates if the user account is active

    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

# Define the Item model
class Item(Document):
    name = StringField(required=True)
    description = StringField()
    owner = ReferenceField(User)

# Define the Record model
class Record(Document):
    item = ReferenceField(Item)
    timestamp = DateTimeField()
    comment = StringField()
