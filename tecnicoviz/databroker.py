from flask import Flask, jsonify, request, Response
from flask_restful import Resource, Api
import json
from backend import getDegrees
from backend import getCourses
from backend import getStudents
from backend import getTeachers
from backend import getColumnNames
from backend import getTerms
import os
from werkzeug.contrib.cache import SimpleCache

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app)
cache = SimpleCache(threshold=20)

class Degrees(Resource):
    def get(self):
        return isCached("degrees", {})
    
class Degree(Resource):
    def get(self, ID):
        condition = {}
        condition["ID"] = ID
        return isCached("degrees", condition)

class DegreeCourses(Resource):
    def get(self, degreeId):
        condition = {}
        condition["degreeId"] = degreeId
        return isCached("courses", condition)
    
class CourseDegrees(Resource):
    def get(self, courseAcronym):
        condition = {}
        condition["courseAcronym"] = courseAcronym
        return isCached("courses", condition)
    
class Courses(Resource):
    def get(self):
        return isCached("courses", {})
    
class Course(Resource):
    def get(self, ID):
        condition = {}
        condition["ID"] = ID
        return isCached("courses", condition)

class CourseStudents(Resource):
    def get(self, courseId):
        condition = {}
        condition["courseId"] = courseId
        return isCached("students", condition)
    
class CourseTeachers(Resource):
    def get(self, courseId):
        condition = {}
        condition["courseId"] = courseId
        return isCached("teachers", condition)

class Students(Resource):
    def get(self):
        return isCached("students", {})
    
class Student(Resource):
    def get(self, username):
        condition = {}
        condition["username"] = username
        return isCached("students", condition)
    
class Teachers(Resource):
    def get(self):
        return isCached("teachers", {})
    
class Teacher(Resource):
    def get(self, username):
        condition = {}
        condition["username"] = username
        return isCached("teachers", condition)

class Terms(Resource):
    def get(self):
        return isCached("terms", {})

def requestDB(table, parameters):
    table_map = {
                'degrees' : getDegrees,
                'courses' : getCourses,
                'students' : getStudents,
                'teachers' : getTeachers,
                'terms' : getTerms
            }
    select = []
    columnNames = getColumnNames(table)
    for row in columnNames:
        select.append("".join(row))
    jsonFile = []
    queryResult = table_map[table](parameters)
    for result in queryResult:
        tempDict = {}        
        for i in range(0,len(select)):
            tempDict[select[i]] = result[i]
        jsonFile.append(tempDict)
    parsedJson = jsonify(jsonFile)
    return parsedJson

@app.route('/')
def root():
    return app.send_static_file('index.html')

def isCached(table, condition):
    parameters = request.args.to_dict()
    parameters = {**condition, **parameters}
    identifier = str(table + str(parameters) + request.remote_addr).lower()
    item = cache.get(identifier)
    if item is not None:
        return item
    else:
        item = requestDB(table, parameters)
        cache.set(identifier, item, timeout=60 * 5)
        return item
        
#@app.route("/degrees/")
#def degrees():
 #   select, where = retrieveParameters('degrees')
  #  item = isCached(select, where, 'degrees')
   # def generate(): 
    #    for i in range(0, len(item), 10):
     #       yield json.dumps(gen(i,item), sort_keys = True, ensure_ascii=False, indent = 4)
    #return Response(generate(), content_type='application/json')

api.add_resource(Degrees, '/degrees/')
api.add_resource(Degree, '/degrees/<int:ID>')
api.add_resource(DegreeCourses, '/degrees/<int:degreeId>/courses')
api.add_resource(Courses, '/courses/')
api.add_resource(CourseDegrees, '/courses/<string:courseAcronym>')
api.add_resource(Course, '/courses/<int:ID>')
api.add_resource(CourseStudents, '/courses/<int:courseId>/students')
api.add_resource(CourseTeachers, '/courses/<int:courseId>/teachers')
api.add_resource(Students, '/students/')
api.add_resource(Student, '/students/<string:username>')
api.add_resource(Teachers, '/teachers/')
api.add_resource(Teacher, '/teachers/<string:username>')
api.add_resource(Terms, '/terms/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
    