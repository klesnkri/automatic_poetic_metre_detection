import json
import os.path
from typing import Tuple
import pandas as pd
from itertools import islice
from typing import Any
from abc import ABC


class AbstractDataLoaderAndSaver(ABC):
    """Abstract class to load and save data in given format."""

    extension = None

    def __init__(self, base_dir: str, input_data_dir: str = "", output_data_dir: str = "") -> None:
        """
        :param base_dir: Absolute path of the base directory
        :param input_data_dir: Directory to load data from
        :param output_data_dir: Directory to save data to
        """
        self.input_data_dir = os.path.join(base_dir, input_data_dir)
        self.output_data_dir = os.path.join(base_dir, output_data_dir)

    @classmethod
    def _add_extension_to_file_name(cls, file_name: str) -> str:
        """
        Add correct extension to file name.
        :param file_name: File name
        :return: File name with correct extension
        """
        return file_name + "." + cls.extension

    def load_data(self, file_name: str, ratio: float = 1) -> Any:
        """
        Load data from file and return.
        :param file_name: File to load data from
        :param ratio: Percentage of data to load
        :return: Loaded data
        """
        pass

    def save_data(self, data: Any, file_name: str) -> None:
        """
        Save data to file.
        :param data: Data to save
        :param file_name: Name of file to save data to
        """
        pass

    def load_all_data(self, file_name_extension: str = "") -> Tuple[Any, Any, Any]:
        """
        Load train, dev and test data at once.
        :param file_name_extension: Extension of the data files
        :return: Loaded train, dev and test data
        """
        train_data = self.load_data(f"train{file_name_extension}")
        dev_data = self.load_data(f"dev{file_name_extension}")
        test_data = self.load_data(f"test{file_name_extension}")

        return train_data, dev_data, test_data

    def save_all_data(self, train_data: Any, dev_data: Any, test_data: Any, file_name_extension: str = "") -> None:
        """
        Save train, dev and test data at once.
        :param train_data: Train data to save
        :param dev_data: Dev data to save
        :param test_data: Test data to save
        :param file_name_extension: Extension of the data file names
        """
        self.save_data(train_data, f"train{file_name_extension}")
        self.save_data(dev_data, f"dev{file_name_extension}")
        self.save_data(test_data, f"test{file_name_extension}")


class JSONDataLoaderAndSaver(AbstractDataLoaderAndSaver):
    """Class to load and save data in JSON format."""

    extension = "json"

    def __init__(self, base_dir: str, input_data_dir: str = "", output_data_dir: str = "") -> None:
        super().__init__(base_dir, input_data_dir, output_data_dir)

    def load_data(self, file_name: str, ratio: float = 1) -> Any:
        file_name_with_ext = self._add_extension_to_file_name(file_name)

        with open(os.path.join(self.input_data_dir, file_name_with_ext), "r") as f:
            data = json.load(f)
            cnt = int(len(data) * ratio)

            if type(data) == list:
                data = data[:cnt]
            elif type(data) == dict:
                data = dict(islice(data.items(), cnt))

        print(f"{file_name_with_ext}: loaded {len(data)} records.")

        return data

    def save_data(self, data: Any, file_name: str) -> None:
        file_name_with_ext = self._add_extension_to_file_name(file_name)

        with open(os.path.join(self.output_data_dir, file_name_with_ext), "w") as f:
            json.dump(data, f)

        print(f"Data saved to {file_name_with_ext}")


class CSVDataLoaderAndSaver(AbstractDataLoaderAndSaver):
    """Class to load and save data in CSV format."""

    extension = "csv"

    def __init__(self, base_dir: str, index_cols, input_data_dir: str = "", output_data_dir: str = "") -> None:
        """
        :param index_cols: Columns to use as index of the pandas DataFrame
        """
        super().__init__(base_dir, input_data_dir, output_data_dir)
        self.index_cols = index_cols

    def load_data(self, file_name: str, ratio: float = 1) -> pd.DataFrame:
        file_name_with_ext = self._add_extension_to_file_name(file_name)
        df = pd.read_csv(os.path.join(self.input_data_dir, file_name_with_ext), index_col=self.index_cols)
        cnt = int(df.shape[0] * ratio)
        print(f"{file_name_with_ext}: loaded {cnt} records.")

        return df[:cnt]

    def save_data(self, data: pd.DataFrame, file_name: str) -> None:
        file_name_with_ext = self._add_extension_to_file_name(file_name)
        data.to_csv(os.path.join(self.output_data_dir, file_name_with_ext))
        print(f"Data saved to {file_name_with_ext}")
