import requests
import json
import urllib.parse

class Query:
	
	nominatim_url = "https://nominatim.openstreetmap.org/"
	open_street_url = "https://api.openstreetmap.org/"
	map_range = "#map=9/-37.7783/145.1624"
	
	def __init__(self, log_handler, building_name):
		self.log_handler = log_handler
		self.building_name = building_name
		self.hyperlink = ""
		self.way_id = ""
		self.original_way = {}
		self.update_way = {}
	
	# search by the function provided by Boat
	def find_hyperlink(self) -> None:
		self.hyperlink = "testing"
		return None

	def find_way_id(self) -> None:
		place = urllib.parse.quote((self.building_name + ", Melbourne, Australia").encode('utf8'))
		
		try:
			res = requests.get(Query.nominatim_url + "search/{place}?format=json&addressdetails=1&limit=1&polygon_svg=1".format(place=place) + self.map_range)
			res = json.loads(res.text)
			self.way_id = str(res[0]['osm_id'])
		except:
			self.log_handler.log_error(self.building_name, "[ERROR: WAY_ID CANNOT BE FOUND]")
		return None

	def read_original_way(self) -> None:
		try:
			res = requests.get(Query.open_street_url + "api/0.6/way/" + self.way_id + ".json")
			self.original_way = json.loads(res.text)
		except:
			self.log_handler.log_error(self.building_name, "[ERROR: WAY CANNOT BE FOUND]")
		return None
	
	def execute(self) -> None:
		self.log_handler.log_header(self.building_name)
		self.find_hyperlink()
		self.find_way_id()
		self.read_original_way()
		msg = {
			"hyperlink": self.hyperlink,
			"way_id": self.way_id,
			"original_way": json.dumps(self.original_way)
		}
		self.log_handler.log_main(msg)
		return None
