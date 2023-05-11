import query
import utilities as util
# import web_scraping as ws

campus = "werribee"
url = "./Mapping/unimelb_{}_url.xlsx".format(campus)
def main() -> None:

	log_handler = util.Log(campus)
	# {'building_name': 'Werribee Biohazard Depot', 'building_number': '415', 'url': 'https://use.mazemap.com/?campusid=217&sharepoitype=identifier&sharepoi=415'}, 
	# buildings = [{'building_name': 'Werribee Biohazard Depot', 'building_number': '415', 'url': 'https://use.mazemap.com/?campusid=217&sharepoitype=identifier&sharepoi=415'}, {'building_name': 'Building 411', 'building_number': '411', 'url': 'https://use.mazemap.com/?campusid=217&sharepoitype=identifier&sharepoi=411'}]
	buildings = util.read_exec(url)
	# # loop all the building in werribee
	for building_info in buildings:
		building = query.Query(log_handler, building_info)
		building.execute()
	return None

if __name__ == "__main__":
	main()