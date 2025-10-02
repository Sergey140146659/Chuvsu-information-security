from BitString import BitString
import os

class DES:
    def __init__(self, IP: list, FP: list, E: list, S: dict, P: list, PC1: list, PC2: list, LS: list):
        self.IP = IP
        self.FP = FP
        self.E = E
        self.S = S
        self.P = P
        self.PC1 = PC1
        self.PC2 = PC2
        self.LS = LS
        self.pad = 0
        self.K_keys = []

    def IP_permutation(self, block: BitString):
        IP_block = block.copy()
        for new_index, old_index in enumerate(self.IP, 0):
            IP_block[new_index] = block[old_index]
        return IP_block

    def E_expansion(self, block: BitString):
        E_expansion_block = BitString('0' * 48)
        for old_index, new_index in enumerate(self.E, 0):
            E_expansion_block[new_index[0]] = block[old_index]
            E_expansion_block[new_index[1]] = block[old_index]
        return E_expansion_block

    def S_i_transform(self, block: BitString, i: str):
        k = int(block.bits[0] + block.bits[5], 2)
        l = int(block.bits[1 : 5], 2)
        return self.S[i][k][l]

    def S_transform(self, block: BitString):
        transformed_blocks = []
        for i in range(0, 48, 6):
            S_i_block = BitString(block[i : i + 6])
            index = f"s{(i // 6 + 1)}"
            result = self.S_i_transform(S_i_block, index)
            transformed_blocks.append(BitString(bin(result)[2:].zfill(4)))
        concatenated_blocks = BitString.from_bits(''.join(b.bits for b in transformed_blocks))
        S_P_permutation = concatenated_blocks.copy()
        for new_index, old_index in enumerate(self.P, 0):
            S_P_permutation[new_index] = concatenated_blocks[old_index]
        return S_P_permutation

    def left_shift(self, block, i):
        shift = self.LS[i]
        return BitString(block[shift:].bits + block[:shift].bits)

    def PC2_permutation(self, L, R):
        LR = BitString.from_bits(''.join(b.bits for b in [L, R]))
        LR_PC2_permutation = BitString('0' * 48)
        for new_index, old_index in enumerate(self.PC2, 0):
            LR_PC2_permutation[new_index] = LR[old_index]
        return LR_PC2_permutation

    def get_K_keys(self, K: BitString):
        K_PC1_permutation = BitString('0' * 56)
        for new_index, old_index in enumerate(self.PC1, 0):
            K_PC1_permutation[new_index] = K[old_index]
        K_keys = []
        L = K_PC1_permutation[0 : 28]
        R = K_PC1_permutation[28 : 56]
        for iter in range(16):
            L_shifted = self.left_shift(L, iter)
            R_shifted = self.left_shift(R, iter)
            K_keys.append(self.PC2_permutation(L_shifted, R_shifted))
            L = L_shifted
            R = R_shifted
        self.K_keys = K_keys
        return K_keys

    def f(self, R: BitString, K: BitString):
        R_expansion = self.E_expansion(R)
        R_expansion = R_expansion ^ K
        S_P_transform = self.S_transform(R_expansion)
        return S_P_transform

    def encrypt_block(self, block: BitString, K: BitString):
        IP = self.IP_permutation(block)
        L = BitString(IP[: 32])
        R = BitString(IP[32: ])
        K_keys = self.get_K_keys(K=K)

        for k in K_keys:
            L, R = R, L ^ self.f(R, k)
        L, R = R, L
        LR = BitString.from_bits(''.join(b.bits for b in [L, R]))
        LR_FP = LR.copy()
        for new_index, old_index in enumerate(self.FP, 0):
            LR_FP[new_index] = LR[old_index]
        return LR_FP

    def encrypt_text(self, text: str, key_hex: str) -> str:
        if len(key_hex) != 16:
            raise ValueError("Ключ должен быть 16 hex-символов (64 бит)")
        key = BitString.from_bits(bin(int(key_hex, 16))[2:].zfill(64))
        while len(text) % 8:
            text = text + '_'
            self.pad += 1
        data = text.encode('utf-8')

        cipher_hex = []
        for i in range(0, len(data), 8):
            block = BitString(data[i:i+8].decode('latin1'))
            encrypted = self.encrypt_block(block, key)
            cipher_hex.append(f"{int(encrypted.bits, 2):016X}")
        return ''.join(cipher_hex)

    def decrypt_text(self, cipher_hex: str, key_hex: str) -> str:
        if len(key_hex) != 16:
            raise ValueError("Ключ должен быть 16 hex-символов (64 бит)")
        key = BitString.from_bits(bin(int(key_hex, 16))[2:].zfill(64))

        if len(cipher_hex) % 16:
            raise ValueError("Длина шифртекста должна быть кратна 16 hex-символам")
        plain_blocks = []

        for i in range(0, len(cipher_hex), 16):
            chunk = cipher_hex[i:i+16]
            block = BitString.from_bits(bin(int(chunk, 16))[2:].zfill(64))
            decrypted = self.decrypt_block(block, key)
            plain_blocks.append(decrypted.sync_text())

        return ''.join(plain_blocks)[:-self.pad]

    def decrypt_block(self, block: BitString, K: BitString) -> BitString:
        IP = self.IP_permutation(block)
        L = BitString(IP[:32])
        R = BitString(IP[32:])
        K_keys = self.get_K_keys(K=K)[::-1]

        for k in K_keys:
            L, R = R, L ^ self.f(R, k)
        L, R = R, L
        LR = BitString.from_bits(''.join(b.bits for b in [L, R]))
        LR_FP = LR.copy()
        for new_index, old_index in enumerate(self.FP, 0):
            LR_FP[new_index] = LR[old_index]
        return LR_FP

    # === лаба 5 ===

    def encrypt_text_cbc(self, text: str, key_hex: str, iv_hex=None) -> str:
        if len(key_hex) != 16:
            raise ValueError("Ключ должен быть 16 hex-символов (64 бит)")
        key = BitString.from_bits(bin(int(key_hex, 16))[2:].zfill(64))
        if iv_hex is None:
            iv_bytes = os.urandom(8)
            iv_hex = iv_bytes.hex()

        if len(iv_hex) != 16:
            raise ValueError("IV должен быть 16 hex-символов (64 бит)")

        feedback_block = BitString.from_bits(bin(int(iv_hex, 16))[2:].zfill(64))
        self.pad = 0
        while len(text) % 8:
            text = text + '_'
            self.pad += 1
        data = text.encode('latin1')

        cipher_hex_blocks = []
        for i in range(0, len(data), 8):
            plaintext_block = BitString(data[i:i+8].decode('latin1'))
            block_to_encrypt = plaintext_block ^ feedback_block
            encrypted_block = self.encrypt_block(block_to_encrypt, key)
            cipher_hex_blocks.append(f"{int(encrypted_block.bits, 2):016X}")
            feedback_block = encrypted_block

        return iv_hex.upper() + ''.join(cipher_hex_blocks)

    def decrypt_text_cbc(self, cipher_with_iv: str, key_hex: str) -> str:
        if len(key_hex) != 16:
            raise ValueError("Ключ должен быть 16 hex-символов (64 бит)")
        key = BitString.from_bits(bin(int(key_hex, 16))[2:].zfill(64))

        if len(cipher_with_iv) < 32 or len(cipher_with_iv) % 16 != 0:
            raise ValueError("Неверная длина шифртекста с IV")

        iv_hex = cipher_with_iv[:16]
        cipher_hex = cipher_with_iv[16:]

        feedback_block = BitString.from_bits(bin(int(iv_hex, 16))[2:].zfill(64))

        plain_text_blocks = []
        for i in range(0, len(cipher_hex), 16):
            ciphertext_block = BitString.from_bits(bin(int(cipher_hex[i:i+16], 16))[2:].zfill(64))
            decrypted_part = self.decrypt_block(ciphertext_block, key)
            plaintext_block = decrypted_part ^ feedback_block
            plain_text_blocks.append(plaintext_block.sync_text())
            feedback_block = ciphertext_block

        full_text = ''.join(plain_text_blocks)

        if self.pad > 0:
            return full_text[:-self.pad]
        return full_text
