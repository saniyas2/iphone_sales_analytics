#%%
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import pandas as pd

# Initialize Selenium WebDriver using Chrome
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run browser in headless mode (without GUI)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Initialize lists to store scraped data
Product_name = []
Discounted_Prices = []
Average_Ratings = []
Total_Ratings_Reviews = []
Description = []

# Starting URL (first page)
current_url = "https://www.flipkart.com/search?q=apple+phone&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_5_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_1_5_na_na_ps&as-pos=1&as-type=RECENT&suggestionId=apple+phone%7CMobiles&requestId=46fc1ac4-b417-4242-b6c0-600ceb9bcca6&as-searchtext=apple&page=1"

page_number = 1  # Initialize page number
max_pages = 23   # Maximum number of pages to scrape

while True:
    # Display the page number being scraped
    print(f"Scraping page {page_number}...")

    # Use Selenium to open the page
    driver.get(current_url)

    # Wait for the page to load
    time.sleep(5)  # Adjust sleep time as necessary

    # Use BeautifulSoup to parse the page content
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all the product boxes on the page
    product_boxes = soup.find_all('div', class_='_75nlfW')

    # Loop through each product box
    for box in product_boxes:
        # Extract product name
        name = box.find("div", class_="KzDlHZ")
        if name:
            Product_name.append(name.text)
        else:
            Product_name.append(None)  # Handle missing product name

        # Extract discounted prices
        discounted_price = box.find("div", class_='Nx9bqj _4b5DiR')
        if discounted_price:
            Discounted_Prices.append(discounted_price.text)
        else:
            Discounted_Prices.append(None)  # Handle missing discounted price

        # Extract average ratings
        average_rating = box.find("span", class_="Y1HWO0")
        if average_rating:
            Average_Ratings.append(average_rating.text)
        else:
            Average_Ratings.append(None)  # Handle missing rating

        # Extract total ratings and reviews
        total_ratings_review = box.find("span", class_="Wphh3N")
        if total_ratings_review:
            Total_Ratings_Reviews.append(total_ratings_review.text)
        else:
            Total_Ratings_Reviews.append(None)  # Handle missing total ratings/reviews

        # Extract description
        description = box.find("ul", class_="G4BRas")
        if description:
            Description.append(description.text)
        else:
            Description.append(None)  # Handle missing description

    # Find the 'Next' button based on anchor tag class
    next_button = soup.find('a', class_='_9QVEpD')

    if next_button and page_number < max_pages:
        next_page_url = 'https://www.flipkart.com' + next_button['href']
        current_url = next_page_url
        page_number += 1  # Increment page number
    else:
        # No 'Next' button found or page limit reached; exit the loop
        break

# Create a DataFrame from the scraped data
df = pd.DataFrame({
    'Product Name': Product_name,
    'Discounted Price': Discounted_Prices,
    'Average Rating': Average_Ratings,
    'Total Ratings and Reviews': Total_Ratings_Reviews,
    'Description': Description
})

# Print the first few rows of the DataFrame
print(df.head())

# Print the shape of the DataFrame to check the size
print(df.shape)

# Close the WebDriver instance
driver.quit()
# %%
print(df.head().to_string)
# %%

# Task 1: Remove '₹' from Discounted Price and convert to integer
df['Discounted Price'] = df['Discounted Price'].str.replace('₹', '').str.replace(',', '').astype(int)

# Task 2: Separate 'Total Ratings and Reviews' into two columns
df[['Total Ratings', 'Total Reviews']] = df['Total Ratings and Reviews'].str.extract(r'(\d[\d,]*) Ratings\s+&\s+(\d[\d,]*) Reviews')

# Convert the newly created columns to integer format by removing commas
df['Total Ratings'] = df['Total Ratings'].str.replace(',', '').astype(int)
df['Total Reviews'] = df['Total Reviews'].str.replace(',', '').astype(int)

# Task 3: Separate 'Product Name' into three columns: Model Type, Color, and Storage Space
df[['Model Type', 'Color', 'Storage Space']] = df['Product Name'].str.extract(r'Apple (iPhone [\w\s]+) \(([\w\s]+), ([\d\s]+[TG]B)\)')

# Fill missing values for non-Apple products (if necessary)
df['Model Type'] = df['Model Type'].fillna('Non-iPhone')
df['Color'] = df['Color'].fillna('N/A')
df['Storage Space'] = df['Storage Space'].fillna('N/A')

# Optional: Drop the original 'Total Ratings and Reviews' and 'Product Name' columns if no longer needed
df.drop(columns=['Total Ratings and Reviews'], inplace=True)

#%%
## Dropping Rows which are not iphone

df = df.loc[df['Model Type'] != 'Non-iPhone']
# %%
print(df.shape)
# %%
df.to_csv("../data/final_iphone_sales.csv")
# %%
