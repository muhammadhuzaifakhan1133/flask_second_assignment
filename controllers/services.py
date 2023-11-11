import db, query
import logging
logging.basicConfig(level=logging.DEBUG)
from flask import request
log = logging.getLogger("flask-app")

def is_valid_service_data(data):
    error_msg = None

    if data.get("name") is None or len(data.get("name").strip()) == 0:
        error_msg = "name field is required"

    if data.get("price") is None or len(data.get("price").strip()) == 0:
        error_msg = "price field is required"

    return error_msg

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