import query
import utilities as util

loc = "Parkville"

def main() -> None:
	log_handler = util.Log(loc)
	# loop all the building
	q1 = query.Query(log_handler, "Wilson Hall")
	q1.execute()
	return None

if __name__ == "__main__":
	main()