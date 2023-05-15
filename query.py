import requests
import json
import configparser
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from lxml import etree

config = configparser.ConfigParser()
config.read('config.ini')
username = config['JIM']['username']
password = config['JIM']['password']

class Query:
	
	nominatim_url = "https://nominatim.openstreetmap.org/"
	open_street_url = "https://api.openstreetmap.org/"
	
	def __init__(self, log_handler, building_info) -> None:
		self.log_handler = log_handler
		self.building_info = building_info
		self.new_changeset = ""
		self.way_id = ""
		self.original_way = ""
		self.updated_way = ""
		self.formal_updated_way = ""
		return
	
	def find_way_id(self) -> None:
		print("___________________________________________")
		print(self.building_info['building_name'])
		print(self.building_info)
		place_one = urllib.parse.quote((self.building_info['building_name'].replace('/', '') + ", Melbourne, Australia").encode('utf8'))
		place_two = urllib.parse.quote((self.building_info['building_name'].replace('/', '')).encode('utf8'))
		try:
			url = Query.nominatim_url + "search/{}?format=json&addressdetails=1&limit=1&polygon_svg=1".format(place_one)
			res = requests.get(url)
			res = json.loads(res.text)
			try:
				print(url)
				self.way_id = str(res[0]['osm_id'])
			except:
				# when first searching fails
				print("[SECOND ATTEMPT]")
				url = Query.nominatim_url + "search/{}?format=json&addressdetails=1&limit=1&polygon_svg=1".format(place_two)
				print(url)
				res = requests.get(url)
				res = json.loads(res.text)
				self.way_id = str(res[0]['osm_id'])
		except:
			self.log_handler.log_error("[ERROR: WAY_ID CANNOT BE FOUND]")
		return None

	def read_original_way(self) -> None:
		url = Query.open_street_url + "api/0.6/way/" + self.way_id
		try:
			res = requests.get(url)
			self.original_way = res.text
		except:
			self.log_handler.log_error("[ERROR: WAY CANNOT BE FOUND]")
		return None
	
	def create_changeset(self) -> None:
		url = "https://api.openstreetmap.org/api/0.6/changeset/create"
		headers = {'Content-Type': 'text/xml'}
		# xml = """<osm><changeset><tag k="created_by" v="is0xjh25"/></changeset></osm>"""
		xml = """<osm><changeset><tag/></changeset></osm>"""
		root = ET.fromstring(xml)
		tag = root.find('.//tag')
		tag.set('k', 'created_by')
		tag.set('v', username)
		xml = ET.tostring(root)
		try:
			res = requests.put(url, headers=headers, data=xml, auth=(username, password))
			changeset_id = res.content.decode('utf-8')
			self.new_changeset = changeset_id
		except:
			self.log_handler.log_error("[ERROR: CHANGESET CANNOT BE CREATE]")
		return None
	
	def close_changeset(self) -> None:
		url = "https://api.openstreetmap.org/api/0.6/changeset/{}/close".format(self.new_changeset)
		headers = {'Content-Type': 'text/xml'}
		try:
			res = requests.put(url, headers=headers, auth=(username, password))
		except:
			self.log_handler.log_error("[ERROR: CHANGESET CANNOT BE CLOSED]")
		return None

	def update_way(self) -> None:
		self.create_changeset() # get new changeset for the update
		self.edit_xml() # update xml
		self.form_update_xml() # update xml
		url = "https://api.openstreetmap.org/api/0.6/changeset/{}/upload".format(self.new_changeset)
		xml = ET.tostring(self.formal_updated_way, encoding='unicode')
		headers = {'Content-Type': 'application/xml'}
		try:
			res = requests.post(url, data=xml, headers=headers, auth=(username, password))
		except:
			self.log_handler.log_error("[ERROR: NEW WAY CANNOT BE UPDATED]")
		finally:
			self.close_changeset()
		return None

	def edit_xml(self) -> None:
		root = ET.fromstring(self.original_way)
		# change original tag attributes
		way = root.find('.//way')
		way.set('changeset', self.new_changeset)
		way.set('user', username)
		way.set('timestamp', str(datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")))
		way.attrib.pop('uid', None)
		# change website:map, etc...
		for key in self.building_info:
			if (key == "building_name" or key == "building_no"):continue
			new_ele = ET.Element('tag', k=key, v=str(self.building_info[key]))
			old_ele = root.find(".//tag[@k='{}']".format(key))
			if old_ele is not None: root[0].remove(old_ele)
			root[0].append(new_ele)
		self.updated_way = root
		return None
	
	def form_update_xml(self) -> None:
		old_root = self.updated_way[0]
		new_xml = '''<osmChange><modify></modify></osmChange>'''
		new_root = ET.fromstring(new_xml)
		new_root[0].append(old_root)
		self.formal_updated_way = new_root
		return None

	def pretty_xml (self, xml) -> str:
		if xml == "": return "[ERROR: UNABLE TO CREATE]"
		return ET.tostring(xml).decode()

	def execute(self) -> None:
		try:
			self.log_handler.log_header(self.building_name)
			self.find_way_id()
			self.read_original_way()
			self.update_way()
		except:
			print("[ERROR]: {}".format(self.building_name))
		msg = {
			"way_id": self.way_id,
			"original_way": self.original_way,
			"updated_way": self.pretty_xml(self.formal_updated_way)
		}
		self.log_handler.log_main(msg)
		return None