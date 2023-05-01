import query
import utilities as util
# import web_scraping as ws

campus = "Parkville"

def main() -> None:
	# all_campus = ws.all_campus_scrapping()
	# print(all_campus)
	# # loop all the building
	log_handler = util.Log(campus)
	# original changeset for Wilson Hall = 133358889
	# q1 = query.Query(log_handlerm, building_info)
	q1 = query.Query(log_handler, "Wilson Hall")
	q1.execute()
	return None

if __name__ == "__main__":
	main()