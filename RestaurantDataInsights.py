#Importing Necessary Libraries

#Pandas for loading, cleaning and manipulating data
#Numpy for simple analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#Pytz to convert date into nepali time
import pytz
#Loading the dataset
restaurantData = pd.read_csv('RestaurantData.csv')

#Checking the dataset using sample
#Add to_string() to have a view of all the column in pycharms terminal
print(restaurantData.sample(10).to_string())

#Checking the column
print(restaurantData.columns)
#data contains createdAt which is the order date lets check if the datatypes are as per needed

#Checking the datatype of column
print(restaurantData.dtypes)

#All other datatype are fine, howver the createdAt should be in datetime
#Before change i'll check if data contains null items
print(restaurantData.isna().sum())
#Data is clean with no null values so no need to do more

#Changing the createAt column to date time, this column is important for time series analysis
restaurantData['createdAt'] = pd.to_datetime(restaurantData['createdAt'])
#Getting nepal time zone
nepal_tz = pytz.timezone('Asia/Kathmandu')
restaurantData['createdAtNepal'] = restaurantData['createdAt'].dt.tz_convert(nepal_tz)

#Rechecking the datatypes
print(restaurantData.dtypes)

#Data Cleaning
#checking for duplicate
print(restaurantData.duplicated().sum())
#dropping duplicates, inplace = True to update the original dataset
restaurantData.drop_duplicates(inplace=True)
#Checking if data duplcates are removed
print(restaurantData.duplicated().sum())



#Data type is changed to column, lets move ahead
#For first level EDA i'll be answering the following questions
# How many data were recorded
# Which was the most-ordered item?
# For the most-ordered item, how many items were ordered?
# How many items were orderd in total?
# How much was the revenue for the period in the dataset?
# What is the average revenue amount per order?

# How many data were recorded
print(f'The number of data is {restaurantData.shape[0]}')
#dataframe.shape gives tuple of rows and column (rows,column) just taking the 0 element i.e rows

# Which was the most-ordered item?
#first group the dataset on the basis of itemname and add all the values within group
#numeric_only= True is set to handle only numeric values
groupedDataSet = restaurantData.groupby('item_name').sum(numeric_only=True)
#now sorting the values by quantity in desceinding order
sortedGroup = groupedDataSet.sort_values('quantity',ascending=False)
#Now the most ordered item is of index 0 using iloc for implicit indexing
mostOrdered = sortedGroup.iloc[0]
print(f'The most ordered item is {mostOrdered}')

#Top selling item visualization
top_selling_items = restaurantData.groupby('item_name')['quantity'].sum().sort_values(ascending=False)
top_selling_items.head(5).plot(kind='bar')
plt.xticks(rotation=45, ha='right')
# Adjust the layout to make room for the x-axis labels
plt.tight_layout()
# Add a title
plt.title('Top 5 Best Selling Items')
# Show the plot
plt.show()

# For the most-ordered item, how many items were ordered?
print(f'For Most selling item the number of item ordered was {mostOrdered["quantity"]}')

# How many items were orderd in total?
totalItemOrdered = restaurantData['quantity'].sum()
print(f'The total items ordered were {totalItemOrdered}')

# How much was the revenue for the period in the dataset?
totalRevenue =(restaurantData['quantity'] * restaurantData['price']).sum(numeric_only=True)
print(f'Overall Revenue {np.round(totalRevenue,2)}')

# What is the average revenue amount per order?
#Adding a revenue column
restaurantData['revenue'] = restaurantData['quantity'] * restaurantData['price']
#Grouping by orderID
grouped_order = restaurantData.groupby(['order_id']).sum(numeric_only=True)
meanGroupedOrder = np.mean(grouped_order['revenue'])
print(f'The average amount per order {meanGroupedOrder}')

#Getting items per order
items_per_order = restaurantData.groupby('order_id')['item_name'].count().sort_values(ascending=False)
print(items_per_order)


#Advance
# Group by Date: restaurantData.groupby(restaurantData['createdAt'].dt.date)['price'].sum() groups the sales data by date and sums the prices to get total sales per day.
sales_trend = restaurantData.groupby(restaurantData['createdAtNepal'].dt.date)['price'].sum()

# Plotting the sales trend
plt.figure(figsize=(10, 6))
sales_trend.plot(kind='line', marker='o')
plt.title('Sales Trend Over Time')
plt.xlabel('Date')
plt.ylabel('Total Sales')
plt.xticks(rotation=30)
plt.grid(True)
plt.show()


#Sales trend over hour
# Extract hour from 'createdAt'
restaurantData['hour'] = restaurantData['createdAtNepal'].dt.hour

# Group by hour and sum the sales
hourly_sales_trend = restaurantData.groupby('hour')['price'].sum()

# Plotting the hourly sales trend
plt.figure(figsize=(10, 6))
hourly_sales_trend.plot(kind='line', marker='o')
plt.title('Hourly Sales Trend')
plt.xlabel('Hour of the Day')
plt.ylabel('Total Sales')
plt.xticks(range(0, 24))  # Ensure x-ticks cover all hours
plt.grid(True)
plt.show()



# Extract the day of the week from 'createdAt_NepalTime'
restaurantData['day_of_week'] = restaurantData['createdAtNepal'].dt.day_name()

# Group by day of the week and sum the sales
weekly_sales = restaurantData.groupby('day_of_week')['price'].sum()

# Ensure the days are in order from Sunday to Saturday
ordered_days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
weekly_sales = weekly_sales.reindex(ordered_days, fill_value=0)

# Plotting the weekly sales trend
plt.figure(figsize=(12, 6))
weekly_sales.plot(kind='bar', color='skyblue')
plt.title('Sales by Day of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Extract year and month from 'createdAt_NepalTime'
restaurantData['year_month'] = restaurantData['createdAtNepal'].dt.to_period('M')

# Group by year and month and sum the sales
monthly_sales = restaurantData.groupby('year_month')['price'].sum()

# Plotting the monthly sales trend
plt.figure(figsize=(12, 6))
monthly_sales.plot(kind='line', marker='o')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.grid(True)
plt.xticks(rotation=45)
plt.show()
