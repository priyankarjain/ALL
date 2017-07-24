from tkinter import *
import assembler_handler
import linker
import simulator
import ast
import Loader1

class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set,height=1000)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas, width = 1000)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

root = Tk()

rootFrame = VerticalScrolledFrame(root)

fileNames = StringVar()
fileNamesInp = ""

literal_table = { 'la':1, 'lb':2, 'lc':3 }
symbol_table = { 'sa11':1, 'sb11':2, 'sc11':3 }
flagBits = {'LE': StringVar().set(0), 'GE': StringVar().set(0), 'Eq': StringVar().set(0), 'S': StringVar().set(0), 'LT': StringVar().set(0), 'GT': StringVar().set(0)}
gpRegisters = {'Acc': StringVar().set(0), 'B': StringVar().set(0), 'C': StringVar().set(0), 'D': StringVar().set(0),
               'E': StringVar().set(0), 'F': StringVar().set(0), 'H': StringVar().set(0), 'L': StringVar().set(0)}
flagBitsList = []
gpRegistersList = []

for i in range(len(flagBits)):
    flagBitsList.append(StringVar())
    flagBitsList[i].set("")

for i in range(len(gpRegisters)):
    gpRegistersList.append(StringVar())
    gpRegistersList[i].set("")

memoryData = []
for i in range(100):
    memoryData.append(StringVar())
    memoryData[i].set('\t')

operand_table = {}
pass1_code = []
pass2_code = []
f = open('opcode.txt', 'r')
data = f.read()
f.close()
lines = data.splitlines()
for line in lines:
    line = line.split('//')
    operand_table[line[0]] = (line[1])

var = StringVar()
OPTIONS = []
linked_filenames = []

pass1_code_string = StringVar()
pass1_code_string_col1 = StringVar()
pass1_code_string_col2 = StringVar()
pass1_code_string_col3 = StringVar()
pass1_code_string_col4 = StringVar()
pass2_code_string_col1 = StringVar()
pass2_code_string_col2 = StringVar()
pass2_code_string_col3 = StringVar()
pass2_code_string_col4 = StringVar()

symbol_table_string = StringVar()
literal_table_string = StringVar()
linked_code = []
pass2_code_generated = False

pass1_codes = {}
pass2_codes = {}
symbol_tables = {}
literal_tables = {}
option = OptionMenu(None,var,"SELECT",*OPTIONS)

pass1_generated = False
pass2_generated = False
assemble_generated = False

def linkCode():
    global linked_code
    linked_code = linker.mainFunction(linked_filenames)
    setLinker()

linked_code_string_col1 = StringVar()
linked_code_string_col2 = StringVar()
linked_code_string_col3 = StringVar()
linked_code_string_col4 = StringVar()

sendfile_name = ""
def setLinker():
    global linked_code
    s1=""
    s2=""
    s3=""
    s4=""
    for p in linked_code:
        t = p.split("\t")
        print(len(t))
        s1 += t[0] + "\n"
        if len(t) > 3:
            if len(t) > 4:
                s2 += t[2] + "\n"
                s3 += t[3] + "\n"
                s4 += t[4] + "\n"
            else:
                s2 += "\n"
                s3 += t[2] + "\n"
                s4 += t[3] + "\n"
        else:
            s2 += "\n"
            s3 += t[2] + "\n"
            s4 += "\n"

    linked_code_string_col1.set(s1)
    linked_code_string_col2.set(s2)
    linked_code_string_col3.set(s3)
    linked_code_string_col4.set(s4)

def selectFile2(v, l):
    v.set(l)
    currentFileName = l
    updateAssembler(pass1_codes[currentFileName], pass2_codes[currentFileName],
                    symbol_tables[currentFileName], literal_tables[currentFileName])
    if(pass1_generated):
        pass1eventListener()
    if(pass2_generated):
        pass2EventListener()
    print(currentFileName)

def readfiles():
    global pass1_codes,pass2_codes,symbol_tables,literal_tables,OPTIONS,linked_filenames,sendfile_name

    fileNamesInp = fileNames.get()
    files = str(fileNamesInp).split()
    sendfile_name = "./Output/"+files[0]+"_pass2.link"
    linked_filenames = files
    OPTIONS = files

    if(option):
         m = option.children['menu']
         m.delete(0,END)
    print(files)
    m = option.children['menu']
    for value in OPTIONS:
        m.add_command(label=value,command=lambda v=var,l=value:selectFile2(v,l))
    m.add_command(label="Linker", command=setLinker)
    var.set(OPTIONS[0])
    # symbol_table, literal_table, extenal_varibles, relocation_table, pass1_code, pass2_code, counter=\
    pass1_codes,pass2_codes, symbol_tables, literal_tables = assembler_handler.assemble_mult_file(files)
    updateAssembler(pass1_codes[var.get()],pass2_codes[var.get()],symbol_tables[var.get()],literal_tables[var.get()])

frameDescribe = Label()
frameInput = LabelFrame()
frameOpCode = LabelFrame()
frameFile = LabelFrame()
frameMemory = LabelFrame()

def updateAssembler(pass1_codes,pass2_codes,symbol_table,literal_table):
    global  assemble_generated
    assemble_generated = True
    s1 = ""
    s2 = ""
    s3 = ""
    s4 = ""

    for p in pass1_codes:
        t = p.split("\t")
        s1 += t[0] + "\n"
        if len(t) > 2:
            if len(t) > 3:
                s2 += t[1] + "\n"
                s3 += t[2] + "\n"
                s4 += t[3] + "\n"
            else:
                s2 += "\n"
                s3 += t[1] + "\n"
                s4 += t[2] + "\n"
        else:
            s2 += "\n"
            s3 += t[1] + "\n"
            s4 += "\n"
    pass1_code_string_col1.set(s1)
    pass1_code_string_col2.set(s2)
    pass1_code_string_col3.set(s3)
    pass1_code_string_col4.set(s4)




def pass1eventListener():
    global symbol_tables,literal_tables, pass1_generated
    pass1_generated = True
    s = ""
    for p in symbol_tables[var.get()]:
        s += str(p) + "\t" + str(symbol_tables[var.get()][p]) + "\n"
    print("s", s)
    symbol_table_string.set(s)

    s = ""
    for p in literal_tables[var.get()]:
        s += str(p) + "\t" + str(literal_tables[var.get()][p]) + "\n"
    literal_table_string.set(s)
    print(var.get())

def pass2EventListener():
    global pass2_generated
    pass2_generated = True
    s1 = ""
    s2 = ""
    s3 = ""
    s4 = ""

    for p in pass2_codes[var.get()]:
        # s += p+"\n"
        t = p.split("\t")
        s1 += t[0] + "\n"
        if len(t) > 2:
            if len(t) > 3:
                s2 += t[1] + "\n"
                s3 += t[2] + "\n"
                s4 += t[3] + "\n"
            else:
                s2 += "\n"
                s3 += t[1] + "\n"
                s4 += t[2] + "\n"
        else:
            s2 += "\n"
            s3 += t[1] + "\n"
            s4 += "\n"

    pass2_code_string_col1.set(s1)
    pass2_code_string_col2.set(s2)
    pass2_code_string_col3.set(s3)
    pass2_code_string_col4.set(s4)
i = 0


currentInstruction = StringVar()
outputs = []
curIns = []
pc = 0
finalmemory = []
finalflagbits = []
finalorder = []
finalgenperreg = []

def simOutput():
    global memoryData,gpRegistersList,flagBitsList,outputs,curIns,finalflagbits,finalmemory,finalorder,finalgenperreg    
    simulator.simulate(sendfile_name)
    
    f = open("./Output/output_sim.link",'r')
    database = f.read()
    f.close()
    lines = database.splitlines()
    for line in lines:
        finalmemory.append(ast.literal_eval(line))
    f = open("./Output/output_lines.link",'r')
    database = f.read()
    f.close()
    lines = database.splitlines()
    for line in lines:
        finalorder.append(line)
    f = open("./Output/output_flag.link",'r')
    database = f.read()
    f.close()
    lines = database.splitlines()
    for line in lines:
        finalflagbits.append(ast.literal_eval(line))
    f = open("./Output/output_gen_per_reg.link",'r')
    database = f.read()
    f.close()
    lines = database.splitlines()
    for line in lines:
        finalgenperreg.append(ast.literal_eval(line))
    
    loaded_output = Loader1.loader(sendfile_name)
    for l in range(len(loaded_output)):
        memoryData[l].set(str(loaded_output[l]))
    for v in range(len(gpRegistersList)):
        gpRegistersList[v].set(0)
    for v in range(len(flagBitsList)):
        flagBitsList[v].set(0)

    
def stepSimulation():
    global pc
    if(pc<len(finalmemory)):
        for l in range(len(finalmemory[pc])):
            memoryData[l].set(str(finalmemory[pc][l]))
        k = 0
        for v in finalgenperreg[pc].keys():
            gpRegistersList[k].set(finalgenperreg[pc][v])
            k+=1
        k = 0
        for v in finalflagbits[pc].keys():
            flagBitsList[k].set(finalflagbits[pc][v])
            k+=1
        currentInstruction.set(finalorder[pc])
    pc+=1    

def displayPack():
    global  rootFrame
    global  option,var
    global pass1_codes,pass2_codes,symbol_tables,literal_tables,OPTIONS

    frameDescribe = Label(rootFrame.interior)
    frameInput = LabelFrame(rootFrame.interior, text= " Input the files ",width=10000)
    frameOpCode = LabelFrame(rootFrame.interior, text = " Operand table for reference ")
    frameFile = LabelFrame(rootFrame.interior, text = " Assembler Output tables ")
    frameLinker = LabelFrame(rootFrame.interior, text = "Linker Output tables ")
    frameMemory = LabelFrame(rootFrame.interior, text= " Simulations ")
    frameOpCodeTable = LabelFrame(rootFrame.interior, text = " Operand table for reference ")

    Label(frameDescribe, text = "\t\t\t\t\t\t\t Assembler  Linker  Loader Assignmet \t\t\t\t\t\t\t", font = 300).pack(side = TOP)
    frameDescribe.pack(side = TOP)


    #for input frame
    Label(frameInput, text="Enter the name of the files : ").pack(side = TOP)
    Entry(frameInput, textvariable = fileNames).pack()
    # .grid(row=1,column=0,padx=2,pady=2,sticky='we',columnspan=9)
    Button(frameInput, text="Assemble", command=readfiles).pack()
    # Button(frameInput, text="Assemble", command=readfiles).grid(row=2,column=0,padx=2,pady=2,sticky='we')
    Button(frameInput, text="Pass1Code", command=pass1eventListener).pack()
    # Button(frameInput, text="View Pass 1 Code", command=readfiles).grid(row=4,column=0,padx=2,pady=2,sticky='we')
    Button(frameInput, text="Pass2code", command=pass2EventListener).pack()
    # Button(frameInput, text="View Pass 2 code", command=readfiles).grid(row=5,column=0,padx=2,pady=2,sticky='we')
    Button(frameInput, text="Link", command=linkCode).pack()

    Button(frameInput, text="Load", command=simOutput).pack()
    # Button(frameInput, text="Simulate", command=readfiles).grid(row=3,column=0,padx=2,pady=2,sticky='we')

    frameInput.pack(fill = "both", expand="yes")


    #for opCode frame
    i = 0
    for k in operand_table.keys():
        key = str(k)
        value = str(operand_table[key])
        key = key.split()
        Label(frameOpCode, text = "" + key[0],justify=LEFT).grid(row=i, column=0, padx=2, pady=2, sticky='w')
        Label(frameOpCode, text = "" + key[1],justify=LEFT).grid(row=i, column=1, padx=2, pady=2, sticky='w')
        Label(frameOpCode, text = "" + key[2],justify=LEFT).grid(row=i, column=2, padx=2, pady=2, sticky='w')
        Label(frameOpCode, text = "" + value,justify=LEFT).grid(row=i, column=3, padx=2, pady=2, sticky='w')
        i += 1



    #for file frame
    frameFile0 = Frame(frameFile)
    frameFile1 = Frame(frameFile)
    frameFile2 = Frame(frameFile)
    frameFile3 = Frame(frameFile)
    frameFile4 = Frame(frameFile)


    currentFileName = ""

    def selectFile(temp):
        currentFileName = var.get()
        updateAssembler(pass1_codes[currentFileName],pass2_codes[currentFileName],
                        symbol_tables[currentFileName],literal_tables[currentFileName])
        print(currentFileName)



    option = OptionMenu(frameFile0, var,"SELECT FILE",*OPTIONS, command=selectFile)
    option.pack()



    print(pass1_code)
    Label(frameFile1, text="Pass 1 code : ", justify=LEFT).grid(row=0, column=0, padx=2, pady=2, sticky='w')
    Label(frameFile1, textvariable=pass1_code_string_col1, justify=LEFT).grid(row=1, column=0, padx=2, pady=2, sticky='w')
    Label(frameFile1, textvariable=pass1_code_string_col2, justify=LEFT).grid(row=1, column=1, padx=2, pady=2, sticky='w')
    Label(frameFile1, textvariable=pass1_code_string_col3, justify=LEFT).grid(row=1, column=2, padx=2, pady=2, sticky='w')
    Label(frameFile1, textvariable=pass1_code_string_col4, justify=LEFT).grid(row=1, column=3, padx=2, pady=2, sticky='w')
    Label(frameFile1, text="\t", justify=LEFT).grid(row=1, column=4, padx=2, pady=2, sticky='w')

    Label(frameFile2, text="Pass 2 code : ", justify=LEFT).grid(row=0, column=0, padx=2, pady=2, sticky='w')
    Label(frameFile2, textvariable=pass2_code_string_col1, justify=LEFT).grid(row=1, column=0, padx=2, pady=2, sticky='w')
    Label(frameFile2, textvariable=pass2_code_string_col2, justify=LEFT).grid(row=1, column=1, padx=2, pady=2, sticky='w')
    Label(frameFile2, textvariable=pass2_code_string_col3, justify=LEFT).grid(row=1, column=2, padx=2, pady=2, sticky='w')
    Label(frameFile2, textvariable=pass2_code_string_col4, justify=LEFT).grid(row=1, column=3, padx=2, pady=2, sticky='w')
    Label(frameFile2, text="\t", justify=LEFT).grid(row=1, column=4, padx=2, pady=2, sticky='w')

    Label(frameFile3, text="Symbol table : ", justify=LEFT).grid(row=0, column=0, padx=2, pady=2, sticky='w')
    Label(frameFile3, textvariable=symbol_table_string, justify=LEFT).grid(row=1, column=0, padx=2, pady=2, sticky='w')
    Label(frameFile3, text="\t", justify=LEFT).grid(row=1, column=1, padx=2, pady=2, sticky='w')
    Label(frameFile4, text="Literal table : ", justify=LEFT).grid(row=0, column=0, padx=2, pady=2, sticky='w')
    Label(frameFile4, text="\t ", justify=LEFT).grid(row=0, column=1, padx=2, pady=2, sticky='w')
    Label(frameFile4, textvariable=literal_table_string, justify=LEFT).grid(row=1, column=0, padx=2, pady=2, sticky='w')


    Label(frameLinker, text="Linked code : ", justify=LEFT).grid(row=0, column=0, padx=2, pady=2, sticky='w')
    Label(frameLinker, textvariable=linked_code_string_col1, justify=LEFT).grid(row=1, column=0, padx=2, pady=2, sticky='w')
    Label(frameLinker, textvariable=linked_code_string_col2, justify=LEFT).grid(row=1, column=1, padx=2, pady=2, sticky='w')
    Label(frameLinker, textvariable=linked_code_string_col3, justify=LEFT).grid(row=1, column=2, padx=2, pady=2, sticky='w')
    Label(frameLinker, textvariable=linked_code_string_col4, justify=LEFT).grid(row=1, column=3, padx=2, pady=2, sticky='w')
    # for i in range(len(pass1_code)):
        # Label(frameFile1, text="\t\t"+ pass1_code[i]+ "\t\t").grid(row = i, column = 0, padx = 2, pady = 2, sticky = 'w'  )
        # Label(frameFile1, textvariable=pass1_code[i]).grid(row = i, column = 0, padx = 2, pady = 2, sticky = 'w'  )

    # for i in range(len(pass2_code)):
    #     Label(frameFile2, text=pass2_code[i]).grid(row = i, column = 0, padx = 2, pady = 2, sticky = 'w'  )
    #
    # i = 0
    # for k in literal_table.keys():
    #     Label(frameFile3, text=str(k)).grid(row = i, column = 0, padx = 2, pady = 2, sticky = 'w')
    #     Label(frameFile3, text=str(literal_table[k])).grid(row = i, column = 1, padx = 2, pady = 2, sticky = 'w')
    #     i += 1
    #
    # i = 0
    # for k in symbol_table.keys():
    #     Label(frameFile4, text=str(k)).grid(row = i, column = 0, padx = 2, pady = 2, sticky = 'w')
    #     Label(frameFile4, text=str(symbol_table[k])).grid(row = i, column = 1, padx = 2, pady = 2, sticky = 'w')
    #     i += 1

    frameFile0.pack(side=TOP)
    frameFile1.pack(side=LEFT,expand="yes", fill="y")
    frameFile2.pack(side=LEFT,expand="yes", fill="y")
    frameFile3.pack(side=LEFT,expand="yes", fill="y")
    frameFile4.pack(side=LEFT,expand="yes", fill="y")
    frameLinker.pack(side=LEFT,expand="yes",fill="both")
    frameOpCode.pack(side=LEFT,fill="y", expand="yes")
    frameFile.pack(fill = "both", expand="yes")


    #for showing simulations :
    frameFlagBits = Frame(frameMemory)
    frameGpRegisters = Frame(frameMemory)
    frameMemoryData = Frame(frameMemory)
    frameCurrentInstruction = Frame(frameMemory)

    Label(frameFlagBits, text = " Flag registers ").grid(row=0, columnspan=8)
    i=1
    for k in flagBits.keys():
        Label(frameFlagBits, textvariable = flagBitsList[i-1], bg='white',fg='black',width=10).grid(row=1, column = i, padx = 2, pady = 2, sticky = 'w')
        Label(frameFlagBits, text = k).grid(row=2, column = i, padx = 2, pady = 2, sticky = 'w')
        i += 1
    frameFlagBits.pack()

    Label(frameGpRegisters, text = " General purpose registers ").grid(row=0, columnspan=8)
    i=1
    for k in gpRegisters.keys():
        Label(frameGpRegisters, textvariable = gpRegistersList[i-1], bg='white', fg='black',width=10).grid(row=1, column = i, padx = 2, pady = 2, sticky = 'w')
        Label(frameGpRegisters, text = k).grid(row=2, column = i, padx = 2, pady = 2, sticky = 'w')
        i += 1
    frameGpRegisters.pack()
    Label(frameCurrentInstruction, text = " Current Instruction ").grid(row=0, column=0,sticky='w')
    Label(frameCurrentInstruction, textvariable = currentInstruction,bg='blue', fg='white',width=60).grid(row=0, column = 1,sticky='w')
    
    frameCurrentInstruction.pack()
    Label(frameMemoryData, text = "Memory").grid(row=0, columnspan = 10)
    for i in range(10):
        for j in range(10):
            Label(frameMemoryData, textvariable = memoryData[i*10+j], bg='white',width = 9).grid(row =i + 1, column = j,padx = 2, pady = 2, sticky ='w')

    frameMemoryData.pack()

    frameMemory.pack(fill = "both", expand="yes")

    # frameOpCode.pack(fill = "both", expand="yes")
    Button(frameInput, text="Next Step", command=stepSimulation).pack()
    rootFrame.pack(fill="both",expand="yes")

displayPack()

root.mainloop()