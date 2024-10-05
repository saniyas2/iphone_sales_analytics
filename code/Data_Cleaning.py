#%%
## Importing the libraries
import pandas as pd
import numpy as np

#%%

# Provide the relative path to your CSV file
file_path = '../data/apple_products.csv'

# Read the CSV file
sales_data = pd.read_csv(file_path)

# Display the dataframe
sales_data.head()
# %%
## Checking missing values
sales_data.isnull().sum()
# %%
## There are no missing values in the dataset
#%%
## Checking for unique values in Brand columns

sales_data['Brand'].unique()
# %%
## Performing Data Cleaning

## Here, I will be performing two steps to clean the data.

## 1.) Dropping columns like brand, UPC and URL as I feel these columns do not add much value to the analysis.
## 2.) Splitting the column Product Name into two columns :- Iphone Model and Storage Space

#%%
## Dropping the columns 

sales_data.drop(columns=['Brand', 'Upc', 'Product URL'], inplace=True)

## Displaying the first five rows

print(sales_data.head())
# %%


## Splitting the column Product Name into two columns :- Iphone Model and Storage Space
sales_data[['iPhone Model', 'Storage Space']] = sales_data['Product Name'].str.extract(r'iPhone\s([\w\s]+)\s?\([^\d]*(\d+)\s?GB\)')

# Display the cleaned dataframe
print(sales_data.head())
# %%

## Saving the data to a CSV file

sales_data.to_csv("../data/final_iphone_sales_data.csv")
# %%
