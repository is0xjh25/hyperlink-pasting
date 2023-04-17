import query as q
def main() -> None:
	q1 = q.Query("Wilsonasdqwe Hall")
	res = q1.find_way_id()
	return None

if __name__ == "__main__":
	main()