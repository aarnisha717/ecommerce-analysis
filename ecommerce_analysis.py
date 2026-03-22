import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine("mysql+mysqlconnector://root:Arnisha2005@localhost/ecommerce")

orders=pd.read_csv("olist_orders_dataset.csv")
orders.to_sql('orders',con = engine,if_exists = "replace",index = False)

customers=pd.read_csv("olist_customers_dataset.csv")
customers.to_sql('customers',con = engine,if_exists = "replace",index = False)

ot=pd.read_csv("olist_order_items_dataset.csv")
ot.to_sql('ot',con = engine,if_exists = "replace",index = False)


print(orders.columns)
print(orders.isnull().sum())
print()

print(customers.columns)
print(customers.isnull().sum())
print()

print(ot.columns)
print(ot.isnull().sum())
print()

print(orders['order_status'].value_counts())
print()


orders['is_delivered']=orders['order_delivered_customer_date'].notnull()
print(orders['is_delivered'].value_counts())
print()

merged = pd.merge(orders,customers,on="customer_id",how="inner")
print(merged.head())
print()

top_cities =merged['customer_city'].value_counts().head(10)
print(top_cities)

top_cities.plot(kind='bar',color='skyblue')
plt.title('TOP 10 CITIES BY ORDERS')
plt.xlabel('City')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("chart/top 10 cities by orders_chart.png")
plt.show()



top_states= merged['customer_state'].value_counts().head(10)

top_states.plot(kind='bar',color='purple')
plt.title('TOP 10 STATES BY ORDERS')
plt.xlabel('States')
plt.ylabel('Number of Orders')
plt.xticks(rotation=0)
plt.savefig("chart/top 10 states by orders_chart.png")
plt.show()

print()
full_data = pd.merge(merged,ot,on = 'order_id', how='inner')
print(full_data['price'].sum())
print()

full_data['order_purchase_timestamp']= pd.to_datetime(full_data['order_purchase_timestamp'])
full_data['month'] = full_data['order_purchase_timestamp'].dt.to_period('M')
monthly_sales = full_data.groupby('month')['price'].sum()

monthly_sales.plot(kind='line',color='green',linewidth=3)
plt.title('MONTHLY SALES TREND')
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.xticks(rotation=45)
plt.savefig("chart/monthly sales trend_chart.png")
plt.show()

products = pd.read_csv("olist_products_dataset.csv")

full_data = pd.merge(full_data,products,on = 'product_id',how='inner')

top_category = full_data['product_category_name'].value_counts().head(10)

top_category.plot(kind='bar',color='blue')
plt.title('TOP 10 PRODUCT CATEGORIES')
plt.xlabel('Category')
plt.ylabel('Count')
plt.xticks(rotation = 45)
plt.savefig("chart/top 10 product categories_chart.png")
plt.show()


orders['is_delivered']= orders['is_delivered'].map({True:"Delivered",False:"Not Delivered"})
orders['is_delivered'].value_counts().plot(kind='bar',color='gold')
plt.title("ORDER DELIVERY STATUS DISTRIBUTION")
plt.xlabel('Order Status')
plt.ylabel('Number of Orders')
plt.xticks(rotation=0)
plt.savefig("chart/order delivery status distribution_chart.png")
plt.show()







