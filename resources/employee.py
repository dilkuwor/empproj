# employee.py
from flask import abort
from flask_restful import fields, marshal_with, reqparse, Resource
from validate_email import validate_email
from pymongo import MongoClient  # Database connector
from bson.objectid import ObjectId
from flask_apispec import MethodResource

client = MongoClient('localhost', 27017)
db = client.timeapi


def email(email_str):
    """Return email_str if valid, raise an exception in other case."""
    if validate_email(email_str):
        return email_str
    else:
        raise ValueError('{} is not a valid email'.format(email_str))


post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'first_name', required=True, help='The first name field is required'
)
post_parser.add_argument(
    'last_name', required=True, help='The last name field is required'
)
post_parser.add_argument(
    'email', dest='email', type=email, help='The email field is required'
)

employee_fields = {
    'employee_id': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'employee_projects': fields.Nested({
        'project_id': fields.String,
        'project_name': fields.String,
        'project_start_date': fields.DateTime,
        'project_end_date': fields.DateTime
    })
}

# check if employee exist in collection or not, if does not exist abort the request
def abort_if_employee_doesnot_exist(employee_id):
    employee = db.employees.find({'_id': ObjectId(employee_id)}).limit(0)
    if employee.count() == 0:
        abort(404)


class EmployeeCollection(MethodResource):

    @marshal_with(employee_fields)
    def get(self):
        cursor = db.employees.find()
        employees = []
        for employee in cursor:
            employee['employee_id'] = employee['_id']
            employees.append(employee)
        return employees

    @marshal_with(employee_fields)
    def post(self):
        args = post_parser.parse_args()
        employee_id = db.employees.insert(args)
        employee = db.employees.find_one({'_id': employee_id})
        employee['employee_id'] = employee_id
        return employee, 201


class Employee(MethodResource):

    @marshal_with(employee_fields)
    def get(self, employee_id):
        employee = db.employees.find_one({'_id': ObjectId(employee_id)})
        return employee

    def delete(self, employee_id):
        abort_if_employee_doesnot_exist(employee_id)
        db.employees.remove({'_id': ObjectId(employee_id)})
        return 'Employee has been deleted', 204

    @marshal_with(employee_fields)
    def put(self, employee_id):
        args = post_parser.parse_args()
        abort_if_employee_doesnot_exist(employee_id)
        db.employees.update({'_id': ObjectId(employee_id)}, {'$set': {'first_name': args['first_name'],
                                                                      'last_name': args['last_name'],
                                                                      'email': args['email']}})
        employee = db.employees.find_one({'_id': ObjectId(employee_id)})
        employee['employee_id'] = employee_id
        return employee, 201
