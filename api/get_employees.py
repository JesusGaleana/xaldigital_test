import os
from flask import Flask
import psycopg2

# Creating the Flask App
app = Flask(__name__)

# Database connection
conn = psycopg2.connect(
    host = os.getenv('HOST_DB'),
    port= os.getenv('PORT_DB'),
    database = os.getenv('DB_NAME'),
    user = os.getenv('DB_USER'),
    password = os.getenv('DB_PASSWORD')
)


@app.route('/', methods=['GET'])
def get_employees():
    """Route to get all records of employees including personal information, company, and department.

    Returns:
        html_code (str): HTML-formatted table containing the records.
    """
    #Get information for employees from database
    cursor = conn.cursor()
    cursor.execute("""select
                            fe.id,
                            dp.first_name,
                            dp.last_name,
                            dc.company_name,
                            dc.address,
                            dc.city,
                            dc.state,
                            dc.zip,
                            dp.phone1,
                            dp.phone2,
                            dp.email,
                            dd.department_name
                        from
                            fact_employees fe
                        left join dim_person dp on
                            fe.employee_id = dp.id
                        left join dim_company dc on
                            fe.company_id = dc.id
                        left join dim_department dd on
                            fe.department_id = dd.id""")
    result = cursor.fetchall()
    cursor.close()

    # Format the results into HTML table
    html_code = """<head>
                    <meta charset="UTF-8">
                    <title>Employees</title>
                    <style>
                    /* Estilo para centrar los elementos */
                    .centrado {
                        text-align: center;
                    }
                    table {
                        width: 50%;
                        margin-left: auto;
                        margin-right: auto;
                        border-collapse: collapse;
                    }
                    th, td {
                        border: 1px solid black;
                        padding: 8px;
                        text-align: left;
                        white-space: nowrap;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                    </style>
                    </head>
                    <body>
                    <h1 class="centrado">Employees</h1>
                    <h3 class="centrado">Employees Data (Personal information, Company and Department)</h3>"""
    html_table = "<table><tr><th>ID</th><th>Firs Name</th><th>Last Name</th><th>Company</th><th>Address</th><th>City</th><th>State</th><th>Zip Code</th><th>Phone One</th><th>Phone Two</th><th>Email</th><th>Department Name</th></tr>"
    for row in result:
        html_table += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td><td>{row[6]}</td><td>{row[7]}</td><td>{row[8]}</td><td>{row[9]}</td><td>{row[10]}</td><td>{row[11]}</td></tr>"
    html_table += "</table>"

    html_code += html_table
    html_code += "</body>"
    return html_code


if __name__ == '__main__':
    app.run(debug=False)
