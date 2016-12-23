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
        try:
            self.memory[self.the_pointer] = next(self.istream)
        except StopIteration:
            try:
                from sys import stdin
                self.istream = iter(stdin.readline().encode())
                self.memory[self.the_pointer] = next(self.istream)
            except StopIteration:
                from itertools import repeat
                self.istream = repeat(0)
                self.memory[self.the_pointer] = 0

    def put(self):
        c = self.memory[self.the_pointer]
        if c in [ord('\n'), ord('\0')]:
            print(self.ostream.decode())
            self.ostream = b''
        else:
            self.ostream += c.to_bytes(1, byteorder='big')

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
            if self.ostream:
                print(self.ostream.decode(), end='')
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
        self.istream = iter([])
        self.ostream = b''

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
        program = \
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
