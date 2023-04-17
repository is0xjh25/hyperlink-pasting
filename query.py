import requests
import json
import jsonify
import urllib.parse

class Query:
	
	nominatim_url = "https://nominatim.openstreetmap.org/"
	open_street_url = "https://api.openstreetmap.org/"
	map_range = "#map=9/-37.7783/145.1624"
	
	def __init__(self, building_name):
		self.building_name = building_name
		self.way_id = ""
		self.way = {}
	
	# search by the function provided by Boat
	def find_hyperlink(self) -> str:
		return "testing"

	def find_way_id(self) -> str:
		place = urllib.parse.quote((self.building_name + ", Melbourne, Australia").encode('utf8'))
		
		try:
			res = requests.get(Query.nominatim_url + "search/{place}?format=json&addressdetails=1&limit=1&polygon_svg=1".format(place=place) + self.map_range)
			res = json.loads(res.text)
			self.way_id = str(res[0]['osm_id'])
		except:
			print(self.building_name)

		return self.way_id

	def read_way(self) -> {}:
		if self.way_id == "": 
			print("xxx")
		else:
			try:
				print(self.way_id)
				res = requests.get(Query.open_street_url + "api/0.6/way/" + self.way_id + ".json")
				self.way = json.loads(res.text)
				print(self.way)
			except:
				print("!!!")

		return self.way
