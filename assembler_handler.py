import assembler
import macro

operand_table = {}
f=open('opcode.txt','r')
data=f.read()
f.close()
lines = data.splitlines()

for line in lines:
    line = line.split(' ')
    operand_table[line[0]] = (line[1],int(line[2]))

pass1_codes={}
pass2_codes={}
symbol_tables={}
literal_tables={}

def assemble_mult_file(files):

    for file in files:
        macro.macrogen(file)
        f = open("./Output/"+file+"_pass1.asm",'w')
        symbol_table, literal_table, extenal_varibles, relocation_table,pass1_code, pass2_code,counter \
            = assembler.get_results(file,operand_table)

        pass1_codes[file] = pass1_code
        pass2_codes[file] = pass2_code
        symbol_tables[file] = symbol_table
        literal_tables[file] = literal_table

        print(symbol_table)
        print(literal_table)
        print(extenal_varibles)
        print(relocation_table)
        print(pass1_code)
        print(pass2_code)
        print(counter)

        for item in pass1_code:
            f.write(item + "\n")
        f.close()

        f = open("./Output/" + file + "_pass2.asm", 'w')
        print("\n\nPASS 2: "+file)
        for item in pass2_code:
            f.write(item + "\n")
        f.close()
        f = open("./Output/" + file + "_tables.asm", 'w')
        print("SYMBOL TABLE: " + file)
        f.write(str(symbol_table))
        f.write("\n")
        print("LITERAL TABLE: " + file)
        f.write(str(literal_table))
        f.write("\n")
        print("RELOCATION TABLE: "+file)
        f.write(str(relocation_table))
        f.write("\n")
        print("EXTERN TABLE: "+file)
        f.write(str(extenal_varibles))
        f.write("\n")
        f.write(str(counter))
        # return symbol_table, literal_table, extenal_varibles, relocation_table,pass1_code, pass2_code,counter
    return pass1_codes, pass2_codes, symbol_tables, literal_tables

        # assemble_mult_file(['file1','file2','file3'])
