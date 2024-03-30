import os
import pandas as pd
from utils.files_manager import FileManager
from utils.postgres_db import PostgreSQLConnection
from utils.read_config_file import YamlDataLoader


def getting_data_db(query, columns):
    query_results = connection.execute_query(query)
    data = []
    if query_results:
        for row in query_results:
            data.append(row)
    df = pd.DataFrame(data)
    df = df.rename(columns=dict(zip(df.columns, columns)))
    return df


if __name__ == "__main__":
    # Initializes the config dictionary
    yaml_data_loader = YamlDataLoader(file_path="config.yml")
    config_params = yaml_data_loader.read_yaml_file()

    # Initializes Tthe FileManager object to read the file
    file_manager = FileManager(file_type="csv", file_path=config_params["file_path"])
    df_data = file_manager.read_file()
    df_data.rename(columns={'department': 'department_name'}, inplace=True)

    # Get connection from Database
    connection = PostgreSQLConnection(
        host = os.getenv("HOST_DB"),
        port= os.getenv("PORT_DB"),
        database = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD")
    )
    connection.connect()

    # Getting data from dim person
    df = getting_data_db(query=config_params["person_info"]["read_query"], columns=config_params["person_info"]["target_cols"])

    # Merge Person ID with the CSV file data
    df = df[config_params["person_info"]["merge_cols"]]
    merged_df = pd.merge(df_data, df, on=config_params["person_info"]["cols_join"], how="left", indicator=True)
    del merged_df["_merge"]

    # Getting data from dim company
    df = getting_data_db(query=config_params["company_info"]["read_query"], columns=config_params["company_info"]["target_cols"])

    # Merge Company ID with the CSV file data
    df = df[config_params["company_info"]["merge_cols"]]
    merged_df = pd.merge(merged_df, df, on=config_params["company_info"]["cols_join"], how="left", indicator=True)
    del merged_df["_merge"]

    # Getting data from dim department
    df = getting_data_db(query=config_params["department_info"]["read_query"], columns=config_params["department_info"]["target_cols"])

    # Merge Department ID with the CSV file data
    df = df[config_params["department_info"]["merge_cols"]]
    merged_df = pd.merge(merged_df, df, on=config_params["department_info"]["cols_join"], how="left", indicator=True)
    del merged_df["_merge"]

    # Getting just the ID columns for load into fact employees table
    if not merged_df.empty:
        merged_df = merged_df[config_params["employee_info"]["source_cols"]]
        values = merged_df.values.tolist()
        columns = ', '.join([str(col) for col in config_params["employee_info"]["target_cols"]])
        connection.insert_query(table=config_params["employee_info"]["table"], columns=columns, values=values)

    # Close the conection to the database
    connection.disconnect()
