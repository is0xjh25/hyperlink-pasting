import query
import utilities as util
# import web_scraping as ws

campus = "test"

def main() -> None:
	# all_campus = ws.all_campus_scrapping()
	# werribee_campus = all_campus['werribee']
	# log_handler = util.Log('werribee')

	log_handler = util.Log('test')
	# {'building_name': 'Werribee Biohazard Depot', 'building_number': '415', 'url': 'https://use.mazemap.com/?campusid=217&sharepoitype=identifier&sharepoi=415'}, 
	buildings = [{'building_name': 'Werribee Biohazard Depot', 'building_number': '415', 'url': 'https://use.mazemap.com/?campusid=217&sharepoitype=identifier&sharepoi=415'}, {'building_name': 'Building 411', 'building_number': '411', 'url': 'https://use.mazemap.com/?campusid=217&sharepoitype=identifier&sharepoi=411'}]
	# # loop all the building in werribee
	for building_info in buildings:
		building = query.Query(log_handler, building_info)
		building.execute()



	return None

if __name__ == "__main__":
	main()