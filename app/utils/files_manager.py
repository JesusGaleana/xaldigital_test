import pandas as pd 


class FileManager:
    def __init__(self, file_type, file_path):
        """Initializes a new instance of the FileManager class.

        Args:
            file_type (str): File type to identify the best handle to extract (ex. csv or parquet)
            file_path (str): Path where the file is located, the file name and extension are necessary here.
        """
        self.file_type = file_type
        self.file_path = file_path

    def read_file(self):
        """Read files function to get data from files

        Returns:
            data (Dataframe): Pandas dataframe with the file data.
        """
        if self.file_type == "csv":
            try:
                data = pd.read_csv(self.file_path)
                return data
            except FileNotFoundError:
                print("The file does not exists.")
                return None
            except Exception as e:
                print("Error reading file:", e)
                return None

