from bs4 import BeautifulSoup
import requests

url="https://www.rockauto.com/en/catalog/"

make = input("Enter the name of the Manufacturer")
year = input("Enter the year of the vehicle")
model = input("Enter the model of the vehicle")

basic_url = url + make + "," + year "," + model

page = requests.get(basic_url)  

print(page.text) 
