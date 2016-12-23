class BrainFuck:
    def plus(self):
        self.memory[self.the_pointer] += 1

    def minus(self):
        self.memory[self.the_pointer] -= 1

    def left(self):
        self.the_pointer -= 1

    def right(self):
        self.the_pointer += 1

    def begin(self):
        if self.memory[self.the_pointer] != 0:
            self.call_stack.append(self.program_counter)
            return

        while True:
            self.program_counter += 1
            if self.program_counter >= self.program_length:
                return self.abort("PC{}: Corresponding ']' cannot be found."
                                  .format(self.call_stack[-1]))
            if self.program[self.program_counter] == ']':
                return
            if self.program[self.program_counter] == '[':
                self.begin()

    def end(self):
        if not self.call_stack:
            return self.abort("PC{}: Corresponding ']' cannot be found."
                              .format(self.program_counter))
        if self.memory[self.the_pointer] == 0:
            self.call_stack.pop()
        else:
            self.program_counter = self.call_stack[-1]

    def read(self):
        while True:
            try:
                self.memory[self.the_pointer] = next(self.buffer)
                return
            except StopIteration:
                try:
                    self.buffer = iter(input().encode())
                except EOFError:
                    from itertools import repeat
                    self.buffer = repeat(0)

    def put(self):
        print(chr(self.memory[self.the_pointer]), end='')

    def dump(self):
        from sys import stderr
        print("\nthe_pointer={0}, program_counter={1}"
              .format(self.the_pointer, self.program_counter), file=stderr)
        print(sorted(self.memory.items()), file=stderr)

    def run(self):
        try:
            while self.program_counter < self.program_length:
                self.interpreter[self.program[self.program_counter]]()
                self.program_counter += 1
        finally:
            self.dump()

    def abort(self, _msg):
        from sys import stderr
        self.program_counter = self.program_length
        print(_msg, file=stderr)
        self.dump()

    def __init__(self, _program):
        from collections import defaultdict
        self.program = _program
        self.program_length = len(_program)

        self.program_counter = 0
        self.the_pointer = 0
        self.memory = defaultdict(int)
        self.call_stack = []
        self.buffer = iter([])

        def nop_factory():
            def nop():
                pass

            return nop

        self.interpreter = defaultdict(nop_factory)
        self.interpreter.update({
            '+': self.plus,
            '-': self.minus,
            '<': self.left,
            '>': self.right,
            '[': self.begin,
            ']': self.end,
            ',': self.read,
            '.': self.put,
            '#': self.dump
        })


if __name__ == '__main__':
    from sys import argv
    try:
        program = open(argv[1]).read()
        if not program:
            raise ValueError
    except:
        program =\
            "++++++++[>+++++++++<-]>." \
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

    print(program)
    bf = BrainFuck(program)
    bf.run()
