class TrailingSpacesStego:

    NORMAL_SPACE = ' '
    NBSP = '\xa0'
    END_MARKER = '\x00'

    def __init__(self):
        pass

    def text_to_bits(self, text: str) -> str:
        return ''.join(format(byte, '08b') for byte in text.encode('utf-8'))

    def bits_to_text(self, bits: str) -> str:
        bytes_list = [int(bits[i:i+8], 2) for i in range(0, len(bits), 8)]
        return bytes(bytes_list).decode('utf-8')

    def preprocess_container(self, container: str) -> str:
        lines = container.split('\n')
        processed_lines = [line.rstrip() for line in lines]
        return '\n'.join(processed_lines)

    def get_capacity_mode1(self, container: str) -> int:
        lines = container.split('\n')
        return len(lines) - 1

    def get_capacity_mode2(self, container: str, bits_per_line: int = 8) -> int:
        lines = container.split('\n')
        return (len(lines) - 1) * bits_per_line

    def embed_mode1(self, container: str, message: str) -> str:
        container = self.preprocess_container(container)
        message_with_marker = message + self.END_MARKER
        message_bits = self.text_to_bits(message_with_marker)

        lines = container.split('\n')
        capacity = len(lines) - 1

        if len(message_bits) > capacity:
            raise ValueError(
                f"Сообщение слишком длинное: {len(message_bits)} бит, "
                f"ёмкость контейнера: {capacity} бит"
            )

        result_lines = []
        for i, line in enumerate(lines):
            if i < len(message_bits):
                bit = message_bits[i]
                spaces = ' ' if bit == '0' else '  '
                result_lines.append(line + spaces)
            else:
                result_lines.append(line)

        return '\n'.join(result_lines)

    def extract_mode1(self, stego_container: str) -> str:
        lines = stego_container.split('\n')
        bits = []

        for line in lines[:-1]:
            trailing_spaces = len(line) - len(line.rstrip())
            bit = '0' if trailing_spaces == 1 else '1'
            bits.append(bit)

        result_bytes = []
        bits_str = ''.join(bits)

        for i in range(0, len(bits_str) - 7, 8):
            byte_bits = bits_str[i:i+8]
            byte_val = int(byte_bits, 2)
            if byte_val == 0:
                break
            result_bytes.append(byte_val)

        return bytes(result_bytes).decode('utf-8')

    def embed_mode2(self, container: str, message: str, bits_per_line: int = 8) -> str:
        container = self.preprocess_container(container)
        message_with_marker = message + self.END_MARKER
        message_bits = self.text_to_bits(message_with_marker)

        lines = container.split('\n')
        capacity = (len(lines) - 1) * bits_per_line

        if len(message_bits) > capacity:
            raise ValueError(
                f"Сообщение слишком длинное: {len(message_bits)} бит, "
                f"ёмкость контейнера: {capacity} бит"
            )

        result_lines = []
        bit_index = 0

        for i, line in enumerate(lines[:-1]):
            spaces = ''
            for j in range(bits_per_line):
                if bit_index < len(message_bits):
                    bit = message_bits[bit_index]
                    bit_index += 1
                    spaces += self.NORMAL_SPACE if bit == '0' else self.NBSP
                else:
                    break
            result_lines.append(line + spaces)

        result_lines.append(lines[-1])
        return '\n'.join(result_lines)

    def extract_mode2(self, stego_container: str, bits_per_line: int = 8) -> str:
        lines = stego_container.split('\n')
        bits = []

        for line in lines[:-1]:
            line_stripped = line.rstrip()
            trailing = line[len(line_stripped):]

            for char in trailing:
                if char == self.NORMAL_SPACE:
                    bits.append('0')
                elif char == self.NBSP:
                    bits.append('1')

        result_bytes = []
        bits_str = ''.join(bits)

        for i in range(0, len(bits_str) - 7, 8):
            byte_bits = bits_str[i:i+8]
            byte_val = int(byte_bits, 2)
            if byte_val == 0:
                break
            result_bytes.append(byte_val)

        return bytes(result_bytes).decode('utf-8')
