import requests
from bs4 import BeautifulSoup

# Step 1: Fetch the page
url = "https://www.scrapethissite.com/pages/simple/"
response = requests.get(url)
response.raise_for_status() # ensure request succeeded1  

# Step 2: Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Step 3: Extract team info
country = soup.find_all("div", class_="country")

for country in country:
    name = country.find("h3", class_="country-name").get_text(strip=True)
    capital = country.find("span", class_="country-capital").get_text(strip=True)
    population = country.find("span", class_="country-population").get_text(strip=True)
    area = country.find("span", class_="country-area").get_text(strip=True)

    print(f"{name} | Captial: {capital} | Population: {population} | Area: {area} km²")