from django.shortcuts import render
from django.http import JsonResponse
from mongoengine.queryset.visitor import Q
from .models import User, Item, Record
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib.auth import logout

# Create your views here.

@csrf_exempt
# View to handle User creation
def create_user(request):
    if request.method == 'POST':
        data = request.POST
        created_at = datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%S')
        user = User(username=data['username'], email=data['email'], created_at=created_at)
        user.save()
        return JsonResponse({'message': 'User created successfully'})

@csrf_exempt
# View to handle Item creation
def create_item(request):
    if request.method == 'POST':
        data = request.POST
        owner = User.objects.get(username=data['owner'])
        item = Item(name=data['name'], description=data['description'], owner=owner)
        item.save()
        return JsonResponse({'message': 'Item created successfully'})

@csrf_exempt
# View to handle Record creation with comment
def create_record(request):
    if request.method == 'POST':
        data = request.POST
        timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M:%S')
        item = Item.objects.get(name=data['item'])
        comment = data.get('comment', '')
        record = Record(item=item, action=data['action'], timestamp=timestamp, comment=comment)
        record.save()
        return JsonResponse({'message': 'Record created successfully'})

@csrf_exempt
# View to register a new user using mongoengine with hashed password
def register(request):
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']
        email = data['email']

        if User.objects(username=username).first():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        user = User(username=username, email=email, created_at=datetime.now())
        user.set_password(password)
        user.save()
        return JsonResponse({'message': 'User registered successfully'})

@csrf_exempt
# View to log in a user using mongoengine with hashed password
def user_login(request):
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']

        user = User.objects(username=username).first()
        if user and user.check_password(password):
            # Simulate a login by returning a success message
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

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
        username = request.GET.get('username')
        user = User.objects(username=username).first()
        if user:
            return JsonResponse({
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at
            })
        else:
            return JsonResponse({'error': 'User not found'}, status=404)

@csrf_exempt
# View to update user profile
def update_profile(request):
    if request.method == 'POST':
        data = request.POST
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
        data = request.POST
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

@csrf_exempt
# View to delete an item
def delete_item(request):
    if request.method == 'POST':
        data = request.POST
        item_id = data['item_id']

        item = Item.objects(id=item_id).first()
        if item:
            item.delete()
            return JsonResponse({'message': 'Item deleted successfully'})
        else:
            return JsonResponse({'error': 'Item not found'}, status=404)

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
                    {'id': str(record.id), 'action': record.action, 'timestamp': record.timestamp, 'comment': record.comment}
                    for record in records
                ]
            })
        else:
            return JsonResponse({'error': 'Item not found'}, status=404)

@csrf_exempt
# View to update a record with comment
def update_record(request):
    if request.method == 'POST':
        data = request.POST
        record_id = data['record_id']
        action = data.get('action')
        timestamp = data.get('timestamp')
        comment = data.get('comment')

        record = Record.objects(id=record_id).first()
        if record:
            if action:
                record.action = action
            if timestamp:
                record.timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')
            if comment is not None:
                record.comment = comment
            record.save()
            return JsonResponse({'message': 'Record updated successfully'})
        else:
            return JsonResponse({'error': 'Record not found'}, status=404)

@csrf_exempt
# View to delete a record
def delete_record(request):
    if request.method == 'POST':
        data = request.POST
        record_id = data['record_id']

        record = Record.objects(id=record_id).first()
        if record:
            record.delete()
            return JsonResponse({'message': 'Record deleted successfully'})
        else:
            return JsonResponse({'error': 'Record not found'}, status=404)
