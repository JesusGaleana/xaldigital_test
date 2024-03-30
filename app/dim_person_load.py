import os
import pandas as pd
from utils.files_manager import FileManager
from utils.postgres_db import PostgreSQLConnection
from utils.read_config_file import YamlDataLoader
from utils.data_validator import AppDataValidator


if __name__ == "__main__":
    # Initializes the config dictionary
    yaml_data_loader = YamlDataLoader(file_path="config.yml")
    config_params = yaml_data_loader.read_yaml_file()

    # Initializes Tthe FileManager object to read the file
    file_manager = FileManager(file_type="csv", file_path=config_params["file_path"])
    data = file_manager.read_file()

    # Getting only person data
    data_company = data[[config_params["person_info"]["cols_from_file"]]].drop_duplicates()

    # Get connection from Database
    connection = PostgreSQLConnection(
        host = os.getenv("HOST_DB"),
        port= os.getenv("PORT_DB"),
        database = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD")
    )
    connection.connect()

    # Validate if the data exist in the table
    columns = config_params["person_info"]["cols_from_file"]
    columns.insert(0,'id')
    join_cols = config_params["person_info"]["cols_join"]
    app_validator = AppDataValidator(connection=connection)
    df_new_data = app_validator.validate_db_table(data_company_filtered, config_params["person_info"]["read_query"], columns, join_cols)

    # Create a list of rows to be inserted and declarate the columns where the data to be inserted
    if not df_new_data.empty:
        values = df_new_data.values.tolist()
        columns = ', '.join([str(col) for col in config_params["person_info"]["cols_from_file"]])
        connection.insert_query(table=config_params["person_info"]["table"], columns=columns, values=values)

    connection.disconnect()
