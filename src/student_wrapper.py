from flask import json
import configparser
from utilities.exceptions import PrimaryParameterNotPresentError
from psycopg2.errors import UniqueViolation
from utilities.db_utils import execute_query
import os

config = configparser.ConfigParser()
path = os.path.join("utilities", "config.ini")
config.read(path)

def get_student_details(roll_no):
    query = config["DATABASE"]["GET_STUDENT_DATA"]
    query = query.format(roll_no=roll_no)
    result = execute_query(query)
    if len(result) == 0:
        return json.dumps({"message":"The roll_no does not exists in database"}), 404
    firstname = result[0][1]
    lastname = result[0][2]
    address_list = fetch_address_list(result)
    jd = json.dumps(
        {
            "roll_no": roll_no,
            "firstname": firstname,
            "lastname": lastname,
            "address": address_list
        })
    return jd, 200


def fetch_address_list(result):
    address_list = []
    for each_address in result:
        address_type = each_address[1]
        hno = each_address[2]
        area = each_address[3]
        city = each_address[4]
        state = each_address[5]
        pincode = each_address[6]
        address_list.append({"AddressType": address_type,
                             "Hno": hno,
                             "area": area,
                             "city": city,
                             "state": state,
                             "pincode": pincode})
    return address_list


def update_student_data(data):
    r_no = data['roll_no']
    fname = data['firstname']
    lname = data['lastname']
    address = data['address']
    query1 = config["DATABASE"]["UPDATE_STUDENT_DETAILS"]
    query1 = query1.format(r_no=r_no, fname=fname, lname=lname)
    try:
        check_roll_no_and_execute_query(r_no, query1)
    except PrimaryParameterNotPresentError as e:
        message = "Primary parameter is missing"
        jd = json.dumps({"status": "Failed",
                         "message": message})
        return jd

    except UniqueViolation as ue:
        print(ue)
        message = "Roll no already exists in database"
        jd = json.dumps({"status": "Failed",
                         "message": message})
        return jd
    populate_insert_address_data(address, r_no)
    message = "Details updated successfully"
    jd = json.dumps({"status": "Success",
                     "message": message})
    return jd


def populate_insert_address_data(address, r_no):
    for each_address in address:
        print(each_address)
        address_type = each_address.get('AddressType')
        hno = each_address.get('Hno')
        area = each_address.get('area')
        city = each_address.get('city')
        state = each_address.get('state')
        pincode = each_address.get('pincode')
        query2 = config["DATABASE"]["UPDATE_ADDRESS"]
        query2 = query2.format(
            r_no=r_no,
            address_type=address_type,
            Hno=hno,
            area=area,
            city=city,
            state=state,
            pincode=pincode
        )
        execute_query(query2)


def check_roll_no_and_execute_query(prime_param, query1):
    if prime_param == "":
        raise PrimaryParameterNotPresentError()
    else:
        execute_query(query1)


