from bs4 import BeautifulSoup
import requests
import inquirer


#Getting the base URL from rockauto. All searches in English start with this
url="https://www.rockauto.com/en/catalog/"

#Getting the car details from the user. Note: Functionize this with error catching included
make = input("Enter the name of the Manufacturer: ")
year = input("Enter the year of the vehicle: ")
model = input("Enter the model of the vehicle: ")

#Appending the retrieved parameters to make the URL more precise
basic_url = url + make + "," + year + "," + model

page = requests.get(basic_url) 

soup = BeautifulSoup(page.content, "html.parser")

#treeroot[catalog] is the portion where you select the Manufacturer begins
results = soup.find(id = "treeroot[catalog]")

#Finding all the trims of the car selected
elements = results.find_all("a",class_ = "navlabellink nvoffset nnormal", href = True)

# Getting the trims and the corresponding urls for the selected make and model
trim_hrefs = {}
for element in elements:
	if element.get_text() not in {make.upper(),year,model.upper()}:
		trim_hrefs[element.get_text()] = element['href']		

def list_stripper(elements, exclusion_set = {make.upper(),year,model.upper()})
	"""
	Rockauto's links change based on the option selected and this function is to provide the items that exist under each submenu. There will be redundant things in the list (like the brand name and the model name) which is already known. This is to extract the other items in the list (such as engine configuration and part categories
	A function that takes in a Result set and does the following:
		* Takes the text only headers (except for those not required as they are not in the scope
		* The corresponding link in rockauto.com


		:elements: The ResultSet for which the operation has to be performed
		:exclusion_set: The list elements to avoid



For example, According to Rock Auto, the nested lists are like this
		Car Make ->Year -> Model -> Parts Categories -> Part Types -> The actual parts

To get an input from the user, we list the available choices for each parent menu. But if we were to choose Parts Categories, the names of its parent lists also shows up. This function excludes the parent names from the item:url dictionary


		returns: A dicticnary with item:URL format

	"""

questions = [
  inquirer.List('trim',
		message = "Select your engine configuration",
		choices = trim_hrefs.keys()
		),
]
answers = inquirer.prompt(questions)
print("You selected: ",answers["trim"])
trim_selected = answers["trim"]
print(trim_hrefs[trim_selected])
final_url = "https://www.rockauto.com"+ trim_hrefs[trim_selected] 

###The actual scraping


page = requests.get(final_url)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find_all("a", class_ = "navlabellink nvoffset nnormal", href = True )


#print(type(results))

print(results)


for element in results:
	print(element.get_text())

