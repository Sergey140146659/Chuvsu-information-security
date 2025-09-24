class GammaEncryptionAlgorithm:
    def __init__(self, letter2index: dict, index2letter: dict, t0: int, A: int, B: int, C: int):
        self.letter2index = letter2index
        self.index2letter = index2letter
        self.t0 = t0
        self.A = A
        self.B = B
        self.C = C

    def encrypt_text(self, text: str) -> str:
        transformed_text = list(map(lambda letter: self.letter2index[letter], text))
        gamma_sequence = [self.t0]
        for i in range(1, len(text)):
            gamma_i = (self.A * gamma_sequence[i - 1] + self.C) % self.B
            gamma_sequence.append(gamma_i)
        gamma_transformed_text = [(letter + gamma) % self.B for letter, gamma in zip(transformed_text, gamma_sequence)]
        crytped_text = ''.join(list(map(lambda letter: self.index2letter[letter], gamma_transformed_text)))
        return crytped_text

    def decrypt_text(self, text: str) -> str:
        transformed_text = list(map(lambda letter: self.letter2index[letter], text))
        gamma_sequence = [self.t0]
        for i in range(1, len(text)):
            gamma_i = (self.A * gamma_sequence[i - 1] + self.C) % self.B
            gamma_sequence.append(gamma_i)
        gamma_transformed_text = [(letter - gamma + self.B * 10) % self.B for letter, gamma in zip(transformed_text, gamma_sequence)]
        crytped_text = ''.join(list(map(lambda letter: self.index2letter[letter], gamma_transformed_text)))
        return crytped_text
