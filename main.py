from flask import Flask
from flask import request, Response
from flask import json
from psycopg2.errors import UniqueViolation

app = Flask(__name__)

import psycopg2

conn = psycopg2.connect(
        host="tam-postgres.postgres.database.azure.com",
        database="postgres",
        # user='postgres',
        user = "postgres@tam-postgres",
        password='Tamana@19',
        port=5432)

class RollNumberNotPresentError(Exception):
    pass

@app.route("/hello")
def hello():
    return Response(json.dumps({"Hello":"World"}), status=200, mimetype='application/json')

@app.route("/StudentDetails/<roll_no>", methods=['GET'])
def StudentDetails(roll_no):
    roll_no = roll_no
    print(roll_no)
    query = 'select * from public."student" s JOIN public."sddress" a on s.roll_no = a.roll_no where s."roll_no"='+str(roll_no)+';'
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    print(result)
    firstname = result[0][1]
    lastname = result[0][2]
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
    jd = json.dumps(
    {
        "roll_no": roll_no,
        "firstname": firstname,
        "lastname": lastname,
        "address": address_list
    })
    return Response(jd, status=200, mimetype='application/json')

@app.route("/updateStudentDetails", methods = ["POST"])
def UpdateDetails():
    data = request.get_json()
    r_no = data['roll_no']
    fname = data['firstname']
    lname = data['lastname']
    address = data['address']
    query1 = f"INSERT INTO public.\"student\"(\"roll_no\",\"firstname\",\"lastname\") VALUES({str(r_no)},\'{fname}\',\'{lname}\');"
    cur = conn.cursor()

    try:
        if r_no == "":
            raise RollNumberNotPresentError()
        cur.execute(query1)
        message = "Details updated successfully"
    except UniqueViolation as ue:
        print(ue)
        message = "Roll no already exists in database"
        jd = json.dumps({"status": "Failed",
                         "message": message})
        return Response(jd, status=500, mimetype='application/json')

    except RollNumberNotPresentError as e:
        message = "Roll no is missing"
        jd = json.dumps({"status": "Failed",
                         "message": message})
        return Response(jd, status=500, mimetype='application/json')
    conn.commit()
    for each_address in address:
        print(each_address)
        address_type = each_address.get('AddressType')
        Hno = each_address.get('Hno')
        area = each_address.get('area')
        city = each_address.get('city')
        state = each_address.get('state')
        pincode = each_address.get('pincode')
        query2 = f"INSERT INTO public.\"address\"(\"roll_no\",\"address_type\",\"hno\",\"area\",\"city\",\"state\",\"pincode\") " \
                 f"VALUES({str(r_no)},'{address_type}','{Hno}','{area}','{city}','{state}',{str(pincode)});"
        cur.execute(query2)
        conn.commit()
    cur.close()
    jd = json.dumps({"status": "Sucsess",
                     "message" : message})
    return Response(jd, status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run()
