import enum

# global counters to avoid label collisions
eq_label_counter = 0
lt_label_counter = 0
gt_label_counter = 0
ret_counter = 0

temp_base = 5

class Command(enum.Enum):
    C_ARITHMETIC = 1
    C_PUSH = 2
    C_POP = 3
    C_LABEL = 4
    C_GOTO = 5
    C_IF = 6
    C_FUNCTION = 7
    C_RETURN = 8
    C_CALL = 9


commandType = {
    "add": Command.C_ARITHMETIC,
    "sub": Command.C_ARITHMETIC,
    "neg": Command.C_ARITHMETIC,
    "eq": Command.C_ARITHMETIC,
    "gt": Command.C_ARITHMETIC,
    "lt": Command.C_ARITHMETIC,
    "and": Command.C_ARITHMETIC,
    "or": Command.C_ARITHMETIC,
    "not": Command.C_ARITHMETIC,
    "push": Command.C_PUSH,
    "pop": Command.C_POP,
    "label": Command.C_LABEL,
    "if-goto": Command.C_IF,
    "goto": Command.C_GOTO,
    "function": Command.C_FUNCTION,
    "call": Command.C_CALL,
    "return": Command.C_RETURN,
}

# TODO: Add a method register a command
# register(vm_command, type, asm)
# command = commands.get(vm_command)
# print(command(arg1, args))


def add():
    return [
        "@SP",
        "A=M-1",
        "D=M",
        "A=A-1",
        "M=D+M",
        "D=A+1",
        "@SP",
        "M=D"
    ]


def sub():
    return [
        "@SP",
        "A=M-1",
        "D=M",
        "A=A-1",
        "M=M-D",
        "D=A+1",
        "@SP",
        "M=D"
    ]


def comp(op, label_counter):
    return [
        "@SP",
        "A=M-1",
        "D=M",
        "A=A-1",
        "D=M-D",
        f"@{op}_LABEL_{label_counter}_TRUE",
        f"D=D;J{op}",
        "@SP",
        "M=M-1",
        "M=M-1",
        "A=M",
        "M=0",
        f"@{op}_LABEL_{label_counter}_END",
        "0;JMP",
        f"({op}_LABEL_{label_counter}_TRUE)",
        "@SP",
        "M=M-1",
        "M=M-1",
        "A=M",
        "M=-1",
        f"({op}_LABEL_{label_counter}_END)",
        "@SP",
        "M=M+1"
    ]


def eq():
    global eq_label_counter
    eq_label_counter += 1
    return comp("EQ", eq_label_counter)


def lt():
    global lt_label_counter
    lt_label_counter += 1
    return comp("LT", lt_label_counter)


def gt():
    global gt_label_counter
    gt_label_counter += 1
    return comp("GT", gt_label_counter)


def binary(op):
    return [
        "@SP",
        "A=M-1",
        "D=M",
        "A=A-1",
        f"M=D{op}M",
        "D=A+1",
        "@SP",
        "M=D"
    ]


def cand():
    return binary('&')


def cor():
    return binary('|')


def unary(op):
    return [
        "@SP",
        "A=M-1",
        f"M={op}M"
    ]


def cnot():
    return unary('!')


def neg():
    return unary('-')

# Filename is required to correctly name static variables
# CodeWriter should set `filename` prior to code generation
filename = ''


def push(segment, index):
    def pushDataSegment(segment, index):
        return [
            f'@{index}',
            'D=A',
            f'@{segment}',
            'A=D+M',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1'
        ]

    def pushLocal(index):
        return pushDataSegment('LCL', index)

    def pushArgument(index):
        return pushDataSegment('ARG', index)

    def pushThis(index):
        return pushDataSegment('THIS', index)

    def pushThat(index):
        return pushDataSegment('THAT', index)

    def pushConstant(index):
        return [
            f'@{index}',
            'D=A',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1'
        ]

    def pushStatic(index):
        global filename
        return [
            f'@{filename}.{index}',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1'
        ]

    def pushPointer(index):
        pointer = 'THIS' if index == '0' else 'THAT'
        return [
            f'@{pointer}',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1'
        ]

    def pushTemp(index):
        global temp_base
        offset = str(temp_base + int(index))
        return [
            f'@{offset}',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1'
        ]

    def pushSegmentValue(segment):
        return [
            f'@{segment}',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1'
        ]

    pushSegment = {
        'local': pushLocal,
        'argument': pushArgument,
        'this': pushThis,
        'that': pushThat,
        'constant': pushConstant,
        'static': pushStatic,
        'pointer': pushPointer,
        'temp': pushTemp,
        'segmentValue': pushSegmentValue,
    }

    ps = pushSegment.get(segment)
    return ps(index)


def pop(segment, index):
    def popDataSegment(segment, index):
        return [
            '@SP',
            'M=M-1',
            f'@{index}',
            'D=A',
            f'@{segment}',
            'D=D+M',
            '@R15',
            'M=D',
            '@SP',
            'A=M',
            'D=M',
            '@R15',
            'A=M',
            'M=D'
        ]

    def popLocal(index):
        return popDataSegment('LCL', index)

    def popArgument(index):
        return popDataSegment('ARG', index)

    def popThis(index):
        return popDataSegment('THIS', index)

    def popThat(index):
        return popDataSegment('THAT', index)

    def popStatic(index):
        global filename
        return [
            '@SP',
            'AM=M-1',
            'D=M',
            f'@{filename}.{index}',
            'M=D'
        ]

    def popPointer(index):
        pointer = 'THIS' if index == '0' else 'THAT'
        return [
            '@SP',
            'AM=M-1',
            'D=M',
            f'@{pointer}',
            'M=D'
        ]

    def popTemp(index):
        global temp_base
        offset = str(temp_base + int(index))
        return [
            '@SP',
            'AM=M-1',
            'D=M',
            f'@{offset}',
            'M=D'
        ]

    popSegment = {
        'local': popLocal,
        'argument': popArgument,
        'this': popThis,
        'that': popThat,
        'static': popStatic,
        'pointer': popPointer,
        'temp': popTemp
    }

    ps = popSegment.get(segment)
    return ps(index)


def label(name, add_filename=True):
    global filename
    return [f'({filename}.{name})' if add_filename else f'({name})']


def ifgoto(name):
    global filename
    return [
        '@SP',
        'AM=M-1',
        'D=M',
        f'@{filename}.{name}',
        'D;JNE']

def goto(name, add_filename=True):
    global filename
    return [
        f'@{filename}.{name}' if add_filename else f'@{name}',
        '0;JMP']

def function(name, nargs):
    code = []
    # declare function entry
    code += label(name, add_filename=False)
    # init local variables
    for n in range(int(nargs)):
        code += push('constant', '0')
    return code

def call(name, nargs):
    global ret_counter
    ret_counter += 1
    code = []
    # push return address label
    code += push('constant', ''.join(label("ret"+ f".{ret_counter}"))[1:-1])
    # push LCL
    code += push('segmentValue', 'LCL')
    # push ARG
    code += push('segmentValue', 'ARG')
    # push THIS
    code += push('segmentValue', 'THIS')
    # push THAT
    code += push('segmentValue', 'THAT')
    # set ARG = SP - 5 - nargs
    arg_offset = 5 + int(nargs)
    code += [
        '@SP',
        'D=M',
        f'@{arg_offset}',
        'D=D-A',
        '@ARG',
        'M=D',
        ]
    # set LCL = SP
    code += [
        '@SP',
        'D=M',
        '@LCL',
        'M=D',
        ]
    # goto functionName
    code += goto(name, add_filename=False)
    # insert label
    code += label("ret"+ f".{ret_counter}")
    return code

def ret():
    code = []
    # Store endFrame (temp6)
    code += [
        '@LCL',
        'D=M',
        '@R13',
        'M=D',
    ]
    # Store return address (temp7 = LCL - 5)
    code += [
        '@LCL',
        'D=M',
        '@5',
        'A=D-A',
        'D=M',
        '@R14',
        'M=D',
    ]
    # Store return value at ARG[0]
    code += pop('argument', '0')
    # SP = ARG + 1
    code += [
        '@ARG',
        'D=M',
        'D=D+1',
        '@SP',
        'M=D',
    ]
    # Restore THAT
    code += [
        '@R13',
        'D=M', # endframe
        '@1',
        'A=D-A', # endframe -1
        'D=M', # *(endframe -1)
        '@THAT',
        'M=D',
    ]
    # Restore THIS
    code += [
        '@R13',
        'D=M', # endframe
        '@2',
        'A=D-A', # endframe -2
        'D=M', # *(endframe -2)
        '@THIS',
        'M=D',
    ]
    # Restore ARG
    code += [
        '@R13',
        'D=M', # endframe
        '@3',
        'A=D-A', # endframe -3
        'D=M', # *(endframe -3)
        '@ARG',
        'M=D',
    ]
    # Restore LOCAL
    code += [
        '@R13',
        'D=M', # endframe
        '@4',
        'A=D-A', # endframe -4
        'D=M', # *(endframe -4)
        '@LCL',
        'M=D',
    ]
    # Jump to return address
    code += [
        '@R14',
        'A=M',
        '0;JMP',
    ]
    return code

def startup():
    code = []
    code += [
        '@256',
        'D=A',
        '@SP',
        'M=D',
    ]
    code += call('Sys.init', '0')
    return code

commandAsm = {
    "add": add,
    "sub": sub,
    "neg": neg,
    "eq": eq,
    "gt": gt,
    "lt": lt,
    "and": cand,
    "or": cor,
    "not": cnot,
    "push": push,
    "pop": pop,
    "label": label,
    "if": ifgoto,
    "goto": goto,
    "function": function,
    "call": call,
    "return": ret,
    "startup": startup,
}
