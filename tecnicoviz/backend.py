import json
import re
import MySQLdb
import MySQLdb.cursors as cursors
from warnings import filterwarnings

def connectDB():
    connection = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='', autocommit=True)
    cursor = connection.cursor()  
    connection.select_db('tecnicoviz1')  
    return connection, cursor

def getDegrees(condition={}):
    result = queryDB('degrees', condition=condition)
    return result      

def getCourses(condition={}):
    result = queryDB('courses', condition=condition)
    return result

def getStudents(condition={}):
    result = queryDB('students', condition=condition)
    return result

def getTeachers(condition={}):
    result = queryDB('teachers', condition=condition)
    return result

def getTerms(condition={}):
    result = queryDB('terms', condition=condition)
    return result

def queryDB(table, condition={}):
    connection, cursor = connectDB()
    select = '*'
    where = ''    
    if condition != {}:
        where = 'WHERE '
        for key, value in condition.items():
            orStatement = ''
            closeClause = ''
            operator = ' = '
            stringBegin = "'"
            stringEnd = "'"
            if '~' in value:
                operator = ' like '
                stringBegin = "'%"
                stringEnd = "%'"
            orStatementBegin = False
            statement = str(value).replace(" ", "").replace("~ct~", "").split(',')
            for i in range(0,len(statement)):
                if len(statement) > i+1:
                    if not orStatementBegin:
                        orStatement += ' ('
                        orStatementBegin = True
                    orStatement += key + operator + stringBegin + str(statement[i]) + stringEnd + ' OR '
                else:
                    if orStatementBegin:
                        closeClause += ')'
                    where = where + orStatement + key + operator + stringBegin + str(statement[i]) + stringEnd + closeClause + ' AND '
    where = where.rsplit(' AND ', 1)[0]
    query = 'SELECT ' + select + ' FROM ' + table + ' ' + where
    print(query)
    cursor.execute(query)
    result = cursor.fetchmany(size=500000)
    while result:
        temp_res = cursor.fetchmany(size=500000)
        if temp_res == ():
            break
        else:
            result = result + temp_res 
    return result  

def getColumnNames(table):
    connection, cursor = connectDB()
    query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'tecnicoviz1' AND TABLE_NAME = %s"
    cursor.execute(query, [table])
    result = cursor.fetchall()
    return result
    