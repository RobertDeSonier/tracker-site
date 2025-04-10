# Description:

 - I want to build a website where you can keep track of different things.
    - The website should have a react frontend, python with Django backend, and a mongoDb
 - It will support User authentication and profiles
 - Users will be able to create new tracking items
 - Once a tracking item is created, the user will be able to add data to the item to be tracked

# Data:

 - Users:
    - id
    - username
    - password
    - email
 - Items:
    - id
    - userId
    - description
 - Records:
    - id
    - itemId
    - datetime
    - comment