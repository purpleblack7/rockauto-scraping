from bs4 import BeautifulSoup
import requests
import inquirer

def cust_specs(): 
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

	#for trim in trim_hrefs.keys():
	#
	#print(trim_hrefs)


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
	return(final_url)	
