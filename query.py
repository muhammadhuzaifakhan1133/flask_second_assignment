import pymysql


def get_all_employees(db_conn):
    # fetch data from db
    query = "SELECT * FROM employee"
    cur = db_conn.cursor()
    cur.execute(query)

    return cur.fetchall()


def get_all_customers(db_conn, employee_id, name):
    query = "SELECT * FROM customer"
    if employee_id is not None or name is not None:
        query += " WHERE "
        if employee_id is not None:
            query += f"employee_id='{employee_id}'"
            if name is not None:
                query += " AND "
        if name is not None:
            query += f"(fname LIKE '%{name}%' OR lname LIKE '%{name}%')"
    print(query)
    cur = db_conn.cursor()
    cur.execute(query)
    return cur.fetchall()


def get_employee_by_id(db_conn, employee_id):
    # fetch data from db
    query = f"SELECT * FROM employee WHERE id=%(employee_id)s"
    cur = db_conn.cursor()
    cur.execute(query, {"employee_id": employee_id})

    return cur.fetchone()


def get_customer_by_id(db_conn, cust_id):
    query = f"SELECT * FROM customer WHERE id=%(customer_id)s"
    cur = db_conn.cursor()
    cur.execute(query, {"customer_id": cust_id})
    return cur.fetchone()


def delete_customer_by_id(db_conn, cust_id):
    query = f"DELETE FROM customer WHERE id=%(customer_id)s"
    cur = db_conn.cursor()
    isDeleted = cur.execute(query, {"customer_id": cust_id})
    db_conn.commit()
    return True if isDeleted == 1 else False


def add_new_employee(db_conn, data):
    # add record into databse
    query = f"""
                INSERT INTO employee (fname, lname, email, manager_id, job_title) 
                VALUES (%(fname)s, %(lname)s, %(email)s, %(manager_id)s, %(job_title)s)
            """
    cur = db_conn.cursor()
    cur.execute(
        query,
        {
            "fname": data.get("fname"),
            "lname": data.get("lname"),
            "email": data.get("email"),
            "manager_id": data.get("manager_id", 0),
            "job_title": data.get("job_title"),
        },
    )

    # save the changes permanently
    db_conn.commit()

    return cur.lastrowid

def add_new_service(db_conn, data):
    # add record into databse
    query = f"""
                INSERT INTO service (name, price) 
                VALUES (%(name)s, %(price)s)
            """
    cur = db_conn.cursor()
    cur.execute(
        query,
        {
            "name": data.get("name"),
            "price": data.get("price"),
        },
    )

    # save the changes permanently
    db_conn.commit()

    return cur.lastrowid


def add_new_customer(db_conn, data):
    # add record into databse
    query = f"""
                INSERT INTO customer (fname, lname, employee_id, phone, city, country, language, lead_generated_at) 
                VALUES (%(fname)s, %(lname)s, %(employee_id)s, %(phone)s, %(city)s, %(country)s, %(language)s, %(lead_generated_at)s)
            """
    cur = db_conn.cursor()
    cur.execute(
        query,
        {
            "fname": data.get("fname"),
            "lname": data.get("lname"),
            "employee_id": data.get("employee_id"),
            "phone": data.get("phone"),
            "city": data.get("city"),
            "country": data.get("country"),
            "language": data.get("language"),
            "lead_generated_at": data.get("lead_generated_at"),
        },
    )

    # save the changes permanently
    db_conn.commit()
    return cur.lastrowid


def update_customer(db_conn, cust_id, data: dict):
    cursor = db_conn.cursor()
    sql = "UPDATE customer SET"
    for k, v in data.items():
        sql += f" {k} = '{v}',"
    sql = sql[:-1]
    sql += f" WHERE id={cust_id}"
    isUpdated = cursor.execute(sql)
    db_conn.commit()
    return True if isUpdated == 1 else False

def get_all_services(db_conn, name, price):
    query = "SELECT * FROM service"
    if name is not None or price is not None:
        query += " WHERE "
        if name is not None:
            query += f"name LIKE '{name}'"
            if price is not None:
                query += " AND "
        if price is not None:
            query += f"price LIKE '{price}'"
    print(query)
    cur = db_conn.cursor()
    cur.execute(query)
    return cur.fetchall()


def get_service_by_id(db_conn, service_id):
    # fetch data from db
    query = f"SELECT * FROM service WHERE id=%(service_id)s"
    cur = db_conn.cursor()
    cur.execute(query, {"service_id": service_id})

    return cur.fetchone()

def update_service(db_conn, ser_id, data: dict):
    cursor = db_conn.cursor()
    sql = "UPDATE service SET"
    for k, v in data.items():
        sql += f" {k} = '{v}',"
    sql = sql[:-1]
    sql += f" WHERE id={ser_id}"
    isUpdated = cursor.execute(sql)
    db_conn.commit()
    return True if isUpdated == 1 else False

def delete_service_by_id(db_conn, ser_id):
    query = f"DELETE FROM service WHERE id=%(service_id)s"
    cur = db_conn.cursor()
    isDeleted = cur.execute(query, {"service_id": ser_id})
    db_conn.commit()
    return True if isDeleted == 1 else False

# --- order

def get_all_orders(db_conn, cust_id, ser_id):
    query = "SELECT * FROM flask2.order"
    if cust_id is not None or ser_id is not None:
        query += " WHERE "
        if cust_id is not None:
            query += f"customer_id LIKE '{cust_id}'"
            if ser_id is not None:
                query += " AND "
        if ser_id is not None:
            query += f"service_id LIKE '{ser_id}'"
    print(query)
    cur = db_conn.cursor()
    cur.execute(query)
    return cur.fetchall()


def get_order_by_id(db_conn, order_id):
    # fetch data from db
    query = f"SELECT * FROM flask2.order WHERE id=%(order_id)s"
    cur = db_conn.cursor()
    cur.execute(query, {"order_id": order_id})

    return cur.fetchone()

def add_new_order(db_conn, data):
    # add record into databse
    query = f"""
                INSERT INTO flask2.order (customer_id, service_id) VALUES (%(customer_id)s, %(service_id)s)
            """
    cur = db_conn.cursor()
    cur.execute(
        query,
        {
            "customer_id": data.get("customer_id"),
            "service_id": data.get("service_id"),
        },
    )

    # save the changes permanently
    db_conn.commit()

    return cur.lastrowid

def delete_order_by_id(db_conn, order_id):
    query = f"DELETE FROM flask2.order WHERE id=%(order_id)s"
    cur = db_conn.cursor()
    isDeleted = cur.execute(query, {"order_id": order_id})
    db_conn.commit()
    return True if isDeleted == 1 else False