from dataclasses import dataclass


@dataclass
class Register:
    value: int

    @property
    def low(self):
        return self.value % 256

    @property
    def hieght(self):
        return (self.value // 256) % 256

    @property
    def value32(self):
        return self.value % 2**32

    @low.setter
    def low(self, value):
        self.value += (value % 256) - self.low

    @hieght.setter
    def hieght(self, value):
        self.value += (value % 256 - self.hieght) * 256

    @value32.setter
    def value32(self, value):
        self.value += value % 2**32 - self.value32

    def __str__(self):
        return f"R({self.value})"


@dataclass
class Int:
    mem: bytearray
    offset: int
    size: int

    @property
    def value(self):
        mem, offset, size = self.mem, self.offset, self.size
        return int.from_bytes(mem[offset : offset + size], "little")

    @value.setter
    def value(self, value):
        mem, offset, size = self.mem, self.offset, self.size
        value = (value % 256**size).to_bytes(size, "little")
        mem[offset : offset + size] = value

    def __int__(self):
        base = self.size * 8
        return (self.value + 2 ** (base - 1)) % 2**base - 2 ** (base - 1)


def get_subreg(reg, i):
    if i == "low":
        return reg.low
    elif i == "hig":
        return reg.hieght
    elif i == "v32":
        return reg.value32


def set_subreg(reg, i, value):
    if i == "low":
        reg.low = value
    elif i == "hig":
        reg.hieght = value
    elif i == "v32":
        reg.value32 = value


@dataclass
class State:
    registers: tuple[Register]

    def move_reg(self, source, sd, target, td):
        source, target = self.registers[source], self.registers[target]
        set_subreg(target, td, get_subreg(source, td))

    def show(self):
        print("registers:")
        for i, name in enumerate("ABCD"):
            print(f"\t{name} : {self.registers[i].value}")


@dataclass
class Instruction:
    operation: str
    args: list[str]


@dataclass
class Programm:
    code: list[Instruction]
    variables: dict[str, (int, int)]
    labels: dict[str, int]