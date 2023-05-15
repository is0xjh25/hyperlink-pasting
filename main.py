import query
import sys
import utilities as util
# import web_scraping as ws

campus = sys.argv[1]
campus_list = ['burnley', 'creswick', 'dookie', 'parkville', 'shepparton', 'southbank', 'werribee']
url = "./Mapping/unimelb_{}_url.xlsx".format(campus)

def main() -> None:
	if campus.lower() not in campus_list:
		print("[ERROR]: {} is not a Unimelb campus.".format(campus))
		return None
	log_handler = util.Log(campus.lower())
	buildings = util.read_exec(url)
	# # loop all the building in campus
	for building_info in buildings:
		building = query.Query(log_handler, building_info)
		building.execute()
	return None

if __name__ == "__main__":
	main()