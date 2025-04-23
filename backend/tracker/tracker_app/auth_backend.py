from mongoengine import DoesNotExist
from tracker_app.models import User
from django.contrib.auth.backends import BaseBackend
from bson import ObjectId
from rest_framework_simplejwt.authentication import JWTAuthentication

class MongoEngineBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            if ObjectId.is_valid(user_id):
                return User.objects.get(id=ObjectId(user_id))
            return None
        except DoesNotExist:
            return None

class MongoJWTAuthentication(JWTAuthentication):
    user_id_claim = 'user_id'  # Define the claim name for the user ID
    check_user_is_active = True  # Enable the check for the `is_active` field

    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[self.user_id_claim]
        except KeyError:
            raise InvalidToken("Token contained no recognizable user identification")

        try:
            if ObjectId.is_valid(user_id):
                user = User.objects.get(id=ObjectId(user_id))
            else:
                raise InvalidToken("Invalid user ID format")
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found", code="user_not_found")

        if self.check_user_is_active and not user.is_active:
            raise AuthenticationFailed("User is inactive", code="user_inactive")

        return user