from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup
import pandas as pd
import time
import csv

def getCars(brand, car_name):
    driver = webdriver.Firefox()
    driver.maximize_window()

    # Storing variables
    cars=[]

    underCars=[] # Under the price average
    avgCars=[] # Average price
    overCars=[] # Over the price average
    otherCars=[] # Not specified

    prices=0

    website = "https://www.autovit.ro/autoturisme/"
    baseUrl = website + brand.strip().lower().replace(" ", "-") + "/" + car_name.strip().lower().replace(" ", "-")

    driver.get(baseUrl)

    # Make the driver wait for the button to be clickable
    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))

    # Click the button (after its clickable of course)
    button.click()
    # Let it breath for 5 seconds.
    time.sleep(5)

    # Extract the content
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")

    # Loop through all the articles
    def parseArticle(article):
        car = {}

        # Get the name of the car
        h1_name = article.find('h1', attrs={'class': "ev7e6t89 ooa-1xvnx1e er34gjf0"})
        name = h1_name.find('a')
        car["name"] = name.text.strip().replace(" ", "")

        # Get the price of the car
        price = article.find('h3', attrs={'class': "ev7e6t82 ooa-bz4efo er34gjf0"})
        car["price"] = int(price.text.strip().replace(" ", ""))

        # Get the description of the car
        descriptionDiv = article.find('div', attrs={"class": "ooa-1jgmfmo ev7e6t812"})
        description = descriptionDiv.find('p', attrs={"class": "ev7e6t88 ooa-17thc3y er34gjf0"})
        car["description"] = description.text.strip()
            
        # Add the prices and names to the lists
        cars.append(car)

        # Price status
        if article.find('p', attrs={"class": "e1xj1nw30 ooa-77y3u4 er34gjf0"}):
            car["priceStatus"] = article.find('p', attrs={"class": "e1xj1nw30 ooa-77y3u4 er34gjf0"}).text
        else:
            car["priceStatus"] = "Nespecificat"

        # Kilometers, Fuel type and year of fabrication
        infoDiv = article.find('dl', attrs={"class": "ooa-13lipl2 ev7e6t87"})
        kilometersText = article.find('dd', attrs={"data-parameter": "mileage"})
        fuelTypeText = infoDiv.find('dd', attrs={"data-parameter": "fuel_type"})
        yearText = infoDiv.find('dd', attrs={"data-parameter": "year"})

        try:
            car["kilometers"] = int(kilometersText.text.strip().replace(" ", "").replace("km", ""))
        except:
            car["kilometers"] = 0
        car["fuelType"] = fuelTypeText.text
        car["year"] = int(yearText.text.strip())
        
            

    def getArticles(soup1):
        for article in soup1.findAll('article', href=False, attrs={'class': 'ev7e6t818'}):
            parseArticle(article)

        time.sleep(4)
        action = ActionChains(driver)
        nextPageBtn = driver.find_element(By.XPATH, "//li[@title='Next Page']")

        time.sleep(4)

        driver.execute_script("window.scrollTo(0, document.querySelector(\"[title='Next Page']\").offsetTop + 100)")
        action.move_to_element(nextPageBtn).click().perform()

        time.sleep(8)

        try:
            driver.find_element(By.CLASS_NAME, "pagination-item__disabled")
            print("A ajuns la ultima pagina.")
        except:
            getArticles(BeautifulSoup(driver.page_source, "html.parser"))

        

        
    print("---- EXTRACTAND MASINILE ----")
    try: 
        driver.find_element(By.XPATH, "//li[@title='Next Page']")
        getArticles(BeautifulSoup(driver.page_source, "html.parser"))
    except:
        pass

    print("---- EXTRACTAND ULTIMA PAGINA ----")
    for article in BeautifulSoup(driver.page_source, "html.parser").findAll('article', href=False, attrs={'class': 'ev7e6t818'}):
        parseArticle(article)

    cars = sorted(cars, key=lambda x: x["price"])

    with open(f"{car_name.capitalize()}.csv", 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = ["name", "price", "description", "price status", "year", "kilometers", "fuel type"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        
        for car in cars:
            prices += car["price"] # Add every price of the car in one variable for the average price calculation

            writer.writerow({"name": car["name"], "price": car["price"], "description": car["description"], "price status": car["priceStatus"], "year": car["year"], "kilometers": car["kilometers"], "fuel type": car["fuelType"]})


    time.sleep(2)

    avg_price = int(prices / len(cars))

    for car in cars:
        if car["price"] < avg_price - 10000:
            underCars.append(car)
        elif car["price"] < avg_price and car["price"] > avg_price - (avg_price / 3):
            avgCars.append(car)
        elif car["price"] > avg_price:
            overCars.append(car)

    # Quit the driver.
    driver.quit()
    return cars, str(avg_price), [underCars[0], avgCars[0], overCars[0]]