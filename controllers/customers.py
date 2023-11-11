import db, query
import logging
logging.basicConfig(level=logging.DEBUG)
from flask import request
log = logging.getLogger("flask-app")

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