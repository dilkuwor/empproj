from flask import Flask
from flask_restful import Api
from timeapi.resources.employee import Employee, EmployeeCollection
from timeapi.resources.project import Project, ProjectCollection
from timeapi.resources.project_employee import ProjectEmployee
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec


app = Flask(__name__)
api = Api(app)

api = Api(app)
api.add_resource(Employee, '/employees/<string:employee_id>')
api.add_resource(EmployeeCollection, '/employees')
api.add_resource(ProjectCollection, '/projects')
api.add_resource(Project, '/projects/<string:project_id>')
api.add_resource(ProjectEmployee, '/projects/<string:project_id>/employees')

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='timeapi',
        version='v1',
        plugins=['apispec.ext.marshmallow'],
    ),
    'APISPEC_SWAGGER_URL': '/spec/',
})
docs = FlaskApiSpec(app)

docs.register(Employee)
docs.register(EmployeeCollection)
docs.register(ProjectCollection)
docs.register(Project)
docs.register(ProjectEmployee)

'''
if __name__ == '__main__':

    app.run(debug=True)
'''