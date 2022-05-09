import pandas as pd
import os

from src.data_loader_and_saver import AbstractDataLoaderAndSaver


class CoNLLDataSaver(AbstractDataLoaderAndSaver):
    """Class to save dataframe contents into CoNLL format file."""

    extension = "txt"

    def __init__(self, base_dir: str, output_data_dir: str, poem_line: bool = False):
        """
        :param poem_line: Whether one input sequence should represent a whole poem or just one poem line
        """
        super().__init__(base_dir, output_data_dir=output_data_dir)
        self.poem_line = poem_line

    def save_data(self, data: pd.DataFrame, file_name: str) -> None:
        file_name_with_ext = self._add_extension_to_file_name(file_name)

        # Create directory if not exists
        file_path = os.path.join(self.output_data_dir, file_name_with_ext)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as f:
            last_poem_idx = None
            last_line_idx = None

            for row in data.reset_index().iterrows():
                values = row[1].values

                poem_idx = values[0]
                line_idx = values[1]

                if last_poem_idx is not None:
                    if self.poem_line:
                        should_write_empty_line = poem_idx != last_poem_idx
                    else:
                        should_write_empty_line = poem_idx != last_poem_idx or line_idx != last_line_idx

                    if should_write_empty_line:
                        f.write("\n")

                f.write(" ".join("".join(str(value).split()) for value in values))
                f.write("\n")

                last_poem_idx = poem_idx
                last_line_idx = line_idx

        print(f"CoNLL dataset saved to {file_name_with_ext}")
