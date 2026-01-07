class BitString:
    def __init__(self, data):
        if isinstance(data, str):
            if all(c in '01' for c in data):
                self.bits = data
            else:
                self.bits = ''.join(format(ord(ch), '08b') for ch in data)
        elif isinstance(data, BitString):
            self.bits = data.bits
        else:
            raise TypeError

    @classmethod
    def from_bits(cls, bits):
        if any(c not in '01' for c in bits):
            raise ValueError
        obj = cls.__new__(cls)
        obj.bits = bits
        return obj

    @classmethod
    def half(cls, other, side):
        if not isinstance(other, BitString):
            raise TypeError
        if side not in ('left', 'right'):
            raise ValueError
        mid = len(other.bits) // 2
        half_bits = other.bits[:mid] if side == 'left' else other.bits[mid:]
        return cls.from_bits(half_bits)

    def __repr__(self):
        return f"BitString({self.bits!r})"

    def __str__(self):
        return self.bits

    def __len__(self):
        return len(self.bits)

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            return BitString.from_bits(self.bits[idx])
        return self.bits[idx]


    def __setitem__(self, idx, value):
        if isinstance(idx, slice):
            value = ''.join(value)
            if any(c not in '01' for c in value):
                raise ValueError
            bits_list = list(self.bits)
            bits_list[idx] = value
            new_bits = ''.join(bits_list)
        else:
            if value not in ('0', '1'):
                raise ValueError
            new_bits = self.bits[:idx] + str(value) + self.bits[idx + 1:]
        if len(new_bits) % 8:
            raise ValueError
        self.bits = new_bits

    def sync_text(self):
        chars = [chr(int(self.bits[i:i + 8], 2))
                 for i in range(0, len(self.bits), 8)]
        return ''.join(chars)

    def copy(self):
        return BitString.from_bits(self.bits)

    def __xor__(self, other):
        if not isinstance(other, BitString):
            raise TypeError
        if len(self.bits) != len(other.bits):
            raise ValueError
        xor_bits = ''.join(
            '0' if a == b else '1'
            for a, b in zip(self.bits, other.bits)
        )
        return BitString.from_bits(xor_bits)
