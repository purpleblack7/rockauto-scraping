from bs4 import BeautifulSoup
import requests

url ="https://www.rockauto.com/en/catalog"

page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find('div')
print(results)
