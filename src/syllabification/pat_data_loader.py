import os
from typing import List

from src.data_loader_and_saver import AbstractDataLoaderAndSaver


class PatDataLoader(AbstractDataLoaderAndSaver):
    """Class to load data in pat format (TeX hyphenation patterns)."""

    extension = "pat"

    def __init__(self, base_dir: str, input_data_dir: str) -> None:
        super().__init__(base_dir, input_data_dir=input_data_dir)

    def load_data(self, file_name: str, ratio: float = 1) -> List[str]:
        with open(os.path.join(self.input_data_dir, file_name), "r") as f:
            loaded_patterns = [line.rstrip() for line in f.readlines() if not line.startswith("%")]

        return loaded_patterns[: ratio * len(loaded_patterns)]
