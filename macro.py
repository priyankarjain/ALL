import os

def macrogen(fileName):
	lineNum = 0
	macrotable = {}
	macroname = ""

	# fileName = "macrotxt.c"
	newFile = open('tempText.c','w')
	currFile = open(fileName,'r')

	for line in currFile.readlines():
		lineNum +=1
		tokens = line.split()

		macroFound = False
		if len(tokens)>0 and tokens[0] == "#define":
			header = tokens[1].split()
			macroname = header[0]
			parameters = tokens[2].lstrip('(').rstrip(')').split(',')
			lines = tokens[3].lstrip('{').rstrip('}').rstrip(';').split(';')
			details = {}
			details["para"] = parameters
			details["lines"] = lines
			details["name"]  = macroname
			macrotable[macroname] = details
			print(lines)
			print(macroname)
			print(parameters)
			continue


		for macroname in macrotable.keys():
			if macroname != "" and line.find(macroname) != -1:
				macroFound = True
				print("Line: ", line)
				tokensInline = line.split()
				for token in tokensInline:

					if token.find(macroname) != -1:
						mac_detail = macrotable[macroname]
						mac_statments = mac_detail["lines"]
						mac_para = mac_detail["para"]
						temp = token.split('(')[1].rstrip(';').rstrip(')')
						print(temp)
						# print(temp)

						paras = temp.rstrip(')').split(',')
						print(paras)
						for statement in mac_statments:
							for i in range(len(paras)):
								para =  paras[i]
								fpara = mac_para[i]
								statement = statement.replace(fpara, para)
								print(statement,fpara, para)
								i+=1
							newFile.write(statement+"\n")
				print(mac_statments)
				continue
		
		if(not macroFound):		
			newFile.write(line)
	
	currFile.close()
	newFile.close()
	os.remove(fileName)
	os.rename('tempText.c', fileName)