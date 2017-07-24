import ast
import assembler_handler

def mainFunction(filenames):
    # filenames = ["file1.txt","file2.txt","file3.txt"]
    literal_names = {}
    symbol_names = {}
    extern_names = {}
    relocation_names = {}
    program_lengths = []
    linked_code = []
    linked_code2 = []
    program_lengths.append(0)

    assembler_handler.assemble_mult_file(filenames)

    def generate_code(counter,string):
        linked_code.append("#" + str(counter) + "\t" + string)


    for file in filenames:
        f = open("./Output/"+file+"_tables.asm", 'r')
        data = f.read()
        f.close()
        lines = data.splitlines()

        symbol_names[file] = ast.literal_eval(lines[0])
        literal_names[file] = ast.literal_eval(lines[1])
        relocation_names[file] = ast.literal_eval(lines[2])
        extern_names[file] = ast.literal_eval(lines[3])
        program_lengths.append(int(lines[4]))

    arr1 = []
    aar2 = []
    filecount = 0
    for file in filenames:
        f = open("./Output/"+file+"_pass1.asm",'r')
        data = f.read()
        f.close()
        lines = data.splitlines()

        f = open("./Output/"+file+"_pass2.asm",'r')
        data = f.read()
        f.close()
        lines2 = data.splitlines()

        for i in range(len(lines)):
            elements1 = lines[i].strip().split("\t")
            elements2 = lines2[i].strip().split("\t")
            mem_location = int(elements1[0][1:])
            string = ""
            element1 = elements1[-1]

            if(mem_location in relocation_names[file]):
                address = 0
                if(element1 in symbol_names[file].keys()):
                    address = int(symbol_names[file][element1])
                    if(element1 in extern_names[file]):
                        for k in range(0,filecount,1):
                            st = filenames[k].upper()+"_"+element1
                            if st in symbol_names[filenames[k]].keys():
                                address = int(symbol_names[filenames[k]][st])
                    else:
                        address += program_lengths[filecount]
                elif(element1 in literal_names[file].keys()):
                    address = int(literal_names[file][element1])
                    address += program_lengths[filecount]

                for j in range(1,len(elements1)-1,1):
                    string += "\t"+elements1[j]
                string+="\t"+str(address)
                generate_code(mem_location+program_lengths[filecount],string)
            else:
                for j in range(1,len(elements2)):
                    string += "\t"+elements2[j]
                generate_code(mem_location + program_lengths[filecount],string)

                if (element1 in literal_names[file].keys()):
                    addr = int(literal_names[file][element1])
                    addr += program_lengths[filecount]
            s =""
            for l in range(1, len(elements1)):
                s += "\t" + elements1[l]
            linked_code2.append("#" + str(mem_location + program_lengths[filecount]) + "\t" + s.strip())

        for key in symbol_names[file].keys():
            symbol_names[file][key] += program_lengths[filecount]
        filecount += 1



    f = open("./Output/" + filenames[0] + "_pass1.link", 'w')
    print("PASS 1 LINKED")
    for item in linked_code2:
        f.write(item+"\n")
    f.close()

    f = open("./Output/" + filenames[0] + "_pass2.link", 'w')
    print("PASS 2 LINKED")
    for item in linked_code:
        f.write(item+"\n")
    f.close()
    return linked_code

