import os
import uuid
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from flask import Flask, request
from flask_restx import Api, Resource, fields
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

env_path = "./src/.env"
load_dotenv(env_path)

MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD") or os.getenv("MONGO_PASSWORD")
MONGO_CLUSTER = os.environ.get("MONGO_CLUSTER") or os.getenv("MONGO_CLUSTER")

api = Api(app)
order_ns = api.namespace("api/v1/orders", "CRUD operations for Orders")

contact = api.model(
    "Contact",
    {
        "name": fields.String(required=True, description="Customer Name"),
        "emailId": fields.String(required=True, description="emailId of customer"),
        "phone": fields.String(required=True, description="Phone number of customer"),
        "address": fields.String(required=True, description="Address of customer")
    },
)

product = api.model(
    "Product",
    {
        "productName": fields.String(required=True, description="Product Name"),
        "productId": fields.String(required=True, description="Product's Unique ID"),
        "price": fields.Float(required=True, description="Product Price"),
        "tax": fields.Float(required=True, description="Product tax percentage"),
        "quantity" : fields.Integer(required=True,description="Item count")
    },
)

orderInsert = api.model(
    "orderInsert",
    {
        "orderItems": fields.List(fields.Nested(product)),
        "contact": fields.Nested(contact)
    },
)

order = api.model(
    "Order",
    {
        "id": fields.String(required=True, description="Product's system generated Id"),
        "orderId": fields.String(required=True, description="Order Id"),
        "orderItems": fields.List(fields.Nested(product)),
        "contact": fields.Nested(contact),
        "totalCost": fields.Float(required=True, description="Total cost of order"),
        "submittedAt" : fields.String(required=True, description="Time order is submitted"),
    },
)

@order_ns.route("/submitOrder")
class Orders(Resource):
    @order_ns.doc(
        "Create Product",
        reponses={200: "Success", 409: "Key alreay exists", 500: "Unexpected Error"},
    )
    @order_ns.expect(orderInsert, validate=True)
    @order_ns.marshal_with(order)
    def post(self):
        db = client["db_om"]
        collection = db["orders"]
        
        data = request.json
        data["id"] = uuid.uuid4().__str__()
        data["submittedAt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        orderId = uuid.uuid4().__str__()
        orderId = "AUTO-"+str(orderId)
        data["orderId"] = orderId
        totalCost = 0
        for cost in data["orderItems"]:
            totalCost += (cost["price"] * cost["quantity"]) + (cost["price"] * (cost["tax"])/100) * cost["quantity"]
        data["totalCost"] = totalCost            
        collection.insert_one(data)
        # SENDS EMAIL AFTER ORDER CREATED
        requestData={}
        requestData["orderId"] = data["orderId"]
        requestData["name"] = data["contact"]["name"]
        requestData["mailId"] = data["contact"]["emailId"]
        requestData["totalCost"] = data["totalCost"]

        # http://127.0.0.1:5004/api/v1/email/sendMail
        url = "http://" + os.getenv("NG_BASEURL") + ":" + os.getenv("NG_PORT") + os.getenv("NG_URL")
        response = requests.post(url, json=requestData)
        return data, 200

@order_ns.route("/<orderId>")
class ProductId(Resource):
    @order_ns.doc(
        "Get Profile",
        reponses={200: "Document Found", 404: "Document Not Found", 500: "Unexpected Error"},
    )
    def get(self, orderId):
        try:
            db = client["db_om"]
            collection = db["orders"]
            
            order_body = {}
            order = collection.find_one({'id': orderId})

            order_body["orderItems"] = order["orderItems"]
            order_body["contact"] = order["contact"]
            order_body["orderId"] = orderId
            order["submittedAt"] = order["submittedAt"]
            order_body["totalCost"] = order["totalCost"]

            return order_body, 200
        except Exception as e:
            return f"Unexpected error: {e}", 500

# Create a new client and connect to the server
uri = f"mongodb+srv://admin:{MONGO_PASSWORD}@{MONGO_CLUSTER}/?retryWrites=true&w=majority"
client = MongoClient(uri)
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

if __name__ == "__main__":
    app.run(port=5003, host="0.0.0.0", debug=True)
