def to_sec(t):
	temp = t.rstrip("s").split("m")
	s = 60*int(temp[0]) + float(temp[1])
	return s

if __name__ == "__main__":
	while (1):
		t = input("> ")
		if t == "stop":
			break
		print(to_sec(t))
