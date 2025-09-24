import json
import os
import random
import string

class GammaEncryptionDictionary:
    def __init__(self, alphabet: str, save_path: str = "./"):
        self.letter2index = {}
        self.index2letter = {}
        self.alphabet = alphabet
        self.save_path = save_path

        for index, letter in enumerate(alphabet, 0):
            self.letter2index[letter] = index
            self.index2letter[index] = letter

    def save_to_json(self, filename: str = "permutation.json") -> str:
        full_path = os.path.join(self.save_path, filename)
        permutation_data = {
            "permutation": self.permutation,
            "inverse_permutation": self.inverse_permutation,
            "block_size": self.block_size
        }
        with open(full_path, 'w', encoding='utf-8') as file:
            json.dump(permutation_data, file, indent=4)
        return full_path

    def load_from_json(self, filename: str = "permutation.json") -> dict:
        full_path = os.path.join(self.save_path, filename)
        with open(full_path, 'r', encoding='utf-8') as file:
            permutation_data = json.load(file)
        self.permutation = permutation_data["permutation"]
        self.inverse_permutation = permutation_data["inverse_permutation"]
        self.block_size = permutation_data["block_size"]
        return permutation_data
