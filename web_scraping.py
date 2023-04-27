import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

campus_info = {
	'werribee': {'code': 'WER', 'id': 217},
	'dookie': {'code': 'DOO', 'id': 220},
	'shepparton': {'code': 'SPT', 'id': 221},
	'southbank': {'code': 'STH', 'id': 216},
	'burnley': {'code': 'BUR', 'id': 218},
	'creswick': {'code': 'CRE', 'id': 219},
	'parkville': {'code': 'PAR', 'id': 200}
}

driver = webdriver.Chrome(ChromeDriverManager().install())

def get_campus_url(campus):
	return "https://maps.unimelb.edu.au/{}/building".format(campus.lower())

def single_campus_scrapping(campus) -> [{}]:
	driver.get(get_campus_url(campus))
	content = driver.page_source
	soup = BeautifulSoup(content, 'html.parser')
	# print(soup.prettify())
	
	Building = []
	Urls = []
	Building_no = []
	#Update the logic to support issue on southbank campus
	for d in soup.find_all('li',{'class' : ['cell Building', 'cell Building Food and drink']}):
		a_tag = d.find('a')  # find the first 'a' tag in the HTML
		url = a_tag['href'] # get the value of the 'href' attribute
		building_name = a_tag.text.strip()  # get the text content of the tag and remove any leading/trailing white space
		#Urls.append(url)
		Building.append(building_name)
		 
	for d in soup.findAll('span', {'title': 'Building Number'}):
		buildNo = d.text.strip()
		Building_no.append(buildNo)
	
	df_campus = pd.DataFrame({'Building name':Building,'No': Building_no})

	# Remove the last 6 characters from all values in the "Building name" column
	df_campus['Building name'] = df_campus['Building name'].apply(lambda x: x[0:len(x)-6])

	# Check blank building name
	id_blank_bd_name = df_campus['Building name'] == ''

	# Define a lambda function to update the URL string
	def update_building_name(row):
		return ('Building ' + row['No'])
	# Apply the lambda function to the "no" column and assign the results to a new column "url"
	df_campus.loc[id_blank_bd_name, 'Building name'] = df_campus.apply(update_building_name, axis=1)

	# #Create campus id mapping
	# campus_id_mapping = pd.DataFrame(data={'campus_code': ['WER', 'DOO','SPT','STH','BUR','CRE','PAR'], 'campus_id': [217, 220,221,216,218,219,200]})

	# Look up the campus_id for a given campus_code
	campus_id = campus_info[campus.lower()]['id']

	# Define a lambda function to update the URL string
	def update_url(row):
		return 'https://use.mazemap.com/?campusid={}&sharepoitype=identifier&sharepoi={}'.format(campus_id, row['No'])
	
	# Apply the lambda function to the "no" column and assign the results to a new column "url"
	df_campus['url'] = df_campus.apply(update_url, axis=1)

	# Print the updated dataframe
	df_campus['url'].head(5)

	"""
	Export to Excel
	"""
	df_campus.to_excel("unimelb_{}_url.xlsx".format(campus.lower()), index=False)

	"""
	Return as json
	"""
	res = []
	# for index, row in df_campus.iterrows():
	# 	building = {}
	# 	building['building_name'] = row['Building name']
	# 	building['building_number'] = row['No']
	# 	building['url'] = row['url']
	# 	res.append(building)

	return res

def all_campus_scrapping() -> {}:
	res = {}
	for campus in campus_info.keys():
		res[campus] = single_campus_scrapping(campus)
	return res

res = single_campus_scrapping('parkville')
# print(res)
# all_campus_scrapping()
