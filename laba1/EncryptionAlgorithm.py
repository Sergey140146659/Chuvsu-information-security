class EncryptionAlgorithm:
    def __init__(self, encrypt_dict: dict, block_size: int):
        self.encrypt_dict = encrypt_dict
        self.decrypt_dict = {val: key for key, val in encrypt_dict.items()}
        self.block_size = block_size

    def text_split(self, text: str) -> list:
        blocks = []
        for i in range(0, len(text), self.block_size):
            block = text[i:i + self.block_size]
            blocks.append(block)
        return blocks

    def encrypt_text(self, text: str) -> str:
        split_text = self.text_split(text)
        encrypted_blocks = list(map(lambda block: self.encrypt_dict[block], split_text))
        return ''.join(encrypted_blocks)

    def decrypt_text(self, text: str) -> str:
        split_text = self.text_split(text)
        decrypted_blocks = list(map(lambda block: self.decrypt_dict[block], split_text))
        return ''.join(decrypted_blocks)
