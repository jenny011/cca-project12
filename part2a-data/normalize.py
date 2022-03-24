import csv

if __name__ == "__main__":
	i=0
	output = []
	with open("./part2a-sec.csv", "r") as f:
		preader = csv.reader(f, delimiter=",")
		for row in preader:
			if i == 0:
				output.append(row)
			else:
				for i in range(1,len(row)):
					row[i] = float(row[i])
				for i in range(2, len(row)):
					row[i] = "{:.2f}".format(row[i]/row[1])
				row[1] = "1.00"
				output.append(row)
			i += 1
	with open("./part2a-normalized.csv", "w") as f:
		pwriter = csv.writer(f, delimiter=",")
		for row in output:
			pwriter.writerow(row)

