# project.py
from flask_restful import fields, marshal_with, reqparse, Resource
from pymongo import MongoClient  # Database connector
from bson.objectid import ObjectId
from flask_apispec import MethodResource

client = MongoClient('localhost', 27017)
db = client.timeapi


post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'project_name', required=True, help='The project name field is required'
)
post_parser.add_argument(
    'project_start_date', required=True, help='The project name field is required'
)
post_parser.add_argument(
    'project_end_date', required=True, help='The project name field is required'
)
post_parser.add_argument(
    'project_employees'
)

project_fields = {
    'project_id': fields.String,
    'project_name': fields.String,
    'project_start_date': fields.DateTime,
    'project_end_date': fields.String,
    'project_employees': fields.String
}
project_fields_response = project_fields
project_fields_response['project_employee'] = fields.Nested({
        'employee_id': fields.String,
        'first_name': fields.String,
        'last_name': fields.String,
        'email': fields.String,
    })


class ProjectCollection(MethodResource):

    @marshal_with(project_fields_response)
    def get(self):
        cursor = db.projects.find()
        projects = []
        for project in cursor:
            project['project_id'] = project['_id']
            projects.append(project)
        return projects

    @marshal_with(project_fields)
    def post(self):
        args = post_parser.parse_args()
        print(args)
        project_id = db.projects.insert(args)
        project = db.projects.find_one({'_id': project_id})
        project['project_id'] = project_id
        return project, 201


class Project(MethodResource):

    @marshal_with(project_fields_response)
    def get(self, project_id):
        project = db.projects.find_one({'_id': ObjectId(project_id)})
        return project

    def delete(self, project_id):
        db.projects.remove({'_id': ObjectId(project_id)})
        return 'Project has been deleted', 204

    @marshal_with(project_fields)
    def put(self, project_id):
        args = post_parser.parse_args()
        db.projects.update({'_id': ObjectId(project_id)}, {'$set': {'project_name': args['project_name'],
                                                                    'project_start_date': args['project_start_date'],
                                                                    'project_end_date': args['project_end_date']}})
        project = db.projects.find_one({'_id': ObjectId(project_id)})
        project['project_id'] = project_id
        return project, 201
