class PermutationEncryptionAlgorithm:
    def __init__(self, permutation: list[int], inverse_permutation: list[int], block_size: int):
        self.permutation = permutation
        self.inverse_permutation = inverse_permutation
        self.block_size = block_size

    def pad_text(self, text: str) -> str:
        remainder = len(text) % self.block_size
        if remainder != 0:
            padding_size = self.block_size - remainder
            text += ' ' * padding_size
        return text

    def text_split(self, text: str) -> list[str]:
        padded_text = self.pad_text(text)
        blocks = []
        for i in range(0, len(padded_text), self.block_size):
            block = padded_text[i:i + self.block_size]
            blocks.append(block)
        return blocks

    def encrypt_block(self, block: str) -> str:
        encrypted_block = [''] * self.block_size
        for i in range(1, self.block_size + 1):
            original_position = i - 1
            new_position = self.permutation[original_position] - 1
            encrypted_block[new_position] = block[original_position]
        return ''.join(encrypted_block)

    def decrypt_block(self, block: str) -> str:
        decrypted_block = [''] * self.block_size
        for i in range(1, self.block_size + 1):
            original_position = i - 1
            new_position = self.inverse_permutation[original_position] - 1
            decrypted_block[new_position] = block[original_position]
        return ''.join(decrypted_block)

    def encrypt_text(self, text: str) -> str:
        blocks = self.text_split(text)
        encrypted_blocks = list(map(self.encrypt_block, blocks))
        return ''.join(encrypted_blocks)

    def decrypt_text(self, text: str) -> str:
        blocks = self.text_split(text)
        decrypted_blocks = list(map(self.decrypt_block, blocks))
        return ''.join(decrypted_blocks)
