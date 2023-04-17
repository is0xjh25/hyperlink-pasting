import query as q
def main() -> None:
	q1 = q.Query("Wilson Hall")
	res = q1.find_way_id()
	q1.read_way()
	return None

if __name__ == "__main__":
	main()