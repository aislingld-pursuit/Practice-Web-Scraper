import requests
from bs4 import BeautifulSoup
import csv

# Step 1: Fetch the page
url = "https://www.scrapethissite.com/pages/simple/"
response = requests.get(url)
response.raise_for_status() # ensure request succeeded1  

# Step 2: Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Step 3: Extract team info
country = soup.find_all("div", class_="country")

# Prepare data in a CSV
country_data = []

for country in country:
    name = country.find("h3", class_="country-name").get_text(strip=True)
    capital = country.find("span", class_="country-capital").get_text(strip=True)
    population = country.find("span", class_="country-population").get_text(strip=True)
    area = country.find("span", class_="country-area").get_text(strip=True)

    # Store data in a dictionary
    country_data.append({
        "Name": name,
        "Capital": capital,
        "Population": population,
        "Area": area
    })

# Write to CSV file

csv_filename = "country_data.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Name", "Capital", "Population", "Area"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader() # Write header row
    writer.writerows(country_data) # Write all the data Row


print(f"Data saved to {csv_filename}")