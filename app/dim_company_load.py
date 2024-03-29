import os
import pandas as pd
from utils.files_manager import FileManager
from utils.postgres_db import PostgreSQLConnection


def validate_db_table(connection, df_data, query):
    """Validates data from a DataFrame against a database table.

    Reads the database table using the provided query and converts the result into a DataFrame.
    Renames the columns of the DataFrame to match expected column names.
    Joins the DataFrame from the CSV file with the DataFrame from the database based on company names.
    Filters out rows that exist in the database table and returns the remaining DataFrame.

    Args:
        connection: An object representing the connection to the database.
        df_data (DataFrame): DataFrame containing data from a CSV file.
        query (str): SQL query to select data from the database table.

    Returns:
        DataFrame: DataFrame containing rows from df_data that do not exist in the database table,
                   or the original df_data if the database table is empty.

    """
    # Read the database table with the query and put the data into Dataframe
    result_query = connection.execute_query(query)
    data = []
    if result_query:
        for row in result_query:
            data.append(row)
    df = pd.DataFrame(data)
    columns = ["id", "company_name", "address", "city", "state", "zip"]
    df = df.rename(columns=dict(zip(df.columns, columns)))

    # Join the df_data(from csv file) with the df(from database) and validate if the rows exist into database table
    if not df.empty:
        df = df[["company_name"]]
        merged_df = pd.merge(df_data, df, on='company_name', how='left', indicator=True)

        # Filter the data that are missing in database table and return the dataframe.
        merged_df = merged_df[(merged_df["_merge"] == "left_only")]
        del merged_df["_merge"]
        return merged_df
    else:
        return df_data



if __name__ == "__main__":
    # Initializes Tthe FileManager object to read the file
    file_manager = FileManager(file_type="csv", file_path="data/sample_data.csv")
    data = file_manager.read_file()

    # Getting only company data
    data_company = data[["company_name", "address", "city","state", "zip"]].drop_duplicates()

    # Validation about state column (This column permit only letters and 2 characters)
    data_company["state_valid"] = [len(state) == 2 for state in data_company["state"]]
    data_company["state_valid_letter"] = [state.isalpha() for state in data_company["state"]]
    data_company_filtered = data_company[(data_company['state_valid']) & (data_company['state_valid_letter'])]
    data_company_filtered = data_company_filtered[["company_name", "address", "city", "state", "zip"]]

    # Get connection from Database
    connection = PostgreSQLConnection(
        host = os.getenv('HOST_DB'),
        port= os.getenv('PORT_DB'),
        database = os.getenv('DB_NAME'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD')
    )
    connection.connect()

    # Validate if the data exist in the table
    query = "SELECT * FROM dim_company;"
    df_new_data = validate_db_table(connection, data_company_filtered, query)

    # Create a list of rows to be inserted and declarate the columns where the data to be inserted
    if not df_new_data.empty:
        values = df_new_data.values.tolist()
        columns = "company_name, address, city, state, zip"
        connection.insert_query(table="dim_company", columns=columns, values=values)

    connection.disconnect()
