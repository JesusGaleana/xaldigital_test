import yaml

class YamlDataLoader:
    def __init__(self, file_path):
        self.file_path = file_path


    def read_yaml_file(self):
        """Reads a YAML configuration file and returns the data as a Python dictionary.

        Args:
            file_path (str): The path to the YAML configuration file.

        Returns:
            dict: A Python dictionary containing the data from the YAML file.
        """
        try:
            with open(self.file_path, 'r') as file:
                data = yaml.safe_load(file)
            return data
        except FileNotFoundError:
            print("The file does not exists.")
            return None
        except yaml.YAMLError:
            print("There is an error in parsing the YAML file.")
            return None