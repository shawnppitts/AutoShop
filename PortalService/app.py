import os
import json
from dotenv import load_dotenv
import requests
from flask import Flask, request, jsonify,render_template
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

env_path = "./src/.env"
load_dotenv(env_path)

PM_BASEURL = os.getenv("PM_BASEURL")
PM_PORT = os.getenv("PM_PORT")
PM_GETPRODUCT_URL = os.getenv("PM_GETPRODUCT_URL")
OM_BASEURL = os.getenv("OM_BASEURL")
OM_PORT = os.getenv("OM_PORT")
OM_SUBMITORDER_URL = os.getenv("OM_SUBMITORDER_URL")
OM_GETORDER_URL = os.getenv("OM_GETORDER_URL")

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')
 
@app.route('/order',methods=['GET','POST'])
def order():
    url = f"http://{PM_BASEURL}:{PM_PORT}{PM_GETPRODUCT_URL}"
    response = requests.get(url).json()

    product_count = len(response)    
    # POST request to submit order
    if request.method == 'POST':
        data={}
        orderItems = []
        contact = {}
        for item in response:
            orderItem ={}
            if int(request.form[item['productId']]):
                orderItem["quantity"] = int(request.form[item['productId']])           
                orderItem["productName"] = item["productName"]
                orderItem["price"] = item["price"]
                orderItem["productId"] = item["productId"]
                orderItem["tax"] = item["tax"]
                orderItems.append(orderItem)

        contact["name"] = request.form["name"]
        contact["address"] = request.form["address"]
        contact["emailId"] = request.form["email"]
        contact["phone"] = request.form["mobile"]

        data["orderItems"] = orderItems
        data["contact"] = contact


        url = f"http://{OM_BASEURL}:{OM_PORT}{OM_SUBMITORDER_URL}"

        response = requests.post(url, json=data)
        json_response = response.json()

        # POST passes details
        return render_template('orderView.html', data=response.json())
    # GET /orders loads products
    return render_template('order.html', data=response)

@app.route('/viewOrder',methods=['GET','POST'])
def viewOrder():
    if request.method == 'POST':
        orderId = request.form['orderId']        
        url = "http://{OM_BASEURL}:{OM_PORT}{OM_GETORDER_URL}{orderId}"
        
        try:
            response = requests.get(url).json()
            return render_template('orderView.html',data=response)
        except:
            return render_template('home.html')
    return render_template('view.html')

if __name__ == "__main__":

    # controller = PushController(meter, collector_exporter, 10000)
    app.run(port=5001, host="0.0.0.0", debug=True)
