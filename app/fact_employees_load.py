import os
import pandas as pd
from utils.files_manager import FileManager
from utils.postgres_db import PostgreSQLConnection


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
    # Initializes Tthe FileManager object to read the file
    file_manager = FileManager(file_type="csv", file_path="data/sample_data.csv")
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
    query = "SELECT * FROM dim_person;"
    columns = ["person_id", "first_name", "last_name", "phone1", "phone2", "email"]
    df = getting_data_db(query, columns)

    # Merge Person ID with the CSV file data
    df = df[["person_id", "first_name", "last_name"]]
    merged_df = pd.merge(df_data, df, on=["first_name", "last_name"], how="left", indicator=True)
    del merged_df["_merge"]

    # Getting data from dim company
    query = "SELECT * FROM dim_company;"
    columns = ["company_id", "company_name", "address", "city", "state", "zip"]
    df = getting_data_db(query, columns)

    # Merge Company ID with the CSV file data
    df = df[["company_id", "company_name"]]
    merged_df = pd.merge(merged_df, df, on=["company_name"], how="left", indicator=True)
    del merged_df["_merge"]

    # Getting data from dim department
    query = "SELECT * FROM dim_department;"
    columns = ["department_id", "department_name"]
    df = getting_data_db(query, columns)

    # Merge Department ID with the CSV file data
    df = df[["department_id", "department_name"]]
    merged_df = pd.merge(merged_df, df, on=["department_name"], how="left", indicator=True)
    del merged_df["_merge"]

    # Getting just the ID columns for load into fact employees table
    if not merged_df.empty:
        merged_df = merged_df[["person_id", "company_id", "department_id"]]
        values = merged_df.values.tolist()
        columns = "employee_id, company_id, department_id"
        connection.insert_query(table="fact_employees", columns=columns, values=values)

    # Close the conection to the database
    connection.disconnect()
