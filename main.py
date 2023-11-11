from flask import Flask
from controllers import customers, employees, orders, services

app = Flask(__name__)

# employee services
app.add_url_rule("/employee", methods=['GET'], view_func=employees.get_employees)
app.add_url_rule("/employee/<user_id>", methods=['GET'], view_func=employees.get_employee_profile)
app.add_url_rule("/employee", methods=['POST'], view_func=employees.add_new_employee)

# customer services
app.add_url_rule("/customer", methods=['GET'], view_func=customers.get_customers)
app.add_url_rule("/customer/<cust_id>", methods=['GET'], view_func=customers.get_customer_profile)
app.add_url_rule("/customer/<cust_id>", methods=['DELETE'], view_func=customers.delete_customer_profile)
app.add_url_rule("/customer/<cust_id>", methods=['PUT'], view_func=customers.update_customer)
app.add_url_rule("/customer", methods=["POST"], view_func=customers.add_new_customer)


# service services
app.add_url_rule("/service", methods=['POST'], view_func=services.add_new_service)
app.add_url_rule("/service", methods=['GET'], view_func=services.get_services)
app.add_url_rule("/service/<ser_id>", methods=['GET'], view_func=services.get_single_service)
app.add_url_rule("/service/<ser_id>", methods=['PUT'], view_func=services.update_service)
app.add_url_rule("/service/<ser_id>", methods=['DELETE'], view_func=services.delete_service_profile)


# order services
app.add_url_rule("/order", methods=['POST'], view_func=orders.add_new_order)
app.add_url_rule("/order", methods=['GET'], view_func=orders.get_orders)
app.add_url_rule("/order/<order_id>", methods=['GET'], view_func=orders.get_single_order)
app.add_url_rule("/order/<order_id>", methods=['DELETE'], view_func=orders.delete_order_profile)


if __name__  == "__main__":
    app.run(
        debug=True,
        port=3000
    )