import re
import CONSTANTS

assign=re.compile('var(.*?)=(.*)')
arith=re.compile('(.*?)=(.*?)[\+\-\*](.*?)')
arith_add=re.compile('(.*?)=(.*?)\+(.*)')
arith_mul=re.compile('(.*?)=(.*?)\*(.*)')
arith_sub=re.compile('(.*?)=(.*?)\-(.*)')

symbol_table = {}
operand_table = {}
literal_table = {}
extenal_varibles = {}
pass1_code = []
pass2_code = []
relocation_table = []
counter = 0
counterEndIf = -1
counterif = 0
counterloop = 0
endiftoggle = 0

def reset():
    global symbol_table,operand_table,literal_table,extenal_varibles,pass1_code,pass2_code,relocation_table
    global  counter,counterloop,counterif,counterEndIf

    symbol_table = {}
    operand_table = {}
    literal_table = {}
    extenal_varibles = {}
    pass1_code = []
    pass2_code = []
    relocation_table = []
    counter = 0
    counterEndIf = -1
    counterif = 0
    counterloop = 0

def generate_code(counter,string):
    global endiftoggle
    if endiftoggle == 1 :
        pass1_code.append("#"+str(counter)  + "\t"+"ENDIF"+str(counterif)+ "\t" + string)
        endiftoggle = 0
    else:
        pass1_code.append("#" + str(counter) + "\t" + string)

def generate_start_code():
    global counter
    generate_code(counter, CONSTANTS.START)
    counter+=1

def generate_stop_code():
    global counter
    generate_code(counter, CONSTANTS.STOP)
    counter+=1

def check_extern(var_name,filename):
    if(var_name in extenal_varibles.keys()):
        return True
    return False

def assign_var_name(var_name,filename):
    if check_extern(var_name, filename):
        new_var_name = var_name
    else:
        new_var_name = filename.upper() + "_" + var_name
    return new_var_name

def assemble_file(filename):
    global  counter
    global  counterloop
    global counterif
    global counterEndIf
    global endiftoggle
    relocation_counter = 0
    endiftoggle = 0
    f = open(filename,'r')
    data=f.read()
    f.close()
    datalines = data.splitlines()

    for line in datalines:
        line = line.strip()
        if(assign.match(line)):
            line = line.strip('var')
            a = re.search(r'(.*)=(.*)',line)
            var_name = assign_var_name(a.group(1).strip().upper(),filename)
            var_value = a.group(2).strip()
            string = var_name+"\t"+CONSTANTS.DS+"\t"+var_value
            symbol_table[var_name] = counter
            generate_code(counter,string)
            counter += int(operand_table['DS'][1])
        elif(arith.match(line)):
            a = re.search(r'(.*)=(.*)[\+\*\-](.*)',line)
            if(arith_add.match(line)):
                var_name1 = assign_var_name(a.group(1).strip().upper(),filename)
                var_name2 = assign_var_name(a.group(2).strip().upper(),filename)

                if(var_name1 == var_name2):
                    if(a.group(3).strip().isdecimal()):
                        lit_name = "=\'"+a.group(3).strip()+"\'"
                        literal_table[lit_name] = counter
                        generate_code(counter,lit_name)
                        counter +=1

                        string =CONSTANTS.LDA+"\t"+ var_name1.upper()
                        generate_code(counter,string)
                        relocation_table.append(counter)
                        relocation_counter += 1
                        counter += int(operand_table['LDA'][1])

                        string = CONSTANTS.ADDI+"\t"+lit_name
                        generate_code(counter,string)
                        relocation_table.append(counter)
                        relocation_counter += 1
                        counter += int(operand_table['ADDI'][1])

                        string = CONSTANTS.STA+"\t"+var_name1.upper()
                        generate_code(counter,string)
                        relocation_table.append(counter)
                        relocation_counter += 1
                        counter += int(operand_table['STA'][1])

                    else:
                        var_name3 = assign_var_name(a.group(3).strip().upper(), filename)
                        string = CONSTANTS.LDA + "\t" + var_name1.upper()
                        generate_code(counter, string)
                        relocation_table.append(counter)
                        relocation_counter += 1
                        counter += int(operand_table['LDA'][1])

                        string = CONSTANTS.ADDM + "\t" + var_name3.upper()
                        generate_code(counter, string)
                        relocation_table.append(counter)
                        relocation_counter += 1
                        counter += int(operand_table['ADDM'][1])

                        string = CONSTANTS.STA+"\t"+var_name1.upper()
                        generate_code(counter,string)
                        relocation_table.append(counter)
                        relocation_counter += 1
                        counter += int(operand_table['STA'][1])

                else:
                    #var_name3 = filename.upper()+"_"+ a.group(3).strip().upper()
                    var_name3 = assign_var_name(a.group(3).strip().upper(), filename)
                    string = CONSTANTS.LDA + "\t" + var_name2.upper()
                    generate_code(counter, string)
                    relocation_table.append(counter)
                    relocation_counter += 1
                    counter += int(operand_table['LDA'][1])

                    string = CONSTANTS.ADDM + "\t" + var_name3.upper()
                    generate_code(counter, string)
                    relocation_table.append(counter)
                    relocation_counter += 1
                    counter += int(operand_table['ADDM'][1])

                    string = CONSTANTS.STA + "\t" + var_name1.upper()
                    generate_code(counter, string)
                    relocation_table.append(counter)
                    relocation_counter += 1
                    counter += int(operand_table['STA'][1])

            elif(arith_mul.match(line)):
                var_name1 = assign_var_name(a.group(1).strip().upper(),filename)
                var_name2 = assign_var_name(a.group(2).strip().upper(),filename)
                # var_name2 = filename.upper()+"_"+  a.group(2).strip()
                if (var_name1 == var_name2):
                    if (a.group(3).strip().isdecimal()):
                        lit_name = "=\'" + a.group(3).strip() + "\'"
                        literal_table[lit_name] = counter
                        generate_code(counter, lit_name)
                        counter += 1

                        string = CONSTANTS.LDA + "\t" + var_name1.upper()
                        generate_code(counter, string)
                        relocation_table.append(counter)
                        relocation_counter += 1
                        counter += int(operand_table['LDA'][1])

                        string = CONSTANTS.MULI + "\t" + lit_name
                        generate_code(counter, string)
                        relocation_table.append(counter)
                        relocation_counter += 1
                        counter += int(operand_table['MULI'][1])

                        string = CONSTANTS.STA + "\t" + var_name1.upper()
                        generate_code(counter, string)
                        relocation_table.append(counter)
                        relocation_counter += 1
                        counter += int(operand_table['STA'][1])

                    else:
                        var_name3 = assign_var_name(a.group(3).strip().upper(), filename)
                        string = CONSTANTS.LDA + "\t" + var_name1.upper()
                        generate_code(counter, string)
                        relocation_table.append(counter)
                        relocation_counter += 1
                        counter += int(operand_table['LDA'][1])

                        string = CONSTANTS.MULM + "\t" + var_name3.upper()
                        generate_code(counter, string)
                        relocation_table.append(counter)
                        relocation_counter += 1
                        counter += int(operand_table['MULM'][1])

                        string = CONSTANTS.STA + "\t" + var_name1.upper()
                        generate_code(counter, string)
                        relocation_table.append(counter)
                        relocation_counter += 1
                        counter += int(operand_table['STA'][1])

                else:
                    var_name3 = assign_var_name(a.group(3).strip().upper(),filename)
                    # var_name3 = filename.upper()+"_"+ a.group(3).strip().upper()
                    string = CONSTANTS.LDA + "\t" + var_name2.upper()
                    generate_code(counter, string)
                    relocation_table.append(counter)
                    relocation_counter += 1
                    counter += int(operand_table['LDA'][1])

                    string = CONSTANTS.MULM + "\t" + var_name3.upper()
                    generate_code(counter, string)
                    relocation_table.append(counter)
                    relocation_counter += 1
                    counter += int(operand_table['MULM'][1])

                    string = CONSTANTS.STA + "\t" + var_name1.upper()
                    generate_code(counter, string)
                    relocation_table.append(counter)
                    relocation_counter += 1
                    counter += int(operand_table['STA'][1])

            elif(arith_sub.match(line)):
                var_name1 = assign_var_name(a.group(1).strip().upper(), filename)
                var_name2 = assign_var_name(a.group(2).strip().upper(), filename)
                if (var_name1 == var_name2):
                    if (a.group(3).strip().isdecimal()):
                        lit_name = "=\'" + a.group(3).strip() + "\'"
                        literal_table[lit_name] = counter
                        generate_code(counter, lit_name)
                        counter += 1

                        string = CONSTANTS.LDA + "\t" + var_name1.upper()
                        generate_code(counter, string)
                        relocation_table.append(counter)
                        relocation_counter += 1
                        counter += int(operand_table['LDA'][1])

                        string = CONSTANTS.SUBI + "\t" + lit_name
                        generate_code(counter, string)
                        relocation_table.append(counter)
                        relocation_counter += 1
                        counter += int(operand_table['SUBI'][1])

                        string = CONSTANTS.STA + "\t" + var_name1.upper()
                        generate_code(counter, string)
                        relocation_table.append(counter)
                        relocation_counter += 1
                        counter += int(operand_table['STA'][1])

                    else:
                        var_name3 = assign_var_name(a.group(3).strip().upper(), filename)
                        string = CONSTANTS.LDA + "\t" + var_name1.upper()
                        generate_code(counter, string)
                        relocation_table.append(counter)
                        relocation_counter += 1
                        counter += int(operand_table['LDA'][1])

                        string = CONSTANTS.SUBM + "\t" + var_name3.upper()
                        generate_code(counter, string)
                        relocation_table.append(counter)
                        relocation_counter += 1
                        counter += int(operand_table['SUBM'][1])

                        string = CONSTANTS.STA + "\t" + var_name1.upper()
                        generate_code(counter, string)
                        relocation_table.append(counter)
                        relocation_counter += 1
                        counter += int(operand_table['STA'][1])

                else:
                    var_name3 = assign_var_name(a.group(3).strip().upper(), filename)
                    string = CONSTANTS.LDA + "\t" + var_name2.upper()
                    generate_code(counter, string)
                    relocation_table.append(counter)
                    relocation_counter += 1
                    counter += int(operand_table['LDA'][1])

                    string = CONSTANTS.SUBM + "\t" + var_name3.upper()
                    generate_code(counter, string)
                    relocation_table.append(counter)
                    relocation_counter += 1
                    counter += int(operand_table['SUBM'][1])

                    string = CONSTANTS.STA + "\t" + var_name1.upper()
                    generate_code(counter, string)
                    relocation_table.append(counter)
                    relocation_counter += 1
                    counter += int(operand_table['STA'][1])
        elif(line.startswith('if')):
            condition = line[2:].strip()
            if ('>' in condition):
                variables = re.search(r'(.*?)>(.*)',condition)
                var_name1 = assign_var_name(variables.group(1).strip().upper(),filename)
                var_name2 = variables.group(2).strip()
                if(var_name2.isnumeric()):
                    string = CONSTANTS.LDA + "\t" + var_name1.upper()
                    generate_code(counter, string)
                    relocation_table.append(counter)
                    relocation_counter += 1
                    counter += int(operand_table['LDA'][1])

                    lit_name = "=\'" + var_name2 + "\'"
                    literal_table[lit_name] = counter
                    generate_code(counter, lit_name)
                    counter += 1

                    string = CONSTANTS.COMPI+"\t"+lit_name
                    generate_code(counter,string)
                    relocation_table.append(counter)
                    relocation_counter += 1
                    counter += int(operand_table['COMPI'][1])

                    string = CONSTANTS.BC+"\t"+"LE"
                    counterEndIf = len(pass1_code)
                    generate_code(counter,string)
                    relocation_table.append(counter)
                    relocation_counter += 1
                    counter += int(operand_table['BC'][1])
                    counterif +=1
                else:
                    var_name2 = assign_var_name(variables.group(2).strip().upper(),filename)
                    string = CONSTANTS.LDA + "\t" + var_name1.upper()
                    generate_code(counter, string)
                    relocation_table.append(counter)
                    counter += int(operand_table['LDA'][1])


                    string = CONSTANTS.MOVER + "\t"+"F_REG" + "\t" + var_name2.upper()
                    generate_code(counter, string)
                    relocation_table.append(counter)
                    relocation_counter += 1
                    counter += int(operand_table['MOVER'][1])

                    string = CONSTANTS.COMP + "\t" + "F_REG"
                    generate_code(counter, string)
                    counter += int(operand_table['COMP'][1])

                    string = CONSTANTS.BC + "\t" + "LE"
                    counterEndIf = len(pass1_code)
                    generate_code(counter, string)
                    relocation_table.append(counter)
                    relocation_counter += 1
                    counter += int(operand_table['BC'][1])
                    counterif += 1
            if ('<' in condition):
                variables = re.search(r'(.*?)<(.*)',condition)
                var_name1 = assign_var_name(variables.group(1).strip().upper(), filename)
                var_name2 = variables.group(2).strip()
                if(var_name2.isnumeric()):
                    string = CONSTANTS.LDA + "\t" + var_name1.upper()
                    generate_code(counter, string)
                    relocation_table.append(counter)
                    relocation_counter += 1
                    counter += int(operand_table['LDA'][1])

                    lit_name = "=\'" + var_name2 + "\'"
                    literal_table[lit_name] = counter
                    generate_code(counter, lit_name)
                    counter += 1

                    string = CONSTANTS.COMPI+"\t"+lit_name
                    generate_code(counter,string)
                    relocation_table.append(counter)
                    counter += int(operand_table['COMPI'][1])

                    string = CONSTANTS.BC+"\t"+"GE"
                    counterEndIf = len(pass1_code)
                    generate_code(counter,string)
                    relocation_table.append(counter)
                    relocation_counter += 1
                    counter += int(operand_table['BC'][1])
                    counterif +=1
                else:
                    var_name2 = assign_var_name(variables.group(2).strip().upper(), filename)
                    string = CONSTANTS.LDA + "\t" + var_name1.upper()
                    generate_code(counter, string)
                    relocation_table.append(counter)
                    relocation_counter += 1
                    counter += int(operand_table['LDA'][1])

                    string = CONSTANTS.MOVER + "\t"+"REG_F"+"\t" + var_name2.upper()
                    generate_code(counter, string)
                    relocation_table.append(counter)
                    relocation_counter += 1
                    counter += int(operand_table['MOVER'][1])

                    string = CONSTANTS.COMP + "\t" + "REG_F"
                    generate_code(counter, string)
                    counter += int(operand_table['COMP'][1])

                    string = CONSTANTS.BC + "\t" + "GE"
                    counterEndIf = len(pass1_code)
                    generate_code(counter, string)
                    relocation_table.append(counter)
                    relocation_counter += 1
                    counter += int(operand_table['BC'][1])
                    counterif += 1
            if ('==' in condition):
                variables = re.search(r'(.*?)\=\=(.*)',condition)
                var_name1 = assign_var_name(variables.group(1).strip().upper(), filename)
                var_name2 = variables.group(2).strip()
                if(var_name2.isnumeric()):
                    string = CONSTANTS.LDA + "\t" + var_name1.upper()
                    generate_code(counter, string)
                    relocation_table.append(counter)
                    relocation_counter += 1
                    counter += int(operand_table['LDA'][1])

                    lit_name = "=\'" + var_name2 + "\'"
                    literal_table[lit_name] = counter
                    generate_code(counter, lit_name)
                    counter += 1

                    string = CONSTANTS.COMPI+"\t"+lit_name
                    generate_code(counter,string)
                    relocation_table.append(counter)
                    counter += int(operand_table['COMPI'][1])

                    string = CONSTANTS.BC+"\t"+"E"
                    counterEndIf = len(pass1_code)
                    generate_code(counter,string)
                    relocation_table.append(counter)
                    counter += int(operand_table['BC'][1])
                    counterif +=1
                else:
                    var_name2 = assign_var_name(variables.group(2).strip().upper(), filename)
                    string = CONSTANTS.LDA + "\t" + var_name1.upper()
                    generate_code(counter, string)
                    relocation_table.append(counter)
                    relocation_counter += 1
                    counter += int(operand_table['LDA'][1])

                    string = CONSTANTS.MOVER  +"\t"+"REG_F"+ "\t" + filename.upper()+"_"+ var_name2.upper()
                    generate_code(counter, string)
                    relocation_table.append(counter)
                    relocation_counter += 1
                    counter += int(operand_table['MOVER'][1])

                    string = CONSTANTS.COMP +"\t" + "REG_F"
                    generate_code(counter, string)
                    counter += int(operand_table['COMP'][1])

                    string = CONSTANTS.BC + "\t" + "E"
                    counterEndIf = len(pass1_code)
                    generate_code(counter, string)
                    relocation_table.append(counter)
                    relocation_counter += 1
                    counter += int(operand_table['BC'][1])
                    counterif += 1
        elif (line.startswith('endif')):
            endiftoggle = 1
            string = pass1_code[counterEndIf]
            endifstring = "ENDIF"+str(counterif)
            symbol_table[endifstring] = counter
            string1 = string+"\t"+endifstring
            pass1_code[counterEndIf] = string1
        elif(line.startswith('loop')):
            count = int(line[4:].strip())
            loop_lit_name = "=\'" + str(count) + "\'"
            literal_table[loop_lit_name] = counter
            generate_code(counter, loop_lit_name)
            counter += 1

            string = CONSTANTS.MOVI +"\tREG_D\t"+loop_lit_name
            generate_code(counter,string)
            relocation_table.append(counter)
            relocation_counter += 1
            counter += int(operand_table[CONSTANTS.MOVI][1])

            counterloop +=1

            symbol_table["AGAIN"+str(counterloop)+"_"+filename.upper()] = counter
            string = "AGAIN"+str(counterloop)+"_"+filename.upper()+"\t"+CONSTANTS.DCR+"\t"+"REG_D"
            generate_code(counter, string)
            counter += int(operand_table[CONSTANTS.DCR][1])
        elif(line.startswith('endloop')):
            lit_name = "=\'" + str(0) + "\'"
            literal_table[lit_name] = counter
            generate_code(counter, lit_name)
            counter += 1

            string = CONSTANTS.COMPRI + "\t" + "REG_D" + "\t" + lit_name
            generate_code(counter, string)
            relocation_table.append(counter)
            relocation_counter += 1
            counter += int(operand_table['COMPI'][1])

            string = CONSTANTS.BC + "\t" + "GE" +"\t"+"AGAIN"+str(counterloop)+"_"+filename.upper()
            generate_code(counter, string)
            relocation_table.append(counter)
            relocation_counter += 1
            counter += int(operand_table['BC'][1])
            counterif += 1
        elif(line.startswith('extern')):
            line = line[6:].strip()
            extenal_varibles[line.upper()] = counter
            if(line not in symbol_table.keys()):
                symbol_table[line.upper()] = 0
                string = CONSTANTS.EXTRN +"\t"+line.upper()
                generate_code(counter, string)
                counter += int(operand_table[CONSTANTS.EXTRN][1])

def pass2_assemble():
    symbol_table_keys = symbol_table.keys()
    literal_table_keys = literal_table.keys()

    for item in pass1_code:
        items = item.split("\t")
        string = ""

        if(items[1].startswith(CONSTANTS.COMP) or items[1].startswith(CONSTANTS.COMPI)):
            for i in range(0, len(items) - 2, 1):
                string += items[i] + "\t"

            if items[-2].strip() in symbol_table_keys:
                if (symbol_table[items[-2]] == 0):
                    string += items[-2] + "\t"
                else:
                    string += str(symbol_table[items[-2]]) + "\t"
            elif items[-2].strip() in literal_table_keys:
                if len(items) != 2:
                    string += str(literal_table[items[-2]])
                else:
                    string += items[-2]
            else:
                string += items[-2] + "\t"

            if items[-1].strip() in symbol_table_keys:
                if (symbol_table[items[-1]] == 0):
                    string += items[-1]
                else:
                    string += str(symbol_table[items[-1]])
            elif items[-1].strip() in literal_table_keys:
                if len(items) != 2:
                    string += str(literal_table[items[-1]])
                else:
                    string += items[-1]
            else:
                string += items[-1]

        elif items[-1].strip() in symbol_table_keys:
            for i in range(0, len(items) - 1, 1):
                string += items[i] + "\t"
            if(symbol_table[items[-1]] == 0):
                string+= items[-1]
            else:
                string += str(symbol_table[items[-1]])
        elif items[-1].strip() in literal_table_keys:
            for i in range(0, len(items) - 1, 1):
                string += items[i] + "\t"
            if(len(items) != 2):
                string += str(literal_table[items[-1]])
            else:
                string += items[-1]
        else:
            string = item

        pass2_code.append(string)

def get_results(filename,opcodes):
    global  operand_table
    reset()
    operand_table = opcodes
    generate_start_code()
    assemble_file(filename)
    generate_stop_code()
    pass2_assemble()
    return symbol_table,literal_table,extenal_varibles,relocation_table,pass1_code,pass2_code,counter