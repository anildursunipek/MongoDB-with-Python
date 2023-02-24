# Mongo is a document-oriented database.
# No sql or not only sql database.
# Data store in collections of documents (looks like JSON file but mongoDB use BSON(binary json file)).
# BSON file support more data type .
# Windows MongoDB Comunity Server İnstallation Guide -> https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/
# pip install pymongo -> this is mongoDB driver
# PyMongo is a Python distribution containing tools for working with MongoDB, and is the recommended way to work with MongoDB from Python.
# dnspython -> if you use cloued version you have to install dnspython otherwise you will get error.

from pymongo import MongoClient
import datetime

cluster = "mongodb://localhost:27017" # conntection string
client = MongoClient(cluster)

print(client.list_database_names()) 
# ['admin', 'config', 'local', 'test']

db = client.test # or client["test"] -> both of them usable 
print(db.list_collection_names())
# ['todos']
# collection rename command -> db.collectionname.renameCollection("newCollectionName") -> mongodbsh command 

todos = db.todos # collection

# Insert one item
todo_item_1 = {
    "name": "Mike",
    "text": "Mike's todo list",
    "status": "open",
    "tags": ["python", "coding"],
    "date": datetime.datetime.now()
}

#result = todos.insert_one(todo_item_1)

# Insert many item
todo_items = [{
    "name": "Kevin",
    "text": "Kevin's todo list",
    "status": "open",
    "tags": ["java", "gym"],
    "date": datetime.datetime.now()
    },
    {
    "name": "Paul",
    "text": "Paul's todo list",
    "status": "open",
    "tags": ["cpp", "coding"],
    "date": datetime.datetime.now()
    }]

#result = todos.insert_many(todo_items)

# MongoDB Query
result = todos.find_one({"name":"Kevin"}) 
print(result)
#{'_id': ObjectId('63f88ce526ca84d22d10763c'), 'name': 'Kevin', 'test': "Kevin's todo list", 'status': 'open', 'tagas': ['java', 'gym'], 'date': datetime.datetime(2023, 2, 24, 13, 9, 41, 527000)}  

result = todos.find_one({"tags":"cpp"})
print(result)
#{'_id': ObjectId('63f88ce526ca84d22d10763d'), 'name': 'Paul', 'test': "Paul's todo list", 'status': 'open', 'date': datetime.datetime(2023, 2, 24, 13, 9, 41, 527000), 'tags': ['cpp', 'coding']}

result = todos.find_one({"name":"Paul", "text":"Paul's todo list"})
print(result)
# {'_id': ObjectId('63f88ce526ca84d22d10763d'), 'name': 'Paul', 'status': 'open', 'date': datetime.datetime(2023, 2, 24, 13, 9, 41, 527000), 'tags': ['cpp', 'coding'], 'text': "Paul's todo list"}   

print("Total number of documents: ", todos.count_documents({}))
print("Number of documents with the name Mike: ", todos.count_documents({"name":"Mike"}))

result = todos.find_one({"_id":"63f88ba8db8c3e3710bb526f"})
print(result) # returned None because data type of _id is not string. it is ObjectId we can import this data type

from bson.objectid import ObjectId
result = todos.find_one({"_id":ObjectId("63f88ba8db8c3e3710bb526f")})
print(result)

# Add more data 
todo_items_2 = [{
    "name": "Kevin",
    "text": "Kevin's todo list",
    "status": "open",
    "tags": ["java", "gym"],
    "date": datetime.datetime.now()
    },
    {
    "name": "Paul",
    "text": "Paul's todo list",
    "status": "open",
    "tags": ["cpp", "coding"],
    },
    {
    "name": "Kevin",
    "text": "Kevin's todo list V2",
    "tags": ["javascript", "new blog post"],
    "date": datetime.datetime.now()
    },
    {
    "name": "Thomas",
    "text": "Thomas's todo list",
    "date": datetime.datetime.now()
    },
    {
    "name": "Micheal",
    "date": datetime.datetime.now()
    },
]

#result = todos.insert_many(todo_items_2)

result = todos.find({"name":"Kevin"})
print(result) # İterable object
for object in result:
    print(object)


# Added more document 
"""
    result = todos.insert_many([
    {"name":"Alex",
     "date":datetime.datetime(2022,1,1)
    },
    {
    "name":"Andrea",
    "date": datetime.datetime(2022,1,2)
    }
    ])
"""
# Comparison Query Selectors
"""
$eq(==): Matches values that are equal to a specified value.
$gt(>): Matches values that are greater than a specified value.
$gte(>=): Matches values that are greater than or equal to a specified value.
$in: Matches any of the values specified in an array.
$lt(<): Matches values that are less than a specified value.
$lte(<=): Matches values that are less than or equal to a specified value.
$ne(!=): Matches all values that are not equal to a specified value.
$nin: Matches none of the values specified in an array.
"""

# $lt: less then
print("$lt Query Selector")
dt = datetime.datetime(2023,1,1)
result = todos.find({"date": {"$lt": dt}})
for document in result:
    print("$lt apply ", document)

# $gt: greater then
print("$gt Query Selector")
result = todos.find({"date": {"$gt":dt}})
for document in result:
    print("$gt apply ", document)

# Delete
#result = todos.delete_one({"_id": ObjectId("63f8931838711bf3746675e1")})
print("Deleted object -> ", result)

# Update Operators
"""
$currentDate: Sets the value of a field to current date, either as a Date or a Timestamp.
$inc: Increments the value of the field by the specified amount.
$min: Only updates the field if the specified value is less than the existing field value.
$max: Only updates the field if the specified value is greater than the existing field value.
$mul: Multiplies the value of the field by the specified amount.
$rename: Renames a field.
$set: Sets the value of a field in a document.
$setOnInsert: Sets the value of a field if an update results in an insert of a document. Has no effect on update operations that modify existing documents.
$unset: Removes the specified field from a document.
"""

print(todos.find_one({"name":"Thomas"}))
# Before update: {'_id': ObjectId('63f8931838711bf3746675e3'), 'name': 'Thomas', 'text': "Thomas's todo list", 'date': datetime.datetime(2023, 2, 24, 13, 36, 8, 626000)}
# Added status
# todos.update_one({"name":"Thomas"}, {"$set":{"status":"new"}})
print(todos.find_one({"name":"Thomas"}))
# After update: {'_id': ObjectId('63f8931838711bf3746675e3'), 'name': 'Thomas', 'text': "Thomas's todo list", 'date': datetime.datetime(2023, 2, 24, 13, 36, 8, 626000), 'status': 'new'}

# Remove specific field
todos.update_one({"name":"Thomas"}, {"$unset": {"status": None}})
print(todos.find_one({"name":"Thomas"})) # Deleted status field

