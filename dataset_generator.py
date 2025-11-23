import pandas as pd 
import random
from datetime import datetime, timedelta

def generate_orders(n=1000):
    categories=["electronics","fashion","home","beauty","sports"]
    cities=["Ankara","Istanbul","Izmir","Bursa","Antalya"]
    payments=["credit_card","eft","cash_on_delivery"]
    data=[]
    for i in range(n):
        order={
            "order_id":i+1,
            "customer_id":random.randint(1,300),
            "order_date":datetime(2023,1,1)+timedelta(days=random.randint(0,900)),
            "price":random.randint(50,150),
            "quantity":random.randint(1,5),
            "category":random.choice(categories),
            "city":random.choice(cities),
            "payment_method":random.choice(payments)
        }
        data.append(order)
    df=pd.DataFrame(data)
    df.to_csv("orders.csv",index=False)
    print("orders.csv başarıyla oluşturuldu")
generate_orders()