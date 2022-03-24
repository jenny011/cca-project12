import csv

def to_sec(t):
	temp = t.rstrip("s").split("m")
	s = 60*int(temp[0]) + float(temp[1])
	return s

if __name__ == "__main__":
	i=0
	output = []
	with open("./part2b-sec.csv", "r") as f:
		preader = csv.reader(f, delimiter=",")
		for row in preader:
			if i == 0:
				output.append(row)
			else:
				for i in range(1,len(row)):
					if row[i]:
						row[i] = float(row[i])
				for i in range(2,len(row)):
					if row[i]:
						row[i] = "{:.2f}".format(row[1]/row[i])
				row[1] = "1.00"
				output.append(row)
			i += 1
	with open("./part2b-normalized.csv", "w") as f:
		pwriter = csv.writer(f, delimiter=",")
		for row in output:
			pwriter.writerow(row)

