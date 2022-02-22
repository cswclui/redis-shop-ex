import json,redis,time
from pprint import pprint 
from datetime import datetime

f = open("./data/orders.json", mode="r", encoding="utf-8")
f2 = open("./data/products.json", mode="r", encoding="utf-8")
f3 = open("./data/users.json", mode="r", encoding="utf-8")
orders = json.loads(f.read())
product_list = json.loads(f2.read())
user_list = json.loads(f3.read())

#convert the product list to python dictionary
catalog={}
for i in product_list:
    product_id=i['id']
    catalog[product_id]={}
    catalog[product_id]["price"]=float(i['price'])
    catalog[product_id]["title"]=i['title']

#convert the user list to python dictionary
users={}
for i in user_list:
    user_id=i['id']
    users[user_id]={}
    users[user_id]['username']=i['username']

r = redis.Redis(host='localhost', port=6379)
r.flushall() #clear all keys in Redis

def process_order():
    for i in orders: #for each order
        date_time_str =i["date"]
        userId=i["userId"]
       
        userName=users[userId]['username']
        orderId=i["id"]
        products=i["products"]
        
        dt=datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        order_date = dt.strftime('%Y-%m-%d')
        order_hour = dt.strftime('%H')
        
        #update order count and set keys' expiry time
        r.incr("orders:"+order_date)
        
        orderRevenue = 0
        for j in products: #for each product in the order
            productID=j["productId"]
            quantity=int(j["quantity"])
            productPrice=catalog[productID]['price']
            productTitle=catalog[productID]['title']
            
            #update popular items 
            r.zincrby("orders:items:id:popular", quantity, productID) 
            r.zincrby("orders:items:title:popular", quantity, productTitle) 
            
            #update unique count of items sold on the day
            r.sadd( "orders:items:"+order_date, productID)
            
            #add the latest products purchased
            r.lpush("orders:items:id:latest", productID)
            r.ltrim("orders:items:id:latest", 0, 10)
            
            r.lpush("orders:items:title:latest", productTitle)
            r.ltrim("orders:items:title:latest", 0, 10)
            
            #update orderRevenue
            orderRevenue += quantity * productPrice
        
        #update sales volume per day
        r.zincrby("sales:revenue:days",orderRevenue, order_date)

        #update sales volume per hour
        r.hincrbyfloat("sales:revenue:"+order_date, order_hour, orderRevenue)

        #update sales volume per user
        r.zincrby("sales:revenue:userid",orderRevenue, userId)
        r.zincrby( "sales:revenue:username",orderRevenue, userName)

process_order()

