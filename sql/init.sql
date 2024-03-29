CREATE TABLE dim_person (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone1 VARCHAR(15),
    phone2 VARCHAR(15),
    email VARCHAR(255)
);

CREATE TABLE dim_company (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(255),
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(2),
    zip VARCHAR(10)
);

CREATE TABLE dim_department (
    id SERIAL PRIMARY KEY,
    department_name VARCHAR(100)
);

CREATE TABLE fact_employees (
    id SERIAL PRIMARY KEY,
    employee_id INT,
    company_id INT,
    department_id INT,
    FOREIGN KEY (employee_id) REFERENCES dim_person(id),
    FOREIGN KEY (company_id) REFERENCES dim_company(id),
    FOREIGN KEY (department_id) REFERENCES dim_department(id)
);
