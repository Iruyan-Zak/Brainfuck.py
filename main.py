from collections import defaultdict
h = "+++[>+++[>+++[>+++<-]<-]<-]>>>."
command = "++++++++[>+++++++++<-]>." \
          "<+++++[>++++++<-]>-." \
          "+++++++." \
          "." \
          "+++." \
          ">++++[>++++++++<-]>." \
          "<<++++++++." \
          "--------." \
          "+++." \
          "------." \
          "--------." \
          ">>+."
command_index = 0
memory_index = 0
memory = defaultdict(int)
return_address = []
buffer = []


def plus():
    memory[memory_index] += 1


def minus():
    memory[memory_index] -= 1


def left():
    global memory_index
    memory_index -= 1


def right():
    global memory_index
    memory_index += 1


def begin():
    global command_index
    if memory[memory_index] == 0:
        command_index += 1
        while command[command_index] != ']':
            if command[command_index] == '[':
                begin()
            command_index += 1
    else:
        return_address.append(command_index)


def end():
    global command_index
    if memory[memory_index] == 0:
        return_address.pop()
    else:
        command_index = return_address[-1]

"""
def read():
    buffer.append(list(input()))
"""


def put():
    print(chr(memory[memory_index]), end='')


def dump():
    print()
    print(dict(memory))
    print("m_index={0}, c_index={1}".format(memory_index, command_index))


while command_index < len(command):
    c = command[command_index]
    if c == "+":
        plus()
    if c == "-":
        minus()
    if c == "<":
        left()
    if c == ">":
        right()
    if c == "[":
        begin()
    if c == "]":
        end()
    if c == ".":
        put()
    if c == "/":
        dump()
    command_index += 1

# dump()
