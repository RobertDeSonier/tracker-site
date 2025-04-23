from django.shortcuts import render
from django.http import JsonResponse
from mongoengine.queryset.visitor import Q
from .models import User, Item, Record
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib.auth import logout
import json
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging
from .auth_backend import MongoJWTAuthentication
from django.views.decorators.http import require_http_methods
from bson import ObjectId

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Create your views here.

@csrf_exempt
# View to handle User creation
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data
            created_at = datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%S')
            user = User(username=data['username'], email=data['email'], created_at=created_at)
            user.save()
            return JsonResponse({'message': 'User created successfully'})
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

@csrf_exempt
# View to handle Item creation
def create_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data
            owner = User.objects.get(username=data['owner'])
            item = Item(name=data['name'], description=data['description'], owner=owner)
            item.save()
            return JsonResponse({'message': 'Item created successfully'})
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

@csrf_exempt
# View to handle Record creation with comment
def create_record(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data
            timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M:%S')
            item = Item.objects.get(name=data['item'])
            comment = data.get('comment', '')
            record = Record(item=item, timestamp=timestamp, comment=comment)
            record.save()
            return JsonResponse({'message': 'Record created successfully'})
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

@csrf_exempt
# View to register a new user using mongoengine with hashed password
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data
            username = data['username']
            password = data['password']
            email = data['email']

            if User.objects(username=username).first():
                return JsonResponse({'error': 'Username already exists'}, status=400)

            user = User(username=username, email=email, created_at=datetime.now())
            user.set_password(password)
            user.save()
            return JsonResponse({'message': 'User registered successfully'})
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

@csrf_exempt
# View to log in a user using mongoengine with hashed password
def user_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data
            username = data['username']
            password = data['password']

            user = User.objects(username=username).first()
            if user and user.check_password(password):
                # Simulate a login by returning a success message
                return JsonResponse({'message': 'Login successful'})
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

@csrf_exempt
# View to log out a user
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logout successful'})

@csrf_exempt
# View to get user profile
def view_profile(request):
    if request.method == 'GET':
        try:
            logger.debug("Starting view_profile function")
            # Manually authenticate the user using the custom MongoJWTAuthentication
            jwt_authenticator = MongoJWTAuthentication()
            user, validated_token = jwt_authenticator.authenticate(request)
            if user:
                logger.debug(f"Authenticated user: {user.username}")
                logger.debug(f"Decoded token: {validated_token}")
                request.user = user
                username = user.username
                user_obj = User.objects(username=username).first()
                if user_obj:
                    logger.debug(f"User found: {user_obj.username}")
                    return JsonResponse({
                        'username': user_obj.username,
                        'email': user_obj.email,
                        'created_at': user_obj.created_at
                    })
                else:
                    logger.debug("User not found in database")
                    return JsonResponse({'error': 'User not found'}, status=404)
            else:
                logger.debug("User not authenticated")
                return JsonResponse({'error': 'User not authenticated'}, status=401)
        except Exception as e:
            logger.error(f"Error in view_profile: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
# View to update user profile
def update_profile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data
            username = data['username']
            email = data.get('email')

            user = User.objects(username=username).first()
            if user:
                if email:
                    user.email = email
                user.save()
                return JsonResponse({'message': 'Profile updated successfully'})
            else:
                return JsonResponse({'error': 'User not found'}, status=404)
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

@csrf_exempt
# View to list all items for a user
def list_items(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        user = User.objects(username=username).first()
        if user:
            items = Item.objects(owner=user)
            return JsonResponse({
                'items': [
                    {'id': str(item.id), 'name': item.name, 'description': item.description}
                    for item in items
                ]
            })
        else:
            return JsonResponse({'error': 'User not found'}, status=404)

@csrf_exempt
# View to update an item
def update_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data
            item_id = data['item_id']
            description = data.get('description')

            item = Item.objects(id=item_id).first()
            if item:
                if description:
                    item.description = description
                item.save()
                return JsonResponse({'message': 'Item updated successfully'})
            else:
                return JsonResponse({'error': 'Item not found'}, status=404)
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

@csrf_exempt
# View to delete an item
def delete_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data
            item_id = data['item_id']

            item = Item.objects(id=item_id).first()
            if item:
                item.delete()
                return JsonResponse({'message': 'Item deleted successfully'})
            else:
                return JsonResponse({'error': 'Item not found'}, status=404)
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

@csrf_exempt
# View to list all records for an item including comments
def list_records(request):
    if request.method == 'GET':
        item_id = request.GET.get('item_id')
        item = Item.objects(id=item_id).first()
        if item:
            records = Record.objects(item=item)
            return JsonResponse({
                'records': [
                    {'id': str(record.id), 'timestamp': record.timestamp, 'comment': record.comment}
                    for record in records
                ]
            })
        else:
            return JsonResponse({'error': 'Item not found'}, status=404)

@csrf_exempt
# View to update a record with comment
def update_record(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data
            record_id = data['record_id']
            timestamp = data.get('timestamp')
            comment = data.get('comment')

            record = Record.objects(id=record_id).first()
            if record:
                if timestamp:
                    record.timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')
                if comment is not None:
                    record.comment = comment
                record.save()
                return JsonResponse({'message': 'Record updated successfully'})
            else:
                return JsonResponse({'error': 'Record not found'}, status=404)
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

@csrf_exempt
# View to delete a record
def delete_record(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data
            record_id = data['record_id']

            record = Record.objects(id=record_id).first()
            if record:
                record.delete()
                return JsonResponse({'message': 'Record deleted successfully'})
            else:
                return JsonResponse({'error': 'Record not found'}, status=404)
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

# View to list and create tracking items
@csrf_exempt
@require_http_methods(["GET", "POST"])
def manage_items(request):
    try:
        jwt_authenticator = MongoJWTAuthentication()
        user, _ = jwt_authenticator.authenticate(request)
        if not user:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

        if request.method == 'GET':
            items = Item.objects(owner=user)
            items_list = [{'id': str(item.id), 'name': item.name, 'description': item.description} for item in items]
            return JsonResponse({'items': items_list})

        elif request.method == 'POST':
            data = json.loads(request.body)
            name = data.get('name')
            description = data.get('description', '')

            if not name:
                return JsonResponse({'error': 'Name is required'}, status=400)

            item = Item(name=name, description=description, owner=user)
            item.save()
            return JsonResponse({'message': 'Item created successfully', 'id': str(item.id)})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# View to update or delete a tracking item
@csrf_exempt
@require_http_methods(["PUT", "DELETE"])
def manage_item(request, item_id):
    try:
        jwt_authenticator = MongoJWTAuthentication()
        user, _ = jwt_authenticator.authenticate(request)
        if not user:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

        item = Item.objects(id=ObjectId(item_id), owner=user).first()
        if not item:
            return JsonResponse({'error': 'Item not found'}, status=404)

        if request.method == 'PUT':
            data = json.loads(request.body)
            item.name = data.get('name', item.name)
            item.description = data.get('description', item.description)
            item.save()
            return JsonResponse({'message': 'Item updated successfully'})

        elif request.method == 'DELETE':
            item.delete()
            return JsonResponse({'message': 'Item deleted successfully'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# View to handle records for a specific item
@csrf_exempt
@require_http_methods(["GET", "POST"])
def manage_records(request, item_id):
    try:
        jwt_authenticator = MongoJWTAuthentication()
        user, _ = jwt_authenticator.authenticate(request)
        if not user:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

        item = Item.objects(id=ObjectId(item_id), owner=user).first()
        if not item:
            return JsonResponse({'error': 'Item not found'}, status=404)

        if request.method == 'GET':
            records = Record.objects(item=item)
            records_list = [
                {'id': str(record.id), 'datetime': record.timestamp, 'comment': record.comment}
                for record in records
            ]
            return JsonResponse({'records': records_list})

        elif request.method == 'POST':
            data = json.loads(request.body)
            timestamp = datetime.strptime(data['datetime'], '%Y-%m-%dT%H:%M:%S')
            comment = data.get('comment', '')

            record = Record(item=item, timestamp=timestamp, comment=comment)
            record.save()
            return JsonResponse({'message': 'Record added successfully', 'id': str(record.id)})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
