import json
import os
import random
import itertools
from typing import Any

class EncryptionDictionary:
    def __init__(self, alphabet: list[Any], block_size: int, save_path: str = "./"):
        self.alphabet = alphabet
        self.block_size = block_size
        self.save_path = save_path
        self.encryption_dict = {}

    def create_dictionary(self, seed: int = 42) -> dict:
        if seed is not None:
            random.seed(seed)

        all_combinations = list(itertools.product(self.alphabet, repeat=self.block_size))
        string_combinations = []
        for combo in all_combinations:
            combo_str = ''.join(str(item) for item in combo)
            string_combinations.append(combo_str)

        values = string_combinations.copy()
        random.shuffle(values)

        self.encryption_dict = dict(zip(string_combinations, values))

        return self.encryption_dict

    def save_to_json(self, filename: str = "encryption_dict.json") -> str:
        full_path = os.path.join(self.save_path, filename)
        with open(full_path, 'w', encoding='utf-8') as file:
            json.dump(self.encryption_dict, file, indent=4)
        return full_path

    def load_from_json(self, filename: str = "encryption_dict.json") -> dict:
        full_path = os.path.join(self.save_path, filename)
        with open(full_path, 'r', encoding='utf-8') as file:
            self.encryption_dict = json.load(file)

        return self.encryption_dict

    def is_bijective(self) -> bool:
        values = list(self.encryption_dict.values())
        return len(values) == len(set(values))
