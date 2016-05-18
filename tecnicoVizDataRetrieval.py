import fenixedu
import json
import os
import urllib.request

# Type fenixEduDataRetrieval() to start the data retrieval

def fenixEduDataRetrieval():
    # Create the configuration object with client_id and client_secret
    config = fenixedu.FenixEduConfiguration.fromConfigFile('fenixedu.ini')
    
    # Connect to the fenixedu api
    client = fenixedu.FenixEduClient(config)
    
    # Create \json directory if doesn't exist
    path = os.getcwd() + "\\json"
    if not os.path.exists(path):
        os.makedirs(path)
   
    # Create \degrees directory if doesn't exist
    if not os.path.exists(path + "\\degrees"):
        os.makedirs(path + "\\degrees")    

    # Get all the degrees and write to json file
    getDegrees(client)
    
    # Get all the academic terms and write to json file
    getAcademicTerms(client)
    
    # Get all the courses and write to json file
    getDegreeCourses(client)
        
def getDegrees(client):
    path = os.getcwd() + "\\json\\degrees.json"
    if not os.path.isfile(path):
        degrees = client.get_degrees()
        degreesJson = open(path, "w")
        json.dump(degrees, degreesJson, sort_keys = True, ensure_ascii = False, indent = 4)
        
def getAcademicTerms(client):
    path = os.getcwd() + "\\json\\academicTerms.json"
    if not os.path.isfile(path):
        terms = client.get_academic_terms()
        termsJson = open(path, "w")
        json.dump(terms, termsJson, sort_keys = True, ensure_ascii = False, indent = 4)
            
def getDegreeCourses(client):
    path = os.getcwd() + "\\json\\degrees" 
    
    # Load degrees json file
    degreesFile = open(path + ".json", "r")
    degreesList = json.load(degreesFile)
    
    # Load academic terms json file
    termsFile = open(os.getcwd() + "\\json\\academicTerms.json", "r")
    termsList = json.load(termsFile)
    
    isInLog = False
    
    for key in termsList:
        infoJSON = termsList[key]
        file = open(os.getcwd() + '\\' "logFile.txt","a")
        readFile = open(os.getcwd() + '\\' "logFile.txt","r")
        for i in range(0, len(degreesList)):
            
            # Create directory for each degree if they don't exist
            degreeName = degreesList[i]["name"]
            degreeType = degreesList[i]["type"]
            degreeTypeParsed = degreeType.split(' Bolonha',1)[0]
            degreePath = path + "\\" + degreeTypeParsed + ' em ' + degreeName
            if not os.path.exists(degreePath):
                os.makedirs(degreePath)
            
            # Extract all degrees from the web API
            url = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/degrees/" + degreesList[i]["id"] + "/courses?academicTerm=" + key
            pageRetrieved = urllib.request.urlopen(url).read()
            courses = json.loads(pageRetrieved.decode('utf-8'))            
            
            # Ignore years without data
            if len(courses) != 0:
                newKey = key.replace("/", " ")
                coursesJson = open(degreePath + "\\" + degreeName.lower() + " " + newKey + ".json", "w", encoding="utf-8")
                json.dump(courses, coursesJson, sort_keys = True, ensure_ascii = False, indent = 4)                
                # Extract courses from all the degrees
                for j in range(0, len(courses)):
                    courseId = courses[j]["id"]
                    # Acronym instead of name because some courses have big length
                    courseName = courses[j]["acronym"] 
                    # Check log file to see if the course was already loaded
                    for line in readFile:
                        if courseName == line:
                            isInLog = True
                        else:
                            isInLog = False
                    if isInLog == False:   
                        # Load individual courses' info
                        individualCourse = client.get_course(courseId)
                        # Load course evaluations (exams and tests dates)
                        courseEvaluation = client.get_course_evaluations(courseId)
                        # Load course groups (number of elements, capacity)
                        courseGroups = client.get_course_groups(courseId)
                        # Load course schedule (class hour, location, time spent)
                        courseSchedule = client.get_course_schedule(courseId)
                        # Load students in a specific course
                        courseStudents = client.get_course_students(courseId)
                        coursePath = degreePath + "\\" + courseName
                        # Con, Com2, Com4, Com5 and Com6 are reserved names, so instead of acronym they will have the full name
                        if courseName == "Con" or courseName == "Com2" or courseName == "Com3" or courseName == "Com4" or courseName == "Com5" or courseName == "Com6" or courseName == "Com7":
                            coursePath = degreePath + "\\" + courses[j]["name"]
                        if not os.path.exists(coursePath):
                            os.makedirs(coursePath)
                        evaluationPath = coursePath + "\\" + "evaluations"
                        groupsPath = coursePath + "\\" + "groups"
                        schedulePath = coursePath + "\\" + "schedule"
                        studentsPath = coursePath + "\\" + "students"
                        # Create the necessary folders
                        if not os.path.exists(evaluationPath):
                            os.makedirs(evaluationPath)
                        if not os.path.exists(groupsPath):
                            os.makedirs(groupsPath)                            
                        if not os.path.exists(schedulePath):
                            os.makedirs(schedulePath)
                        if not os.path.exists(studentsPath):
                            os.makedirs(studentsPath)
                        # Save individual course information in json file
                        individualCourseJson = open(coursePath + "\\" + courseName.lower() + " " + newKey + ".json", "w", encoding="utf-8")
                        json.dump(individualCourse, individualCourseJson, sort_keys = True, ensure_ascii = False, indent = 4)
                        # Save evaluation information in json file
                        evaluationJson = open(evaluationPath + "\\" + "evaluation" + " " + newKey + ".json", "w", encoding="utf-8")
                        json.dump(courseEvaluation, evaluationJson, sort_keys = True, ensure_ascii = False, indent = 4)                        
                        # Save groups information in json file
                        groupsJson = open(groupsPath + "\\" + "groups" + " " + newKey + ".json", "w", encoding="utf-8")
                        json.dump(courseGroups, groupsJson, sort_keys = True, ensure_ascii = False, indent = 4)                        
                        # Save schedule information in json file
                        scheduleJson = open(schedulePath + "\\" + "schedule" + " " + newKey + ".json", "w", encoding="utf-8")
                        json.dump(courseSchedule, scheduleJson, sort_keys = True, ensure_ascii = False, indent = 4) 
                        # Save students information in json file
                        studentsJson = open(studentsPath + "\\" + "students" + " " + newKey + ".json", "w", encoding="utf-8")
                        json.dump(courseStudents, studentsJson, sort_keys = True, ensure_ascii = False, indent = 4)                        
                        # Register in log file
                        log = courseName + "\n"
                        file.write(log)
        file.close()
        readFile.close()
                    
