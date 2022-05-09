import os
import gzip
from gensim.models import Word2Vec
from typing import List

from src.data_loader_and_saver import AbstractDataLoaderAndSaver


class EmbeddingsSaver(AbstractDataLoaderAndSaver):
    """Class to save compressed Word2Vec embeddings."""

    extension = "gz"

    def __init__(self, embeddings_type: str, base_dir: str, output_data_dir: str) -> None:
        """
        :param embeddings_type: Type of embeddings (sampa_syllables/tokens)
        """
        super().__init__(base_dir, output_data_dir=output_data_dir)
        self.embeddings_type = embeddings_type

    def save_embeddings(self, word_2_vec_model: Word2Vec, vocab: List[str], file_name_extension: str) -> None:
        """
        Save compressed Word2Vec embeddings into output directory.
        :param word_2_vec_model: Trained Word2Vec model
        :param vocab: Word2Vec model vocabulary
        :param file_name_extension: Extension of the embeddings file name
        """
        file_name = "embeddings_" + self.embeddings_type + file_name_extension

        # Create output file
        with open(os.path.join(self.output_data_dir, file_name), "w") as f:
            for syllable in vocab:
                vector = word_2_vec_model.wv[syllable]
                to_write = [syllable, *vector]
                f.write(" ".join(str(x) for x in to_write))
                f.write("\n")

        # Compress output file
        file_name_with_compress_ext = self._add_extension_to_file_name(file_name)

        with open(os.path.join(self.output_data_dir, file_name), "rb") as f:
            with gzip.open(os.path.join(self.output_data_dir, file_name_with_compress_ext), "wb") as f_gz:
                f_gz.writelines(f)

        # Delete uncompressed output file
        os.remove(os.path.join(self.output_data_dir, file_name))

        print(f"Embeddings saved to {file_name_with_compress_ext}")
