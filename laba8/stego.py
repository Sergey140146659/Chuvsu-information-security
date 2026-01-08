import re


class SentenceIntervalStego:

    SENTENCE_END_PATTERN = re.compile(r'([.!?])(\s+)')
    END_MARKER = '\x00'

    def __init__(self):
        pass

    def text_to_bits(self, text: str) -> str:
        return ''.join(format(byte, '08b') for byte in text.encode('utf-8'))

    def bits_to_text(self, bits: str) -> str:
        bytes_list = [int(bits[i:i+8], 2) for i in range(0, len(bits), 8)]
        return bytes(bytes_list).decode('utf-8')

    def preprocess_container(self, container: str) -> str:
        def normalize_spaces(match):
            return match.group(1) + ' '
        return self.SENTENCE_END_PATTERN.sub(normalize_spaces, container)

    def get_capacity(self, container: str) -> int:
        matches = self.SENTENCE_END_PATTERN.findall(container)
        return len(matches)

    def get_capacity_bytes(self, container: str) -> int:
        return self.get_capacity(container) // 8

    def can_embed(self, container: str, message: str) -> bool:
        message_bits = self.text_to_bits(message)
        capacity = self.get_capacity(container)
        return len(message_bits) <= capacity

    def embed(self, container: str, message: str) -> str:
        container = self.preprocess_container(container)
        message_bits = self.text_to_bits(message)
        capacity = self.get_capacity(container)

        if len(message_bits) > capacity:
            raise ValueError(
                f"Сообщение слишком длинное: {len(message_bits)} бит, "
                f"ёмкость контейнера: {capacity} бит"
            )

        bit_index = 0

        def replace_spaces(match):
            nonlocal bit_index
            punctuation = match.group(1)

            if bit_index < len(message_bits):
                bit = message_bits[bit_index]
                bit_index += 1
                spaces = ' ' if bit == '0' else '  '
            else:
                spaces = ' '

            return punctuation + spaces

        return self.SENTENCE_END_PATTERN.sub(replace_spaces, container)

    def extract(self, stego_container: str, message_length_bits: int = None) -> str:
        bits = []

        for match in self.SENTENCE_END_PATTERN.finditer(stego_container):
            spaces = match.group(2)
            bit = '0' if len(spaces) == 1 else '1'
            bits.append(bit)

            if message_length_bits and len(bits) >= message_length_bits:
                break

        bits_str = ''.join(bits)
        bits_str = bits_str[:len(bits_str) // 8 * 8]

        if not bits_str:
            return ""

        return self.bits_to_text(bits_str)

    def extract_with_length_prefix(self, stego_container: str) -> str:
        all_bits = []

        for match in self.SENTENCE_END_PATTERN.finditer(stego_container):
            spaces = match.group(2)
            bit = '0' if len(spaces) == 1 else '1'
            all_bits.append(bit)

        if len(all_bits) < 16:
            raise ValueError("Недостаточно данных для извлечения длины сообщения")

        length_bits = ''.join(all_bits[:16])
        message_length = int(length_bits, 2)
        message_bits = ''.join(all_bits[16:16 + message_length * 8])

        return self.bits_to_text(message_bits)

    def embed_with_marker(self, container: str, message: str) -> str:
        message_with_marker = message + self.END_MARKER
        return self.embed(container, message_with_marker)

    def extract_with_marker(self, stego_container: str) -> str:
        bits = []

        for match in self.SENTENCE_END_PATTERN.finditer(stego_container):
            spaces = match.group(2)
            bit = '0' if len(spaces) == 1 else '1'
            bits.append(bit)

        bits_str = ''.join(bits)
        result_bytes = []

        for i in range(0, len(bits_str) - 7, 8):
            byte_bits = bits_str[i:i+8]
            byte_val = int(byte_bits, 2)
            if byte_val == 0:
                break
            result_bytes.append(byte_val)

        return bytes(result_bytes).decode('utf-8')

    def embed_with_length_prefix(self, container: str, message: str) -> str:
        message_bits = self.text_to_bits(message)
        length_prefix = format(len(message), '016b')
        full_message_bits = length_prefix + message_bits

        container = self.preprocess_container(container)
        capacity = self.get_capacity(container)

        if len(full_message_bits) > capacity:
            raise ValueError(
                f"Сообщение слишком длинное: {len(full_message_bits)} бит, "
                f"ёмкость контейнера: {capacity} бит"
            )

        bit_index = 0

        def replace_spaces(match):
            nonlocal bit_index
            punctuation = match.group(1)

            if bit_index < len(full_message_bits):
                bit = full_message_bits[bit_index]
                bit_index += 1
                spaces = ' ' if bit == '0' else '  '
            else:
                spaces = ' '

            return punctuation + spaces

        return self.SENTENCE_END_PATTERN.sub(replace_spaces, container)
