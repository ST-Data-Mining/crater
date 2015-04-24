import pdb,sys
name = "./result/0216/myresult10"

out = ""

def each(out, f):
	f.readline()
	f.readline()
	while True:
		line = f.readline()
		if "Y-Def" in line:
			out += " & "+line[6:20].strip().replace("_","\_") +" & "+line[30:37].strip() +" & "+line[40:47].strip() 
			# out += " & \quart"+"{"+float(line[88:92].strip())*100 +"}{"+float(line[95:99].strip())*100 +"}{"+float(line[102:106].strip())*100+"}"+"\\\\" +"\n"
			# pdb.set_trace()
			out += " & \quart"+"{"+str(float(line[88:92].strip())*100) +"}{"+str(line[40:47].strip())+"}{"+str(float(line[95:99].strip())*100)+"}"+"\\\\" +"\n"

		if "Def" not in line:
			break
	return out

def onlyg(out, f):
	f.readline()
	f.readline()
	while True:
		line = f.readline()
		if "Y-Def" in line:
		  out +=line
		if "Def" not in line:
			break
	return out

def IQR(funnname):
	if "Dataset:" in line:
		 # out += "\\rowcolor[gray]{.9}"+line[9:line.find("\n")]
		 out += "***"+line[9:line.find("\n")]+"***\n"
	if "*g*" in line:
		out+= "```\n"+line
		out = onlyg(out, f)+"```\n"


def main(funname, filename):
	f = open(filename)
	while True:
		line = f.readline()
		if "Dataset:" in line:
			 # out += "\\rowcolor[gray]{.9}"+line[9:line.find("\n")]
			 out += "***"+line[9:line.find("\n")]+"***\n"
		if "*g*" in line:
			out+= "```\n"+line
			out = onlyg(out, f)+"```\n"
		if not line:
			break
	f.close()
	f = open(filename+'latex', 'w')
	f.write(out+'\n')
	f.close()
	print out


if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2])




