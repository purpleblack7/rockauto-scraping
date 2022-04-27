from bs4 import BeautifulSoup
import requests
import inquirer
import re
import pandas as pd

#Getting the base URL from rockauto. All searches in English start with this
url="https://www.rockauto.com/en/catalog/"
bare_url = "https://www.rockauto.com/"

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
#trim_hrefs = {}
#for element in elements:
#	if element.get_text() not in {make.upper(),year,model.upper()}:
#		trim_hrefs[element.get_text()] = element['href']		
#
def list_stripper(elements, exclusion_set):
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
	output_set = {}

	for element in elements:
		if element.get_text() not in exclusion_set:
			output_set[element.get_text()] = element['href']		
	return output_set


#Creating the exclusion set. This set will be appended to the further we go down the list.
list_position = [make.upper(),year,model.upper()]

trim_hrefs = list_stripper(elements,list_position)
questions = [
  inquirer.List('trim',
		message = "Select your engine configuration",
		choices = trim_hrefs.keys()
		),
]
answers = inquirer.prompt(questions)
print("You selected: ",answers["trim"])
trim_selected = answers["trim"]
#print(trim_hrefs[trim_selected])
inter_url = bare_url+ trim_hrefs[trim_selected] 



##Adding the trim to the exclusion list

list_position.append(answers["trim"]) 
###The actual scraping


page = requests.get(inter_url) 
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find_all("a", class_ = "navlabellink nvoffset nnormal", href = True )

part_categories_href = list_stripper(results, list_position)

###### For later when iterating over multiple elements
#for pc in part_categories_href.keys():
#	print("Extracting {0} data".format(pc))
#	inter_url =  bare_url + part_categories_href[pc]
#	page = requests.get(inter_url) 
#	soup = BeautifulSoup(page.content, "html.parser")
#
#	#treeroot[catalog] is the portion where you select the Manufacturer begins
#	results = soup.find_all("td", class_ ="nlabel") 



# Testing for single element in the list. Convert to iteration when done

## This part gets a bit tricky and I'm unable to use list_stripper because there is no one properly defined class here. It goes from 'navlabellink nvoffset nimportant' to 'navlabellink nvoffset nnormal' to even 'navlabellink nvoffset nreversevideo'(lol wut?). So I tried a different approach here where I extract the link first and build the string from there.

#Creating a master dataframe
df =pd.DataFrame()

part_cat = 'Accessories'
inter_url = bare_url + part_categories_href['Accessories']
page = requests.get(inter_url)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find_all("td", class_ = "niconspace ncollapsedicon")
href_list = []
pc_href = {}
#Getting all the links first
for result in results:
	element = result.find(href = True)
	href_list.append(element['href'])
#Building the string from it
for href in href_list:
	text = href.split(',')[6].replace('+',' ').upper()
	pc_href[text] = href


for pc in pc_href:
	print(pc)
	inter_url = bare_url + pc_href[pc]
	page = requests.get(inter_url)
	soup = BeautifulSoup(page.content, "html.parser")
	#Getting the manufacturer details as well as the details of the part
	results = soup.find_all("div",class_ ="listing-text-row-moreinfo-truck")
	#print(type(result))

	#Initializing Empty Lists
	manufacturer_list = []
	part_num_list = []
	desc_list = []
	part_text_list = []
	price_list = []
	
	for result in results:
		#The name of the manufacturer	
		manufacturer = result.find("span", class_ = "listing-final-manufacturer")
		print(manufacturer.get_text())
		manufacturer_list.append(manufacturer.get_text())
		#The part number in RockAuto
		part_num = result.find("span", class_ = "listing-final-partnumber as-link-if-js buyers-guide-color")
		print(part_num.get_text())
		part_num_list.append(part_num.get_text())
		#The description of the part
		desc = result.find("span", class_ = "span-link-underline-remover")
		desc_list.append(desc.get_text())
		print(desc.get_text())
	#Since the text uder the part description is in another class, it lies outside the listing-text-row-moreinfo-truck class
	results_text = soup.find_all("div", class_ = "listing-text-row")
	for result_text in results_text:
		print(result_text.get_text())
		part_text_list.append(result_text.get_text())
	#Getting the price of the product
	results_price = soup.find_all("span", class_ ="ra-formatted-amount listing-price listing-amount-bold")
	for result_price in results_price:
		print(result_price.get_text())
		price_list.append(result_price.get_text())

	print(part_num_list)
	print(manufacturer_list)
	print(desc_list)
	print(part_text_list)
	print(price_list)

	#Creating an intermediate dataframe
	df1= pd.DataFrame([part_num_list,manufacturer_list,desc_list, part_text_list,price_list]).T#, columns = ["ID","Manufacturer","Description","Details","Price"])
	print(df1)
	df = pd.concat([df,df1])

df = df.rename(columns = {0:"ID",1:"Manufacturer",2:"Description",3:"Details",4:"Price"})	
print(df)

#<span class="listing-final-partnumber  as-link-if-js buyers-guide-color" id="vew_partnumber[10394]" onclick="if (cataloglite.IsMobileAndNotExpanded(&quot;10394&quot;)) { return; } cataloglite.ShowBuyersGuidePopup(&quot;10394&quot;);" title="Buyer's Guide" alt="Buyer's Guide">11423</span>
	#kyu = result.find("span", class_ = "listing-final-manufacturer")
#	print(kyu)
#<span class="ra-formatted-amount listing-price listing-amount-bold"><span id="dprice[837][v]">$310.79</span></span>
