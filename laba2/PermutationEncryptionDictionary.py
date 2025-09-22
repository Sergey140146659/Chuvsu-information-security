import json
import os
import random

class PermutationEncryptionDictionary:
    def __init__(self, block_size: int, save_path: str = "./"):
        self.block_size = block_size
        self.save_path = save_path
        self.permutation = []
        self.inverse_permutation = []

    def create_permutation(self, seed: int = 42) -> list[int]:
        random.seed(seed)
        positions = list(range(1, self.block_size + 1))
        random.shuffle(positions)
        self.permutation = positions
        self.inverse_permutation = [0] * self.block_size
        for i in range(self.block_size):
            orig_pos = i + 1
            new_pos = self.permutation[i]
            self.inverse_permutation[new_pos - 1] = orig_pos
        return self.permutation

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

    def is_valid_permutation(self) -> bool:
        return len(self.permutation) == self.block_size and \
               sorted(self.permutation) == list(range(1, self.block_size + 1))
