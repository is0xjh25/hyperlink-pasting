import datetime
import pandas as pd

class Log:
	divide_line = "------------------------------------------------------------\n"
	def __init__(self, loc):
		self.loc = loc
		self.file_name = self.init_log_file()

	def init_log_file(self) -> str:
		now = datetime.datetime.now().strftime("%Y-%m-%d %H%M")
		file_name = "{loc}-{time}".format(loc=self.loc, time=now)
		try:
			f = open(file_name + ".txt", "w")
			try:
				f.write(file_name+'\n')
				f.write(Log.divide_line+'\n')
			except:
				print("[ERROR: WRITE FILE FAILED (init)]")
		except:
			print("[ERROR: CREATE FILE FAILED (init)]")
			exit(1)
		else:
			print("[FILE CREATED SUCCESSFULLY (init)]")
			f.close()
		return file_name + ".txt"

	def log_header(self, building_name) -> None:
		now = datetime.datetime.now().strftime("%H:%M:%S")
		try:
			f = open(self.file_name, "a")
			try:
				f.write(Log.divide_line)
				f.write("[{building_name}, {loc} {time}]\n\n".format(building_name=building_name, loc=self.loc, time=now))
			except:
				print("[ERROR: WRITE FILE FAILED (header)]")
		except:
			print("[ERROR: OPEN FILE FAILED (header)]")
		else:
			f.close()

		return None

	def log_main(self, msg) -> None:
		try:
			f = open(self.file_name, "a")
			try:
				for key, value in msg.items():
					f.write("[{key}]\n".format(key=key.upper()))
					f.write(value + '\n\n')
				f.write(Log.divide_line+'\n')
			except:
				print("[ERROR: WRITE FILE FAILED (main)]")
		except:
			print("[ERROR: OPEN FILE FAILED (main)]")
		finally:
			f.close()
		return None
	
	def log_error(self, msg) -> None:
		try:
			f = open(self.file_name, "a")
			try:
				f.write(msg+'\n\n')
			except:
				print("[ERROR: WRITE FILE FAILED (error)]")
		except:
			print("[ERROR: OPEN FILE FAILED (error)]")
		else:
			f.close()
		return None

def read_exec(url) -> {}:
	res = []
	data = pd.read_excel(url)
	print(data)
	for index, row in data.iterrows():
		building = {}
		building['building_name'] = row['Building name']
		building['building_number'] = row['No']
		building['url'] = row['url']
		res.append(building)
	return res