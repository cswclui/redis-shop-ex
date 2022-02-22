import redis
from pprint import pprint 

r = redis.StrictRedis(host="localhost", port=6379, charset="utf-8", decode_responses=True)

def most_popular_items(n):
    #todo

def last_item_purchased(n):
    #todo

def print_orders(n):    
    #todo

n=4
if __name__ == "__main__":
    print("=====most_popular_item=====")
    most_popular_items(n)
    print("\n=====last_item_purchased=====")
    last_item_purchased(n)
    print("\n=====print_orders=====")
    print_orders(n)

