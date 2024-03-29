import psycopg2

class PostgreSQLConnection:
    def __init__(self, host, port, database, user, password):
        """Initializes a new instance of the PostgreSQLConnector class.

        Args:
            host (str): Host where is located the database
            port (int): Access port to the database
            database (str): Database name
            user (str): User name to access to database
            password (str): Password of the user name
        """
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        """Connects to the PostgreSQL database using the provided connection parameters.
        Attempts to establish a connection to the PostgreSQL database using the host, port, database name, username, and password provided during object initialization.
        If the connection fails, it prints an error message indicating the reason for the failure.
        """
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()
            print("Connection successful to PostgreSQL")
        except (Exception, psycopg2.Error) as error:
            print("Error connecting to PostgreSQL:", error)

    def disconnect(self):
        """Disconnects from the PostgreSQL database by closing the cursor and connection.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Successful disconnection from PostgreSQL")

    def execute_query(self, query):
        """Function to execute a query to the database

        Args:
            query (String): Query to get data from the database

        Returns:
            list or None: A list with tuples from the query result or None if an error ocurrs.
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except (Exception, psycopg2.Error) as error:
            print("Error executing query:", error)
            return None

    def insert_query(self, table, columns, values):
        """Inserts data into a specific table in the database.

        Args:
            table (str): Name of the table where the data will be inserted.
            columns (str): Names of the columns separated by comma where the values will be inserted.
            values (list): List of tuples where each tuple represents the values to insert into the corresponding columns.

        Returns:
            None
        """
        try:
            # Separate columns by comma and remove whitespace
            column_list = columns.split(", ")
            # Generate mask string dynamically
            mask = "(" + ','.join(['%s'] * len(column_list)) + ")"
            # cursor.mogrify() to insert multiple values
            args = ','.join(self.cursor.mogrify(mask, i).decode('utf-8') for i in values)
            
            # executing the sql statement
            self.cursor.execute(f"INSERT INTO {table} ({columns}) VALUES " + (args))
            self.connection.commit()
            return None
        except (Exception, psycopg2.Error) as error:
            print("Error executing insert query:", error)
            return None

