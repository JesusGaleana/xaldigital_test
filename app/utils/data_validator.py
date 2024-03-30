import pandas as pd

class AppDataValidator: 
    def __init__(self, connection):
        self.connection = connection

    def validate_db_table(self, df_data, query, columns, join_cols):
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
        result_query = self.connection.execute_query(query)
        data = []
        if result_query:
            for row in result_query:
                data.append(row)
        df = pd.DataFrame(data)
        df = df.rename(columns=dict(zip(df.columns, columns)))

        # Join the df_data(from csv file) with the df(from database) and validate if the rows exist into database table
        if not df.empty:
            df = df[[join_cols]]
            merged_df = pd.merge(df_data, df, on=join_cols, how='left', indicator=True)

            # Filter the data that are missing in database table and return the dataframe.
            merged_df = merged_df[(merged_df["_merge"] == "left_only")]
            del merged_df["_merge"]
            return merged_df
        else:
            return df_data
