import requests
import csv
from bs4 import BeautifulSoup

#We are using headers so site can trust us more
headers = { 
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}
RUNNINGTYPE = "Diesel"

#First things first we need to write our table headers
with open ("CampingworldData.csv", "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(
        ("Stock Number","Location", "Lenght","Sleeps","Condition", "Price", "Horsepowers")
    )

#Collecting all car's links
for page in range (1, 21):
    url = "https://rv.campingworld.com/rvclass/motorhome-rvs?page=" + str(page)
    req = requests.get(url=url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    all_hrefs = soup.find_all(class_="productTitle")
    links = []

    for link in all_hrefs:
        item_text = link.text
        item_href = "https://rv.campingworld.com/" + link.get("href")
        links.append(item_href)

    #Collecting characteristics for each car
    for item in links:
        req = requests.get(url=item, headers=headers)
        soup = BeautifulSoup(req.text, "lxml")
        
        try:
            fueltype = soup.find("div", class_="tab-pane show active").find("h4", string="FUEL TYPE").find_next("h5").text
            if fueltype == RUNNINGTYPE:
                sleeps = soup.find("div", class_="tab-pane show active").find("h4", string="SLEEPS").find_next("h5").text
                lenght = soup.find("div", class_="tab-pane show active").find("h4", string="LENGTH").find_next("h5").text
                price = soup.find("span", attrs={"class": "price-info low-price"}).text
                location = soup.find("span", class_="stock-results").find("b").text
                stock_num = soup.find("div", class_="stock-num-prod-details").text
                condition = soup.find("h1", class_="roundedPill assetCondition pull-right").text
                if int(price.translate({ord(i): None for i in '$,'})) >= 300000:
                    horsepowers = soup.find("div", class_="tab-pane show active").find("h4", string="HORSEPOWER").find_next("h5").text
                else:
                    horsepowers = ""

                #Writing all data to our CSV file
                with open ("CampingworldData.csv", "a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        (stock_num, location, lenght, sleeps, condition, price, horsepowers)
                    )
        except Exception:
            pass
