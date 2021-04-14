debug = False

program = [
    "0xffb84b",
    "0xfafa6e",
    "0xffb84b",
    "0xd7f171",
    "0xffb84b",
    "0xb5e877",
    "0xffb84b",
    "0x95dd7d",
]

program_memory = {
    "0xfafa6e":["0xca00f2","0x48656c"],#  0  ----
    "0xd7f171":["0xca00f2","0x6c6f20"],#  1  ----
    "0xb5e877":["0xca00f2","0x576f72"],#  2  ----
    "0x95dd7d":["0xca00f2","0x6c6421"],#  3  ----                  
}



import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from pprint import pprint
from PIL import ImageColor


def read_var(d,h):
    if(d == commands_dict['int']):
        return int(h,16)
    elif(d == commands_dict['str']):
        return hex_to_string(h)
    elif(d == commands_dict['bool']):
        if(h == commands_dict['true']):
            return "True"
        return "False"

def hex_to_rgb(h):
    h = h.replace("0x","#")
    return list(ImageColor.getcolor(h,"RGB"))

def program_to_image(ins, registers):
 pass

def registers_string(r):
    for register in r:
        value = "EMPTY"
        value_as_type = ""
        if(len(r[register])>1):
            value = r[register][1]
            value_as_type =  " => " + str(read_var(r[register][0],r[register][1]))
        print(register + " : " + value + value_as_type)

def divide_chunks(toChunk, sep):
    def divide_chunks(l, n):
        for i in range(0, len(l), n): 
            yield l[i:i + n]
    return list(divide_chunks(toChunk, sep))

def rgb_to_hex(rgb):
    return "0x%02x%02x%02x" % tuple(rgb)

def hex_to_string(h):
    rgb = hex_to_rgb(h)
    text = chr(rgb[0])+chr(rgb[1])+chr(rgb[2])
    return text

def string_to_hex(s):
    rgb = [ord(s[0]),ord(s[1]),ord(s[2])]
    h = rgb_to_hex(rgb)
    return h


commands_dict = {
    'var': '0xD6CF0A',
    'copy':'0xc6a3e6',
    'int': '0xff0000',
    'str': '0xca00f2', 
    'bool':'0xed6b1a',
    'true':'0x32a852',
    'fals':'0xd93daf',
    'ptyp':'0xFFB84B',
    'praw':'0x9e8520',
    'add': '0x9D3756',
    'sub': '0x3243fc',
    'mult':'0x3dc9fc',
    'eq':  '0x1fe061',
    'lt':  '0xdb4716',
    'gt':  '0x7cebc4',
    # 'leg': '0xffffff',
    # 'geq': '0xffffff',
    'not': '0x6b1810',
    'if':  '0xe063bd',
    'inc': '0xa66d7f',
    'dec': '0x7a86ff',
    'for': '0x1d7499',
}

for com in commands_dict:
    commands_dict[com] = commands_dict[com].lower()

commands_image = [] 
for com in commands_dict:
    commands_image.append([hex_to_rgb(commands_dict[com])])
commands_image = commands_image

labels = []
for label in commands_dict:
    buffer = "".join([" " for i in range(5)])
    labels.append(label+buffer+"("+commands_dict[label]+")")

def program_to_image(code, mem):
    pic_out = []
    temp = []
    pad = "0xffffff"
    for register in mem:
        temp.append(hex_to_rgb(register))
    pic_out.append(temp)
    #print(temp)
    temp = []
    for register in mem:
        data = pad
        if(len(mem[register])>0):
            data = mem[register][0]
        temp.append(hex_to_rgb(data))
    pic_out.append(temp)
    temp = []
    for register in mem:
        data = pad
        if(len(mem[register])>0):
            data = mem[register][1]
        temp.append(hex_to_rgb(data))
    pic_out.append(temp)

    # if(len(code)>len(mem.keys())):
    #     for i in range(len(pic_out)):
    #         for p in range(len(code)-len(mem.keys())):
    #             pic_out[i].append([0,0,0])

    code_pic = []
    for command in code:
        code_pic.append(hex_to_rgb(command))
    #pic_out.insert(0, code_pic)
    #plt.imshow([code_pic])
    temp = []
    if(len(code)>len(mem)):
        pad_to = len(mem)
        #print(len(code_pic))
        code_pic = divide_chunks(code_pic, pad_to)
        for i in range(len(code_pic)):
            while(len(code_pic[i]) < pad_to):
                code_pic[i].append(hex_to_rgb(pad))      
        for i in range(len(code_pic)-1,-1,-1):
            pic_out.insert(0,code_pic[i])

    return pic_out


def run_code(ins, registers, debug=True):
    i = 0
    offset = 0
    old_ins = []
    for line in ins:
        old_ins.append(line)
    pre_run_pic = program_to_image(ins, registers)
    while(i<len(ins)):#for i in range(len(ins)+offset): # for every command from the input  while(i<len(ins)):
        if(ins[i] == ""):
            pass

        elif(ins[i] in commands_dict.values()): # if this command is valid
            if(debug): print(i, end=" ")
            command = ins[i] # get the current command
            if(command == commands_dict['var']): #check to see if this is a variable definition command
                if(commands_dict['var'] in ins[i+1:]):
                    far_index = ins[i+1:].index(commands_dict['var'])+len(ins[:i])+1
                    temp_var = ins[i+1:far_index]
                    #print(i+1)
                    #print()
                    ins[far_index] = ""
                    ins[far_index-1] = ""
                    ins[far_index-2] = ""
                    ins[far_index-3] = ""
                    # variable gained
                    reg_ind = temp_var[0]
                    d_type = temp_var[1]
                    var = temp_var[2]
                    
                    if(d_type in commands_dict.values()):# an integer
                        if(d_type == commands_dict['bool']):
                            if(var == commands_dict['true'] or var == commands_dict['fals']):
                                registers[reg_ind] = [d_type, var]
                            else:
                                print("NOT A VALID BOOLEAN", end=" ")
                        else:
                            registers[reg_ind] = [d_type, var]
                        if(debug): print(f"ADDED {var} TO {reg_ind} REGISTER", end=" ")
                    else:
                        print("INVALID DATATYPE", end=" ")

                else:
                    print("DIDNT CLOSE VARIABLE", end="")


            elif(command == commands_dict['add']): #check to see if this is a variable definition command
                if(commands_dict['add'] in ins[i+1:]):
                    # far_index = ins[i+1:].index(commands_dict['add'])+len(ins[:i])+1
                    # temp_var = ins[i+1:far_index]
                    far_index = ins[i+1:].index(commands_dict['add'])+len(ins[:i])+1
                    temp_var = ins[i+1:far_index]
                    #print(temp_var)
                    # variable gained
                    reg_ind = temp_var[0]
                    var_regs = temp_var[1:]

                    ins[far_index] = ""
                    for j in range(len(var_regs)+2):
                        ins[far_index-j] = ""

                    d_type = registers[var_regs[0]][0]
                    type_flag = True
                    for var in var_regs:
                        if(registers[var][0] != d_type):
                            type_flag = False
                            break
                    
                    if(type_flag):
                        value = 0
                        for var in var_regs:
                            value += int(registers[var][1], 16)

                        val_hex = "0x"+hex(value).replace("0x","").rjust(6, '0')
                        registers[reg_ind] = [d_type, val_hex]
                        if(debug): print(f"ADDED {value} TO {reg_ind} REGISTER", end=" ")
                    else:
                        print("DATATYPE MISMATCH", end=" ")

                else:
                    print("DIDNT CLOSE VARIABLE", end="")


            


            elif(command == commands_dict['sub']): #check to see if this is a variable definition command
                if(commands_dict['sub'] in ins[i+1:]):
                    far_index = ins[i+1:].index(commands_dict['sub'])+len(ins[:i])+1
                    temp_var = ins[i+1:far_index]

                    # variable gained
                    reg_ind = temp_var[0]
                    var_regs = temp_var[1:]

                    ins[far_index] = ""
                    for j in range(len(var_regs)+2):
                        ins[far_index-j] = ""

                    d_type = registers[var_regs[0]][0]
                    type_flag = True
                    for var in var_regs:
                        if(registers[var][0] != d_type):
                            type_flag = False
                            break
                    
                    if(type_flag):
                        value = int(registers[var_regs[0]][1],16)
                        #
                        for var in var_regs[1:]:
                            value -= int(registers[var][1], 16)

                        val_hex = "0x"+hex(value).replace("0x","").rjust(6, '0')
                        registers[reg_ind] = [d_type, val_hex]
                        if(debug): print(f"ADDED {value} TO {reg_ind} REGISTER", end=" ")
                    else:
                        print("DATATYPE MISMATCH", end=" ")

                else:
                    print("DIDNT CLOSE VARIABLE", end="")



            elif(command == commands_dict['mult']):
                if(commands_dict['mult'] in ins[i+1:]):
                    far_index = ins[i+1:].index(commands_dict['mult'])+len(ins[:i])+1
                    temp_var = ins[i+1:far_index]
                    #print(temp_var)
                    # variable gained
                    reg_ind = temp_var[0]
                    var_regs = temp_var[1:]

                    ins[far_index] = ""
                    for j in range(len(var_regs)+2):
                        ins[far_index-j] = ""

                    d_type = registers[var_regs[0]][0]
                    type_flag = True
                    for var in var_regs:
                        if(registers[var][0] != d_type):
                            type_flag = False
                            break
                    
                    if(type_flag):
                        value = 1
                        for var in var_regs:
                            value *= int(registers[var][1], 16)

                        val_hex = "0x"+hex(value).replace("0x","").rjust(6, '0')
                        registers[reg_ind] = [d_type, val_hex]
                        if(debug): print(f"ADDED {value} TO {reg_ind} REGISTER", end=" ")
                    else:
                        print("DATATYPE MISMATCH", end=" ")

                else:
                    print("DIDNT CLOSE VARIABLE", end="")




            elif(command == commands_dict['eq']):
                reg_ind = ins[i+1]
                val_1 = ins[i+2]
                val_2 = ins[i+3]
                ins[i] = ""
                ins[i+1] = ""
                ins[i+2] = ""
                ins[i+3] = ""
                if(registers[val_1][0] == registers[val_2][0]):
                    value = ""
                    if(registers[val_1][1] == registers[val_2][1]):
                        registers[reg_ind] = [commands_dict['bool'],commands_dict['true']]
                        value = commands_dict['true']
                    else:
                        registers[reg_ind] = [commands_dict['bool'],commands_dict['fals']]
                        value = commands_dict['fals']
                    if(debug): print(f"ADDED {value} TO {reg_ind} REGISTER", end=" ")
                else:
                    print("DATATYPE MISMATCH", end=" ")


            elif(command == commands_dict['lt']):
                reg_ind = ins[i+1]
                val_1 = ins[i+2]
                val_2 = ins[i+3]
                ins[i] = ""
                ins[i+1] = ""
                ins[i+2] = ""
                ins[i+3] = ""
                if(registers[val_1][0] == registers[val_2][0]):
                    value = ""
                    if(registers[val_1][1] < registers[val_2][1]):
                        registers[reg_ind] = [commands_dict['bool'],commands_dict['true']]
                        value = commands_dict['true']
                    else:
                        registers[reg_ind] = [commands_dict['bool'],commands_dict['fals']]
                        value = commands_dict['fals']
                    if(debug): print(f"ADDED {value} TO {reg_ind} REGISTER", end=" ")
                else:
                    print("DATATYPE MISMATCH", end=" ")

            elif(command == commands_dict['gt']):
                reg_ind = ins[i+1]
                val_1 = ins[i+2]
                val_2 = ins[i+3]
                ins[i] = ""
                ins[i+1] = ""
                ins[i+2] = ""
                ins[i+3] = ""
                if(registers[val_1][0] == registers[val_2][0]):
                    value = ""
                    if(registers[val_1][1] > registers[val_2][1]):
                        registers[reg_ind] = [commands_dict['bool'],commands_dict['true']]
                        value = commands_dict['true']
                    else:
                        registers[reg_ind] = [commands_dict['bool'],commands_dict['fals']]
                        value = commands_dict['fals']
                    if(debug): print(f"ADDED {value} TO {reg_ind} REGISTER", end=" ")
                else:
                    print("DATATYPE MISMATCH", end=" ")


            elif(command == commands_dict['not']):
                reg_ind = ins[i+1]
                val = ins[i+2]
                ins[i] = ""
                ins[i+1] = ""
                ins[i+2] = ""
                if(registers[val][0] == commands_dict['bool']):
                    value = ""
                    if(registers[val][1] == commands_dict['fals']):
                        registers[reg_ind] = [commands_dict['bool'],commands_dict['true']]
                        value = commands_dict['true']
                    else:
                        registers[reg_ind] = [commands_dict['bool'],commands_dict['fals']]
                        value = commands_dict['fals']
                    if(debug): print(f"ADDED {value} TO {reg_ind} REGISTER", end=" ")
                else:
                    print("CAN ONLY USE NOT ON A BOOL", end=" ")


            elif(command == commands_dict['if']):
                truth_val = ins[i+1]
                ins[i+1] = ""
                if(registers[truth_val][0] == commands_dict['bool']):
                    far_index = ins[i+1:].index(commands_dict['if'])+len(ins[:i])+1
                    ins[far_index] = ""
                    if(registers[truth_val][1] == commands_dict['true']):
                        if(debug): print(f"{truth_val} WAS TRUE, RUNNING FOLLOWING CODE", end=" ")
                    else:
                        for j in range(i,far_index):
                            ins[j] = ""
                        if(debug): print(f"{truth_val} WAS FALSE, SKIPING FOLLOWING CODE", end=" ")
    
                else:
                    print("IF STATEMENT REQUIRES BOOLEAN" , end=" ")



            elif(command == commands_dict['for']):
                times = ins[i+1]
                temp_reg = ins[i+2]
                far_index = ins[i+1:].index(commands_dict['for'])+len(ins[:i])+1
                coms = ins[i+3:far_index]
                #print(coms)
                ins[i] = ""
                ins[i+1] = ""
                ins[i+2] = ""
                ins[far_index] = ""
                coms_to_inject = []
        
                for _ in range(int(registers[times][1],16)-1):
                    coms_to_inject += coms
                    coms_to_inject += [commands_dict['inc'],temp_reg]
                
                ins = ins[:i+1]+coms_to_inject+ins[i:]
                if(debug): print(f"BEGINING FOR LOOP ON {temp_reg}", end=" ")


            elif(command == commands_dict['inc']):
                to_inc = ins[i+1]
                ins[i+1] = ""
                if(registers[to_inc][0] == commands_dict['int']):
                    value = int(registers[to_inc][1],16)
                    value += 1
                    val_hex = "0x"+hex(value).replace("0x","").rjust(6, '0')
                    registers[to_inc] = [commands_dict['int'],val_hex]
                    if(debug): print(f"REGISTER {to_inc} INCREMENTED", end=" ")
                else:
                    print("INVALID DATATYPE", end=" ")

            elif(command == commands_dict['dec']):
                to_inc = ins[i+1]
                ins[i+1] = ""
                if(registers[to_inc][0] == commands_dict['int']):
                    value = int(registers[to_inc][1],16)
                    value -= 1
                    val_hex = "0x"+hex(value).replace("0x","").rjust(6, '0')
                    registers[to_inc] = [commands_dict['int'],val_hex]
                    if(debug): print(f"REGISTER {to_inc} DECREMENTED", end=" ")
                else:
                    print("INVALID DATATYPE", end=" ")



            elif(command == commands_dict['copy']):
                orig_reg = ins[i+1]
                dest_reg = ins[i+2]
                ins[i] = ""
                ins[i+1] = ""
                ins[i+2] = ""
                registers[dest_reg] = [registers[orig_reg][0],registers[orig_reg][1]]
                if(debug): print(f"COPIED {orig_reg} TO {dest_reg}", end=" ")




            elif(command == commands_dict['praw']):
                reg_ind = ins[i+1]
                ins[i+1] = ""
                print(registers[reg_ind][1], end=" ")
                if(not debug): print()
            elif(command == commands_dict['ptyp']):
                reg_ind = ins[i+1]
                ins[i+1] = ""
                print(f"REGISTER {reg_ind} IS SET TO {read_var(registers[reg_ind][0],registers[reg_ind][1])}", end=" ")
                if(not debug): print()
            if(debug): print()
        else:
            if(debug): print(i, end=" ")
            print("INVALID COMMAND", end=" ")
            print("")
        ins[i] = ""
        i+=1
    #print(registers)
    if(debug): print("\nREGISTERS")
    if(debug): registers_string(program_memory)
    post_run_pic = program_to_image(old_ins,registers)
    return pre_run_pic,post_run_pic


pre,post = run_code(program, program_memory, debug=debug)

plt.clf()
plt.figure(figsize=(18,9))
plt.subplot(1, 2, 1)
plt.axis('off')
plt.imshow(pre)
plt.subplot(1, 2, 2)
plt.axis('off')
plt.imshow(post)
plt.show()

