import random
import string
import requests


def random_char(char_num):
    return "".join(random.choice(string.ascii_letters) for _ in range(char_num))


# add new employee
def add_new_employee():
    url = "http://localhost:3000/employee"

    r = requests.post(
        url,
        json={
            "fname": "muhammad",
            "lname": "danish",
            "email": random_char(5) + "@gmail.com",
        },
    )
    response_data = r.json()
    print(response_data)
    return response_data["data"]["id"]


def get_employee_by_id(employee_id):
    url = "http://localhost:3000/employee" + "/" + str(employee_id)
    r = requests.get(url)
    response_data = r.json()
    print(response_data)


def get_customer_by_id(customer_id):
    url = "http://localhost:3000/customer" + "/" + str(customer_id)
    r = requests.get(url)
    response_data = r.json()
    print(response_data)

def delete_customer_by_id(customer_id):
    url = "http://localhost:3000/customer" + "/" + str(customer_id)
    r = requests.delete(url)
    response_data = r.json()
    print(response_data)


def update_customer(customer_id):
    url = "http://localhost:3000/customer" + "/" + str(customer_id)
    r = requests.put(
        url,
        json={
            # "fname": "muhammad",
            "lname": "nabeel",
            # "employee_id": "1",
            # "phone": "123456789",
            # "city": "Lahore",
            # "country": "Pakistan",
            # "language": "Eng",
            # "lead_generated_at": "2023-10-10",
        },
    )
    response_data = r.json()
    print(response_data)

def add_new_customer():
    url = "http://localhost:3000/customer"
    r = requests.post(
        url,
        json={
            "fname": "muhammad",
            "lname": "nabeel",
            "employee_id": "1",
            "phone": "123456789",
            "city": "Karachi",
            "country": "Pakistan",
            "language": "Eng",
            "lead_generated_at": "2023-10-10",
        },
    )
    response_data = r.json()
    print(response_data)
    return response_data["data"]["id"]

def add_new_service():
    url = "http://localhost:3000/service"
    r = requests.post(
        url,
        json={
            "name": "serv-01",
            "price": "15",
        },
    )
    response_data = r.json()
    print(response_data)
    return response_data["data"]["id"]


def get_all_employees():
    url = "http://localhost:3000/employee"
    r = requests.get(url)
    response_data = r.json()
    print(response_data)

def get_all_customers():
    url = "http://localhost:3000/customer"
    r = requests.get(url, params={
        "employee_id": "1",
        "name": "ali"
    })
    response_data = r.json()
    print(response_data)

def get_all_services():
    url = "http://localhost:3000/service"
    r = requests.get(url)
    response_data = r.json()
    print(response_data)

def get_service_by_id(service_id):
    url = "http://localhost:3000/service" + "/" + str(service_id)
    r = requests.get(url)
    response_data = r.json()
    print(response_data)

def delete_service_by_id(service_id):
    url = "http://localhost:3000/service" + "/" + str(service_id)
    r = requests.delete(url)
    response_data = r.json()
    print(response_data)


def update_service(service_id):
    url = "http://localhost:3000/service" + "/" + str(service_id)
    r = requests.put(
        url,
        json={
            "name": "ser-02",
        },
    )
    response_data = r.json()
    print(response_data)

# -- order

def add_new_order():
    url = "http://localhost:3000/order"
    r = requests.post(
        url,
        json={
            "service_id": "1",
            "customer_id": "5",
        },
    )
    response_data = r.json()
    print(response_data)
    if r.status_code == 200:
        return response_data["data"]["id"]

def get_all_orders():
    url = "http://localhost:3000/order"
    r = requests.get(url)
    response_data = r.json()
    print(response_data)

def get_order_by_id(order_id):
    url = "http://localhost:3000/order" + "/" + str(order_id)
    r = requests.get(url)
    response_data = r.json()
    print(response_data)

def delete_order_by_id(order_id):
    url = "http://localhost:3000/order" + "/" + str(order_id)
    r = requests.delete(url)
    response_data = r.json()
    print(response_data)


# employee_id = add_new_employee()
# get_employee_by_id(employee_id)
# get_all_employees()
# customer_id = add_new_customer()
# get_customer_by_id(customer_id)
# get_all_customers()
# delete_customer_by_id(customer_id)
# update_customer(5)
# service_id = add_new_service()
# get_all_services()
# get_service_by_id(service_id)
# delete_service_by_id(2)
# order_id = add_new_order()
# get_all_orders()
# get_order_by_id(order_id)
# delete_order_by_id(2)


