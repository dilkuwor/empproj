# project.py
from flask_restful import fields, marshal_with, reqparse, Resource
from pymongo import MongoClient  # Database connector
from bson.objectid import ObjectId
from flask_apispec import MethodResource

client = MongoClient('localhost', 27017)
db = client.timeapi

post_parser = reqparse.RequestParser()

post_parser.add_argument(
    'employee_id', required=True, help='The project employees field is required'
)

project_employees_fields = {
    'project_id': fields.String,
    'employee_id': fields.List(fields.String)
}


def update_project_employees(project_id, employee_ids):
    # update employee id in project document
    db.projects.update({'_id': ObjectId(project_id)}, {'$set': {'project_employees': ",".join(employee_ids)}
                                                       })


def update_employee_projects(employee_id, project_ids):
    # update project id in employee document
    db.employees.update({'_id': ObjectId(employee_id)}, {'$set': {'employee_projects': ",".join(
        project_ids)}})


def find_project_employees(project_id):
    project = db.projects.find_one({'_id': ObjectId(project_id)})
    if project is not None:
        try:
            return project['project_employees'].split(',')
        except:
            pass
    return []


def find_employee_projects(employee_id):
    employee = db.employees.find_one({'_id': ObjectId(employee_id)})
    if employee is not None:
        try:
            return employee['employee_projects'].split(',')
        except:
            pass
    return []


class ProjectEmployee(MethodResource):

    def put(self, project_id):

        args = post_parser.parse_args()
        employee_id = args['employee_id']
        employee_ids = find_project_employees(project_id)
        if employee_id not in employee_ids:
            employee_ids.append(employee_id)
            update_project_employees(project_id, employee_ids)

        # update project id in employee collection
        employee_project_ids = find_employee_projects(employee_id)
        if project_id not in employee_project_ids:
            employee_project_ids.append(project_id)
            update_employee_projects(employee_id, employee_project_ids)

        return {"project_id": project_id, "project_employees": employee_ids}, 201

    def delete(self, project_id):

        args = post_parser.parse_args()
        employee_id = args['employee_id']
        employee_ids = find_project_employees(project_id)
        if employee_id in employee_ids:
            employee_ids.remove(employee_id)
            update_project_employees(project_id, employee_ids)

        # update project id in employee collection
        employee_project_ids = find_employee_projects(employee_id)
        if project_id not in employee_project_ids:
            employee_project_ids.remove(project_id)
            update_employee_projects(employee_id, employee_project_ids)

        return '', 204
