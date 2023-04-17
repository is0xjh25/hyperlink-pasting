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
	
	# search by the function provided by Boat
	def find_hyperlink(self) -> str:
		return "testing"

	def find_way_id(self) -> str:
		place = urllib.parse.quote((self.building_name + ", Melbourne, Australia").encode('utf8'))
		response = requests.get(Query.nominatim_url + "search/{place}?format=json&addressdetails=1&limit=1&polygon_svg=1".format(place=place) + self.map_range)
		res = json.loads(response.text)
		if len(res) == 0:
			print(self.building_name)
		elif res[0]['osm_id']:
			self.way_id = res[0]['osm_id']
		else:
			# log error
			print(self.building_name)
		# response1 = requests.get(Query.open_street_url + "api/0.6/way/" + str(res[0]['osm_id']))
		# print(response1.text)
		# print(self.way_id)
		return self.way_id

	def read_way(self) -> {}:
		return {}
