f = open("./opcode.txt", 'r')
data = f.read()
f.close()
lines = data.splitlines()
optab = {}

for line in lines:
    line = line.strip().split()
    opcode = str(line[0])
    optab[opcode] = int(line[2])


mem_locations_instr = {}
gen_per_reg = {'Acc': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'H': 0, 'L': 0}
flags = {'LE': 0, 'GE': 0, 'Eq': 0, 'S': 0, 'LT': 0, 'GT': 0}

# def loader():
#     for line in lines:
#         p = line.split("\t")
#         mem_locations_instr[p[0][1]] = p[]

ins = []
def simulate(filename):
    f = open("./Output/a.c_pass2.link", 'r')
    data = f.read()
    f.close()
    lines = data.splitlines()
    global optab,mem_locations_instr,gen_per_reg,flags
    pc = 0
    outputs = []
    i = 0
    currins = ""
    f = open("./Output/output_sim.link", 'w')
    f2 = open("./Output/output_lines.link",'w')
    while i < len(lines):
        element1 = lines[i].strip().split("\t")
        print(i)
        currins = lines[i]
        ins.append(lines[i]+"\n")        
        temp_instr = ""
        for j in range(2,len(element1)):
            temp_instr += element1[j] +" "
        instr = temp_instr
        mem_location = int(element1[0][1:])
        pc = mem_location

        if "DS" in element1:
            mem_locations_instr[mem_location] = int(element1[4])
        elif element1[2].startswith("START"):
            mem_locations_instr[mem_location] = (element1[2])
        elif "STOP" in element1 :
            print("asdasdasd"+str(mem_location))
            mem_locations_instr[mem_location] = "STOP"
        elif element1[2].startswith('='):
            temp_literal = element1[2].strip('=')
            temp_literal = temp_literal.strip("'")
            mem_locations_instr[mem_location] = int(temp_literal)
        elif element1[2] == "LDA":
            mem_locations_instr[mem_location] = "LDA"
            mem_locations_instr[mem_location+1] = int(element1[3])
            gen_per_reg['Acc'] = mem_locations_instr[int(element1[3])]
            # print(Gen_per_reg)
        elif element1[2] == "STA":
            mem_locations_instr[mem_location] = "STA"
            mem_locations_instr[mem_location+1] = element1[3]
            mem_locations_instr[int(element1[3])] = int(gen_per_reg['Acc'])
            # print(mem_locations_instr)
        elif element1[2] == "COMPI":
            mem_locations_instr[mem_location] = "COMPI"
            mem_locations_instr[mem_location + 1] = element1[3]
            if gen_per_reg['Acc'] == mem_locations_instr[int(element1[3])]:
                flags['Eq'] = 1
                flags['GE'] = 1
                flags['LE'] = 1
                flags['LT'] = 0
                flags['GT'] = 0
                flags['S'] = 0
            elif gen_per_reg['Acc'] < mem_locations_instr[int(element1[3])]:
                flags['Eq'] = 0
                flags['GE'] = 0
                flags['LE'] = 1
                flags['LT'] = 1
                flags['GT'] = 0
                flags['S'] = 1
            elif gen_per_reg['Acc'] > mem_locations_instr[int(element1[3])]:
                flags['Eq'] = 0
                flags['GE'] = 1
                flags['LE'] = 0
                flags['LT'] = 0
                flags['GT'] = 1
                flags['S'] = 0
        elif element1[2] == "COMP":
            mem_locations_instr[mem_location] = "COMP"
            if gen_per_reg['Acc'] == gen_per_reg['F'] :
                flags['Eq'] = 1
                flags['GE'] = 1
                flags['LE'] = 1
                flags['LT'] = 0
                flags['GT'] = 0
                flags['S'] = 0
            elif gen_per_reg['Acc'] < gen_per_reg['F']:
                flags['Eq'] = 0
                flags['GE'] = 0
                flags['LE'] = 1
                flags['LT'] = 1
                flags['GT'] = 0
                flags['S'] = 1
            elif gen_per_reg['Acc'] > gen_per_reg['F']:
                flags['Eq'] = 0
                flags['GE'] = 1
                flags['LE'] = 0
                flags['LT'] = 0
                flags['GT'] = 1
                flags['S'] = 0
        elif element1[2] == "COMPRI":
            mem_locations_instr[mem_location] = "COMPRI"
            mem_locations_instr[mem_location + 1] = element1[4]
            if gen_per_reg['D'] == mem_locations_instr[int(element1[4])]:
                flags['Eq'] = 1
                flags['GE'] = 1
                flags['LE'] = 1
                flags['LT'] = 0
                flags['GT'] = 0
                flags['S'] = 0
            elif gen_per_reg['D'] < mem_locations_instr[int(element1[4])]:
                flags['Eq'] = 0
                flags['GE'] = 0
                flags['LE'] = 1
                flags['LT'] = 1
                flags['GT'] = 0
                flags['S'] = 1
            elif gen_per_reg['D'] > mem_locations_instr[int(element1[4])]:
                flags['Eq'] = 0
                flags['GE'] = 1
                flags['LE'] = 0
                flags['LT'] = 0
                flags['GT'] = 1
                flags['S'] = 0
        elif element1[2] == "BC":
            if element1[3] == "GE":
                mem_locations_instr[mem_location] = "BC GE"
                mem_locations_instr[mem_location + 1] = int(element1[4])
                if flags['GE'] == 1:
                    if(mem_location < int(element1[4])):
                        temp = mem_location
                        print(temp, element1[4])

                        while(temp!=int(element1[4])):
                            print(i,temp,element1[4])
                            i += 1
                            temp_element1 = lines[i].strip().split("\t")
                            temp = int(temp_element1[0][1:])
                        i -= 1
                        print(i, temp, element1[4])
                    else:
                        temp = mem_location
                        print(temp, element1[4])

                        while (temp != int(element1[4])):
                            print(i, temp, element1[4])
                            i -= 1
                            temp_element1 = lines[i].strip().split("\t")
                            temp = int(temp_element1[0][1:])
                        i -= 1
                        print(i, temp, element1[4])

        # i += 1
            elif element1[3] == "LE":
                mem_locations_instr[mem_location] = "BC LE"
                mem_locations_instr[mem_location + 1] = int(element1[4])
                if flags['LE'] == 1:
                    if (mem_location < int(element1[4])):
                        temp = mem_location
                        print(temp, element1[4])

                        while (temp != int(element1[4])):
                            print(i, temp, element1[4])
                            i += 1
                            temp_element1 = lines[i].strip().split("\t")
                            temp = int(temp_element1[0][1:])
                        i -= 1
                        print(i, temp, element1[4])
                    else:
                        temp = mem_location
                        print(temp, element1[4])

                        while (temp != int(element1[4])):
                            print(i, temp, element1[4])
                            i -= 1
                            temp_element1 = lines[i].strip().split("\t")
                            temp = int(temp_element1[0][1:])
                        i -= 1
                        print(i, temp, element1[4])
        elif element1[2] == "ADDI":
            mem_locations_instr[mem_location] = "ADDI"
            mem_locations_instr[mem_location + 1] = int(element1[3])
            gen_per_reg['Acc'] += mem_locations_instr[int(element1[3])]
            if gen_per_reg['Acc'] > 0:
                flags['Eq'] = 0
                flags['GE'] = 1
                flags['LE'] = 0
                flags['LT'] = 0
                flags['GT'] = 1
                flags['S'] = 0
            elif gen_per_reg['Acc'] < 0:
                flags['Eq'] = 0
                flags['GE'] = 0
                flags['LE'] = 1
                flags['LT'] = 1
                flags['GT'] = 0
                flags['S'] = 1
            elif gen_per_reg['Acc'] == 0:
                flags['Eq'] = 1
                flags['GE'] = 1
                flags['LE'] = 1
                flags['LT'] = 0
                flags['GT'] = 0
                flags['S'] = 0
        elif element1[2] == "ADDM":
            mem_locations_instr[mem_location] = "ADDM"
            mem_locations_instr[mem_location + 1] = int(element1[3])
            gen_per_reg['Acc'] += mem_locations_instr[int(element1[3])]
            if gen_per_reg['Acc'] > 0:
                flags['Eq'] = 0
                flags['GE'] = 1
                flags['LE'] = 0
                flags['LT'] = 0
                flags['GT'] = 1
                flags['S'] = 0
            elif gen_per_reg['Acc'] < 0:
                flags['Eq'] = 0
                flags['GE'] = 0
                flags['LE'] = 1
                flags['LT'] = 1
                flags['GT'] = 0
                flags['S'] = 1
            elif gen_per_reg['Acc'] == 0:
                flags['Eq'] = 1
                flags['GE'] = 1
                flags['LE'] = 1
                flags['LT'] = 0
                flags['GT'] = 0
                flags['S'] = 0
        elif element1[2] == "MULI":
            mem_locations_instr[mem_location] = "MULI"
            mem_locations_instr[mem_location + 1] = int(element1[3])
            gen_per_reg['Acc'] *= mem_locations_instr[int(element1[3])]
            if gen_per_reg['Acc'] > 0:
                flags['Eq'] = 0
                flags['GE'] = 1
                flags['LE'] = 0
                flags['LT'] = 0
                flags['GT'] = 1
                flags['S'] = 0
            elif gen_per_reg['Acc'] < 0:
                flags['Eq'] = 0
                flags['GE'] = 0
                flags['LE'] = 1
                flags['LT'] = 1
                flags['GT'] = 0
                flags['S'] = 1
            elif gen_per_reg['Acc'] == 0:
                flags['Eq'] = 1
                flags['GE'] = 1
                flags['LE'] = 1
                flags['LT'] = 0
                flags['GT'] = 0
                flags['S'] = 0
        elif element1[2] == "MULM":
            mem_locations_instr[mem_location] = "MULM"
            mem_locations_instr[mem_location + 1] = int(element1[3])
            gen_per_reg['Acc'] *= mem_locations_instr[int(element1[3])]
            if gen_per_reg['Acc'] > 0:
                flags['Eq'] = 0
                flags['GE'] = 1
                flags['LE'] = 0
                flags['LT'] = 0
                flags['GT'] = 1
                flags['S'] = 0
            elif gen_per_reg['Acc'] < 0:
                flags['Eq'] = 0
                flags['GE'] = 0
                flags['LE'] = 1
                flags['LT'] = 1
                flags['GT'] = 0
                flags['S'] = 1
            elif gen_per_reg['Acc'] == 0:
                flags['Eq'] = 1
                flags['GE'] = 1
                flags['LE'] = 1
                flags['LT'] = 0
                flags['GT'] = 0
                flags['S'] = 0
        elif element1.__len__() >= 4 and element1[3] == "DCR":
            mem_locations_instr[mem_location] = "DCR"
            gen_per_reg['D'] -= 1
        elif element1[2] == "MOVER":
            mem_locations_instr[mem_location] = "MOVER"
            mem_locations_instr[mem_location + 1] = int(element1[4])
            gen_per_reg['F'] = mem_locations_instr[int(element1[4])]
        elif element1[2] == "MOVI":
            mem_locations_instr[mem_location] = "MOVI"
            mem_locations_instr[mem_location + 1] = int(element1[4])
            gen_per_reg['D'] = mem_locations_instr[int(element1[4])]
        
        f.write(str(mem_locations_instr)+"\n")
        f2.write(str(currins)+"\n")
        outputs.append(mem_locations_instr)
        i += 1


    # print("\n\n\n\nHo gaya")
    # for k,v in mem_locations_instr.items():
    #     print(k,v)
    # # print(Gen_per_reg)
    # print(mem_locations_instr)
    print(outputs)
    return mem_locations_instr,gen_per_reg,flags,ins,outputs