# Autovit.ro webscraping project

This is a web scraping project that extracts car information from autovit.ro, a popular Romanian car sales website. The project is implemented using Python and the Selenium and BeautifulSoup libraries.

## Project Overview
The web scraping project consists of two main components:

1. `searchCars.py`: This python script contains the code to extract car information. It uses Selenium to interact with the autovit.ro website and BeautifulSoup to parse the HTML content. The script allows you to search for cars by specifying the brand and model, and it provides information about various car listings, including name, price, description, price status (if it is specified), year, kilometers and fuel type. It also calculates the average price of the searched cars and categorize them as under average, average and over average price.

2. `main.py`: This script provides a GUI for the web scraping project. It allows users to select a car brand and a model or if they want something that is not provided by the list, they can search for a specific brand and model. It then displays the results, including average price and the cheapest, average and expensive ones.

## Requirments (in order to run the project):
* Selenium
* BeautifulSoup
* Firefox web browser
* customtkinter
* CTkListbox

Install them using the following command:
```pip install selenium beautifulsoup4 customtkinter CTklistbox```

## How to use the app:
1. Run the `main.py` script.
2. Use the interface to select a brand, view available models and press the 'Cauta' button.
! If you want a specific brand and a model that isn't displayed already, press the 'Cauta un model de masina specific' and enter the brand and model name. Make sure it's correct and the car is listed on autovit.ro
3. Wait for the results to be displayed.