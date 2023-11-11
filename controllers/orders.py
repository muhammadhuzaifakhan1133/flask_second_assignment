import db, query
import logging
logging.basicConfig(level=logging.DEBUG)
from flask import request
log = logging.getLogger("flask-app")

def is_valid_order_data(data):
    error_msg = None

    if data.get("service_id") is None or len(data.get("service_id").strip()) == 0:
        error_msg = "service_id field is required"

    if data.get("customer_id") is None or len(data.get("customer_id").strip()) == 0:
        error_msg = "customer_id field is required"

    return error_msg

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