import re

MICROCODE_SIZE = 69

# Arithmetic Logical Unit
CMD = {
    'add': 50,
    'notL': 51,
    'notR': 52,
    'incL': 53,
    'decL': 54,
    'incR': 55,
    'decR': 56,
    'xor': 57,
    'end': 67,
    'dec': 68
}

# Multiplexer controls
MUX = {
    'in': 1,
    'A': 2,
    'B': 3,
    'C': 4,
    'D': 5,
    'E': 6,
    'F': 7,
}

# Registers
REG = {
    'A': 8, 
    'B': 15, 
    'C': 22, 
    'D': 29, 
    'E': 36, 
    'F': 43,
}

# Register command offsets
REG_CMD = {
    'in': 0, 
    'LL1': 1, 
    'LR1': 2, 
    'AL1': 3, 
    'AR1': 4, 
    'CL1': 5, 
    'CR1': 6, 
}

FLAGS = {
    'AH': 1,
    'AL': 2,
    'BH': 3,
    'BL': 4,
    'CH': 5,
    'CL': 6,
    'DH': 7,
    'DL': 8,
    'EH': 9,
    'EL': 10,
    'FH': 11,
    'FL': 12,
    'CNT': 13,
    'ALU': 14,
    'false': 15
}

RESET = {
    'A': 58,
    'B': 59,
    'C': 60,
    'D': 61,
    'E': 62,
    'F': 63,
    'CNT': 64,
    'ROM': 65,
    'FLAG': 66
}


# Decorators
def no_operands(fn):
    def wrapper(self, src, dest):
        if src or dest:
            raise Exception('Operation doesn\'t take any operands')
        return fn(self)
    return wrapper


def one_operand(fn):
    def wrapper(self, src, dest):
        if dest:
            raise Exception('Operation only takes one operand')
        return fn(self, src)
    return wrapper


def two_operands(fn):
    def wrapper(self, src, dest):
        if dest and len(dest) > 1:
            raise Exception('Operation only takes to operands')
        return fn(self, src, dest and dest[0])
    return wrapper


def operand_array(fn):
    def wrapper(self, src, dest):
        array = []
        if src:
            array.append(src)
        if dest:
            array.extend(dest)
        return fn(self, array)
    return wrapper


# Compiler logic
class Compiler:
    _labels = {}
    #  -- Operations --[
    @no_operands
    def _end(self):
        # Out = L and End
        return self.create_micro_code(CMD['end'])

    @no_operands
    def _add(self):
        # M=L+R or A=M=L+R
        return self.create_micro_code(CMD['add'], REG['A'])
    
    @one_operand
    def _xor(self):
        # L xor R
        return self.create_micro_code(CMD['xor'], REG['A'])
    
    @one_operand
    def _inc(self, src):
        # increment
        if src != 'L' and src != 'R':
            raise Exception('Bad increment param!!')
        return self.create_micro_code(CMD['inc' + src], REG['A'])
    
    @one_operand
    def _dec(self, src):
        # decrement
        if src and src != 'L' and src != 'R':
            raise Exception('Bad decrement param!!')
        return self.create_micro_code(CMD['dec' + (src or '')], REG['A'] if src else -1)

    @one_operand
    def _not(self, src):
        # invert
        if src != 'L' and src != 'R':
            raise Exception('Bad not param!!')
        return self.create_micro_code(CMD['not' + src], REG['A'])

    def _mov(self, src, args):
        return self.create_micro_code(-1 if src == 'M' else MUX[src], *([] if args[0] == 'L' else [REG[key] for key in args]))
    
    @no_operands
    def _nop(self):
        return self.create_micro_code()
    
    @two_operands
    def _jmp(self, dest, flag):
        # jump
        destInt, flagInt = None, None
        try:
            destInt = int(dest)
        except ValueError:
            destInt = self._labels[dest]
        try:
            if flag:
                flagInt = int(flag)
        except ValueError:
            flagInt = FLAGS[flag]
        bits = self.to_binary_array(destInt, 8, 5)
        bits.extend(self.to_binary_array(flagInt if flagInt else FLAGS['false'], 4, 1))
        return self.create_micro_code(0, *bits)

    @operand_array
    def _res(self, operands):
        # reset data
        return self.create_micro_code(*[RESET[item] for item in operands])

    # -- Shifts
    @one_operand
    def _shl(self, src):
        return self.create_micro_code(REG[src] + REG_CMD['LL1'])
    
    @one_operand
    def _shr(self, src):
        return self.create_micro_code(REG[src] + REG_CMD['LR1'])
    
    @one_operand
    def _sal(self, src):
        return self.create_micro_code(REG[src] + REG_CMD['AL1'])
    
    @one_operand
    def _sar(self, src):
        return self.create_micro_code(REG[src] + REG_CMD['AR1'])
    
    @one_operand
    def _rol(self, src):
        return self.create_micro_code(REG[src] + REG_CMD['CL1'])
    
    @one_operand
    def _ror(self, src):
        return self.create_micro_code(REG[src] + REG_CMD['CR1'])

    # -- Helpers --    
    @staticmethod
    def create_micro_code(*ids):
        return ''.join(['1' if i in ids else '0' for i in range(0, MICROCODE_SIZE)])

    @staticmethod
    def to_binary_array(number, size, offset=0):
        return [i for i in range(offset, offset+size) if '{0:0{1}b}'.format(number, size)[-size:][i-offset] == '1']

    def parse(self, key, src, dest):
        op = getattr(self, '_'+key)
        if not op:
            raise Exception("Operaton does not exist")
        return op(src, dest)

    def compile(self, codelines):
        return self.parse_code( self.collect_labels(self.collect_comments(codelines)))

    _commentPattern = re.compile(r'(?:(?P<code0>.*?);(?P<comment>.*))|(?P<code1>.+)')

    def collect_comments(self, codelines):
        _codelines = []
        address = 0
        for codeline in codelines:
            match = self._commentPattern.match(codeline)
            if match:
                data = match.groupdict()
                code = data['code0'] or data['code1']
                if code:
                    _codelines.append(code)
                    address += 1
                # TODO add comments later
        return _codelines

    _labelPattern = re.compile(r'^\s*(?P<label>\w[\w\d]+):$')

    def collect_labels(self, codelines):
        _codelines = codelines.copy()
        address = 0
        for codeline in codelines:
            match = self._labelPattern.match(codeline)
            if match:
                self._labels[match.groupdict()['label']] = address
                _codelines.remove(codeline)
                continue
            address += 1
        return _codelines

    _codePattern = re.compile(r'\s*(?P<key>\w+)\s?(?P<src>[\d\w]+)?(?:\s)?(?P<dest>.+$)?')

    def parse_code(self, codelines):
        address = 0
        for codeline in codelines:
            match = self._codePattern.match(codeline)
            if not match:
                raise Exception('Parse exception at line {0}. Code: "{1}"'.format(
                    codelines.index(codeline), codeline
                ))
            args = match.groupdict()
            yield '{address} => "{code}",'.format(
                address=address,
                code=self.parse(
                    args['key'], args['src'],
                    None if not args['dest'] else args['dest'].strip().split(' ')
                )
            )
            address += 1


def main(args):
    for code in Compiler().compile(open(args[1]).readlines()):
        print(code)


if __name__ == '__main__':
    import sys

    main(sys.argv)
