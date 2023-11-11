import logging
logging.basicConfig(level=logging.DEBUG)
from flask import Flask, request
import db, query

app = Flask(__name__)
log = logging.getLogger("flask-app")

@app.route("/customer", methods=['GET'])
def get_customers():
    log.info("get all customers")
    employee_id = request.args.get("employee_id")
    name = request.args.get("name")
    conn = db.mysqlconnect()
    customers = query.get_all_customers(conn, employee_id, name)
    db.disconnect(conn)
    if len(customers) == 0:
        log.warning("customer not found")
        return {
            "data": [],
            "message": "customer not found"
        }
    return {
        "data": customers
    }, 200


@app.route("/employee", methods=['GET'])
def get_employees():
    log.info("get all employees")

    conn = db.mysqlconnect()
    employees = query.get_all_employees(conn)
    db.disconnect(conn)
    
    if len(employees) == 0:
        log.warning("employee not found")
        return {
            "data": [],
            "message": "employee not found"
        }, 200

    return {
        "data": employees
    }, 200

@app.route("/customer/<cust_id>", methods=['GET'])
def get_customer_profile(cust_id):
    if cust_id.isdigit() == False or int(cust_id) <= 0:
        log.error("Invalid customer id")
        return {
            "error": {"message": "invalid id"}
        }, 400
    conn = db.mysqlconnect()
    customer = query.get_customer_by_id(conn, cust_id)
    db.disconnect(conn)

    if customer is None:
        log.warning("customer not found")
        return {
            "error": {"message": "customer not found"}
        }, 400
    
    return {
        "data": customer
    }, 200

@app.route("/customer/<cust_id>", methods=['DELETE'])
def delete_customer_profile(cust_id):
    if cust_id.isdigit() == False or int(cust_id) <= 0:
        log.error("Invalid customer id")
        return {
            "error": {"message": "invalid id"}
        }, 400
    conn = db.mysqlconnect()
    isDeleted = query.delete_customer_by_id(conn, cust_id)
    db.disconnect(conn)

    if isDeleted == False or isDeleted is None:
        log.warning("customer not found")
        return {
            "error": {"message": "customer not found"}
        }, 400
    
    return {
        "message": "customer deleted successfully" 
    }, 200

@app.route("/employee/<user_id>", methods=['GET'])
def get_employee_profile(user_id):
    print("user_id", user_id)
    if user_id.isdigit() == False or int(user_id) <= 0:
        log.error("invalid ID")
        return {
            "error": {"message": "invalid id"}
        }, 400

    conn = db.mysqlconnect()
    employee = query.get_employee_by_id(conn, user_id)
    db.disconnect(conn)

    if employee is None:
        log.warning("employee not found")
        return {
            "error": {"message": "employee not found"}
        }, 400

    return {
        "data": employee
    }, 200

@app.route("/customer/<cust_id>", methods=['PUT'])
def update_customer(cust_id):
    if cust_id.isdigit() == False or int(cust_id) <= 0:
        log.error("Invalid customer id")
        return {
            "error": {"message": "invalid id"}
        }, 400 
    data = request.get_json()
    if all([True if v==None else False for v in data.values()]):
        return {
            "error": {"message": "Please enter atleast one field"}
        }, 400
    conn = db.mysqlconnect()
    isUpdated = query.update_customer(conn, cust_id, data)
    if isUpdated == False or isUpdated is None:
        log.warning("customer not found")
        return {
            "error": {"message": "customer not found"}
        }, 400
    
    return {
        "message": "customer updated successfully" 
    }, 200

def is_valid_customer_data(data):
    error_msg = None
    if data.get("fname") is None or len(data.get("fname").strip()) == 0:
        error_msg = "fname field is required"

    if data.get("lname") is None or len(data.get("lname").strip()) == 0:
        error_msg = "lname field is required"

    if data.get("phone") is None or len(data.get("phone").strip()) == 0:
        error_msg = "phone field is required"
    
    if data.get("lead_generated_at") is None or len(data.get("lead_generated_at").strip()) == 0:
        error_msg = "lead_generated_at field is required"

    if data.get("employee_id") is None or len(data.get("employee_id").strip()) == 0:
        error_msg = "employee_id field is required"
    else:
        if (data.get("employee_id").isdigit() == False or int(data.get("employee_id")) <= 0):
            error_msg = "employee_id field is invalid"

    return error_msg
    

def is_valid_employee_data(data):
    error_msg = None

    if data.get("fname") is None or len(data.get("fname").strip()) == 0:
        error_msg = "fname field is required"

    if data.get("lname") is None or len(data.get("lname").strip()) == 0:
        error_msg = "lname field is required"

    if data.get("email") is None or len(data.get("email").strip()) == 0:
        error_msg = "email field is required"

    return error_msg

def is_valid_service_data(data):
    error_msg = None

    if data.get("name") is None or len(data.get("name").strip()) == 0:
        error_msg = "name field is required"

    if data.get("price") is None or len(data.get("price").strip()) == 0:
        error_msg = "price field is required"

    return error_msg

@app.route("/customer", methods=["POST"])
def add_new_customer():
    if not request.is_json:
        return {
            "error": {
                "message": "API accepts json data"
            }
        }, 400
    data = request.get_json()
    if (error := is_valid_customer_data(data)) is not None:
        return {
            "error": {
                "message": error,
            }
        }, 400
    
    conn = db.mysqlconnect()
    customer_id = query.add_new_customer(conn, data)
    db.disconnect(conn)

    log.info("new customer added")
    return {
        "data": {"id": customer_id}
    }, 200


@app.route("/employee", methods=['POST'])
def add_new_employee():
    if not request.is_json:
        return {
            "error": {"message": "API Accepts json data"}
        }, 400
    
    data = request.get_json()
    if (error := is_valid_employee_data(data)) is not None:
        return {
            "error": {"message": error}
        }, 400
    
    conn = db.mysqlconnect()
    employee_id = query.add_new_employee(conn, data)
    db.disconnect(conn)

    log.info("new employee added")
    return {
        "data": {"id": employee_id}
    }, 200

@app.route("/service", methods=['POST'])
def add_new_service():
    if not request.is_json:
        return {
            "error": {"message": "API Accepts json data"}
        }, 400
    
    data = request.get_json()
    if (error := is_valid_service_data(data)) is not None:
        return {
            "error": {"message": error}
        }, 400
    
    conn = db.mysqlconnect()
    employee_id = query.add_new_service(conn, data)
    db.disconnect(conn)

    log.info("new service added")
    return {
        "data": {"id": employee_id}
    }, 200

@app.route("/service", methods=['GET'])
def get_services():
    log.info("get all services")
    price = request.args.get("price")
    name = request.args.get("name")
    conn = db.mysqlconnect()
    services = query.get_all_services(conn, name, price)
    db.disconnect(conn)
    if len(services) == 0:
        log.warning("service not found")
        return {
            "data": [],
            "message": "service not found"
        }
    return {
        "data": services
    }, 200

@app.route("/service/<ser_id>", methods=['GET'])
def get_single_service(ser_id):
    if ser_id.isdigit() == False or int(ser_id) <= 0:
        log.error("Invalid service id")
        return {
            "error": {"message": "invalid id"}
        }, 400
    conn = db.mysqlconnect()
    service = query.get_service_by_id(conn, ser_id)
    db.disconnect(conn)

    if service is None:
        log.warning("service not found")
        return {
            "error": {"message": "service not found"}
        }, 400
    
    return {
        "data": service
    }, 200

@app.route("/service/<ser_id>", methods=['PUT'])
def update_service(ser_id):
    if ser_id.isdigit() == False or int(ser_id) <= 0:
        log.error("Invalid service id")
        return {
            "error": {"message": "invalid id"}
        }, 400 
    data = request.get_json()
    if all([True if v==None else False for v in data.values()]):
        return {
            "error": {"message": "Please enter atleast one field"}
        }, 400
    conn = db.mysqlconnect()
    isUpdated = query.update_service(conn, ser_id, data)
    if isUpdated == False or isUpdated is None:
        log.warning("service not found")
        return {
            "error": {"message": "service not found"}
        }, 400
    
    return {
        "message": "service updated successfully" 
    }, 200

@app.route("/service/<ser_id>", methods=['DELETE'])
def delete_service_profile(ser_id):
    if ser_id.isdigit() == False or int(ser_id) <= 0:
        log.error("Invalid service id")
        return {
            "error": {"message": "invalid id"}
        }, 400
    conn = db.mysqlconnect()
    isDeleted = query.delete_service_by_id(conn, ser_id)
    db.disconnect(conn)

    if isDeleted == False or isDeleted is None:
        log.warning("service not found")
        return {
            "error": {"message": "service not found"}
        }, 400
    
    return {
        "message": "service deleted successfully" 
    }, 200

# --- order

def is_valid_order_data(data):
    error_msg = None

    if data.get("service_id") is None or len(data.get("service_id").strip()) == 0:
        error_msg = "service_id field is required"

    if data.get("customer_id") is None or len(data.get("customer_id").strip()) == 0:
        error_msg = "customer_id field is required"

    return error_msg

@app.route("/order", methods=['POST'])
def add_new_order():
    if not request.is_json:
        return {
            "error": {"message": "API Accepts json data"}
        }, 400
    
    data = request.get_json()
    if (error := is_valid_order_data(data)) is not None:
        return {
            "error": {"message": error}
        }, 400
    
    conn = db.mysqlconnect()
    service_id = query.add_new_order(conn, data)
    db.disconnect(conn)

    log.info("new order added")
    return {
        "data": {"id": service_id}
    }, 200

@app.route("/order", methods=['GET'])
def get_orders():
    log.info("get all orders")
    ser_id = request.args.get("service_id")
    cust_id = request.args.get("customer_id")
    conn = db.mysqlconnect()
    orders = query.get_all_orders(conn, cust_id, ser_id)
    db.disconnect(conn)
    if len(orders) == 0:
        log.warning("order not found")
        return {
            "data": [],
            "message": "order not found"
        }
    return {
        "data": orders
    }, 200

@app.route("/order/<order_id>", methods=['GET'])
def get_single_order(order_id):
    if order_id.isdigit() == False or int(order_id) <= 0:
        log.error("Invalid order id")
        return {
            "error": {"message": "invalid id"}
        }, 400
    conn = db.mysqlconnect()
    order = query.get_order_by_id(conn, order_id)
    db.disconnect(conn)

    if order is None:
        log.warning("order not found")
        return {
            "error": {"message": "order not found"}
        }, 400
    
    return {
        "data": order
    }, 200

@app.route("/order/<order_id>", methods=['DELETE'])
def delete_order_profile(order_id):
    if order_id.isdigit() == False or int(order_id) <= 0:
        log.error("Invalid order id")
        return {
            "error": {"message": "invalid id"}
        }, 400
    conn = db.mysqlconnect()
    isDeleted = query.delete_order_by_id(conn, order_id)
    db.disconnect(conn)

    if isDeleted == False or isDeleted is None:
        log.warning("order not found")
        return {
            "error": {"message": "order not found"}
        }, 400
    
    return {
        "message": "order deleted successfully" 
    }, 200


if __name__  == "__main__":
    app.run(
        debug=True,
        port=3000
    )