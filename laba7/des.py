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

    def encrypt_text_ofb(self, text: str, key_hex: str, iv_hex: str = None, k: int = 8) -> str:
        if len(key_hex) != 16:
            raise ValueError("Ключ должен быть 16 hex-символов (64 бит)")

        key = BitString.from_bits(bin(int(key_hex, 16))[2:].zfill(64))

        if iv_hex is None:
            iv_hex = os.urandom(8).hex()

        if len(iv_hex) != 16:
            raise ValueError("IV должен быть 16 hex-символов (64 бит)")

        shift_register = BitString.from_bits(bin(int(iv_hex, 16))[2:].zfill(64))

        data = text.encode('latin1')
        cipher_bits = ""

        for i in range(len(data)):
            output_block = self.encrypt_block(shift_register, key)

            keystream_k_bits = output_block[:k]

            plaintext_byte = data[i:i+1]
            plaintext_k_bits = BitString(plaintext_byte.decode('latin1'))

            cipher_k_bits = plaintext_k_bits ^ keystream_k_bits
            cipher_bits += cipher_k_bits.bits

            shift_register = BitString.from_bits(shift_register.bits[k:] + output_block[:k].bits)

        cipher_hex = f"{int(cipher_bits, 2):0{len(cipher_bits) // 4}X}"

        return iv_hex.upper() + cipher_hex

    def decrypt_text_ofb(self, cipher_with_iv: str, key_hex: str, k: int = 8) -> str:
        if len(key_hex) != 16:
            raise ValueError("Ключ должен быть 16 hex-символов (64 бит)")

        key = BitString.from_bits(bin(int(key_hex, 16))[2:].zfill(64))

        if len(cipher_with_iv) < 16:
            raise ValueError("Неверная длина шифртекста с IV")

        iv_hex = cipher_with_iv[:16]
        cipher_hex = cipher_with_iv[16:]

        shift_register = BitString.from_bits(bin(int(iv_hex, 16))[2:].zfill(64))

        num_bits = len(cipher_hex) * 4
        ciphertext_bits_str = bin(int(cipher_hex, 16))[2:].zfill(num_bits)
        ciphertext_bits = BitString.from_bits(ciphertext_bits_str)

        plain_bytes_list = []

        for i in range(0, len(ciphertext_bits), k):
            output_block = self.encrypt_block(shift_register, key)

            keystream_k_bits = output_block[:k]

            cipher_k_bits = BitString(ciphertext_bits[i:i+k])

            plaintext_k_bits = cipher_k_bits ^ keystream_k_bits
            plain_bytes_list.append(plaintext_k_bits.sync_text().encode('latin1'))

            shift_register = BitString.from_bits(shift_register.bits[k:] + output_block[:k].bits)

        return (b"".join(plain_bytes_list)).decode('latin1')

    def generate_keystream_ofb(self, key_hex: str, iv_hex: str, length: int, k: int = 8) -> str:
        if len(key_hex) != 16:
            raise ValueError("Ключ должен быть 16 hex-символов (64 бит)")

        if len(iv_hex) != 16:
            raise ValueError("IV должен быть 16 hex-символов (64 бит)")

        key = BitString.from_bits(bin(int(key_hex, 16))[2:].zfill(64))
        shift_register = BitString.from_bits(bin(int(iv_hex, 16))[2:].zfill(64))

        keystream_bits = ""

        for _ in range(length):
            output_block = self.encrypt_block(shift_register, key)
            keystream_k_bits = output_block[:k]
            keystream_bits += keystream_k_bits.bits
            shift_register = BitString.from_bits(shift_register.bits[k:] + output_block[:k].bits)

        return keystream_bits
