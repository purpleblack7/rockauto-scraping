
def collect(url):
	"""
	Takes in the final url from the inputs and scrapes prices from the link for the selected car/truck
	"""


	page = requests.get(url)
	soup = BeautifulSoup(page.content, "html.parser")
	results = soup.find_all("td", class_ = "nlabel", href = True)
	print(results)

	
