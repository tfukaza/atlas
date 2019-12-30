##############################
# This module is the interface for other python modules to interact with a
# PostgreSQL database.  
# It contains functions to maintain the database, as well as 
# functions to retrieve data from the database in useful manners
##############################

import psycopg2
import json

#Constants used to run the database
f = None
usr = ""
passwd = ""
host = ""
port = ""
database = ""

connection = None
cursor = None
# =======================
# Initializes the tables in the database
# Make sure there are no tables in the database when running this, otherwise the 
# function will return an error
# =======================

def init_db():

    print("initializing")
    cursor.execute("""

    CREATE TABLE "departments"
    (
        "mode"          char(10),
        "dept_id"       char(10),
        "dept_name"     char(100)
    );

    CREATE TABLE "courses"
    (
        "dept"          char(10),
        "course_order"  int,
        "course_num"    char(8),
        "course_title"  char(200),
        "course_unit"   char(10),
        "course_type"   char(15),
        "course_req"    json,
        "course_grade"  char(5),
        "course_desc"   char(1500)
    );

    CREATE TABLE "lectures"
    (
        "dept"          char(10),
        "course_num"    char(16),
        "course_id"     char(9),
        "term"          char(4),     
        "lec_name"      char(16),
        "lec_status"    char(32),
        "lec_capacity"  json,
        "lec_w_status"  char(32),
        "lec_w_capacity"json,
        "lec_day"       char(16),
        "lec_time_s"    char(16),
        "lec_time_e"    char(16),
        "lec_location"  char(64),
        "lec_inst"      char(64)

    );

    CREATE TABLE "discussions"
    (
        "lec_id"        char(9),
        "course_id"     char(9),
        "term"          char(4),     
        "dis_name"      char(16),
        "dis_status"    char(32),
        "dis_capacity"  json,
        "dis_w_status"  char(32),
        "dis_w_capacity"json,
        "dis_day"       char(8),
        "dis_time_s"    char(16),
        "dis_time_e"    char(16),
        "dis_location"  char(64),
        "dis_inst"      char(64)
    );
    
    """)
    connection.commit()


# =======================
# Provided a path to the config file, opens a connection to the database using the 
# provided configurations
# Config files should be a text file containing the:
#   database username
#   password
#   IP address
#   port number
#   database name
# in each line 
# =======================
def open_connection(path="config"):

    global f 
    global usr 
    global passwd 
    global host 
    global port 
    global database 

    global connection 
    global cursor 

    #print("Opening config file")
    f = open(path,"r")

    usr = f.readline()
    passwd = f.readline()
    host = f.readline()
    port = f.readline()
    database = f.readline()

    #make sure to remove the newlines
    usr = usr[:-1]
    passwd = passwd[:-1]
    host = host[:-1]
    port = port[:-1]

    print("Establishing connection with database")
    connection = psycopg2.connect(  user = usr,
                                    password = passwd,
                                    host = host,
                                    port = port,
                                    database = database)
    cursor = connection.cursor()

    #cursor.execute("SELECT version();")
    #record = cursor.fetchone()
    #print("Connected to: ", record, "\n")

# =======================
# Closes connection with the database 
# =======================

def close_connection():
 
    if(connection):
        cursor.close()
        connection.close()
    else:
        print("No open connections")


# =======================
# Queries the databse, provided a command as a string
# =======================

def get_db(q):

    cursor.execute(q)
    result = cursor.fetchall()
    connection.commit()

    return result

# =======================
# Deletes tables in the database
# =======================

def delete_db():
    cursor.execute("""
    DROP TABLE departments;
    DROP TABLE courses;
    DROP TABLE lectures;
    DROP TABLE discussions;
    """)
    connection.commit()

# =======================
# Adds a department to the table
# Ignored if department already exists
# =======================

def addDept(mode, dept_id, dept_name):

    result = get_db("SELECT * FROM departments WHERE dept_name='" + dept_name + "';")

    if len(result) == 0:
        command = "INSERT INTO departments "
        command+="VALUES ("
        command+="'" + mode + "', "
        command+="'" + dept_id + "', "
        command+="'" + dept_name + "'); "
        cursor.execute(command)
        connection.commit()

# =======================
# Given information regarding a course, updates its information in the table
# If the course does not exist yet, it will be newly created
# =======================
def updateCourse(course):

    #check if course exists in db
    chk = "SELECT course_order FROM courses WHERE dept='" + course["dept"] + "' AND course_num='" + course["course_num"] + "';"
    cursor.execute(chk)
    result = cursor.fetchall()

    command = ""

    #if course does not exist yet, add it
    if len(result) == 0:
        command = "INSERT INTO courses "
        command+="VALUES ("
        command+="'" + course["dept"] + "', "
        command+=" " + str(course["course_order"]) + ", "
        command+="'" +course["course_num"] + "', "
        command+="'" +course["course_title"] + "', "
        command+="'" +course["course_unit"] + "', "
        command+="'" +course["course_type"] + "', "
        command+="'" +json.dumps(course["course_req"]) + "', "
        command+="'" +course["course_grade"] + "', "
        command+="'" +course["course_desc"] + "');"

    # if course exist, update it
    else:
        command = "UPDATE courses "
        command+= "SET "
        command+= "course_order = " + str(result[0][0]) + ", "
        command+= "course_num = '" + course["course_num"] + "', "
        command+= "course_title = '" + course["course_title"] + "', "
        command+= "course_unit = '" + course["course_unit"] + "', "
        command+= "course_type='" + course["course_type"] + "', "
        command+= "course_req='" + json.dumps(course["course_req"]) + "', "
        command+= "course_grade='" + course["course_grade"] + "', "
        command+= "course_desc='" + course["course_desc"] + "'" 
        command+= "WHERE dept='" + course["dept"] + "' AND course_num='" + course["course_num"] + "';"

    cursor.execute(command)
    connection.commit()

# =======================
# Given an id and term for a lecture, adds it to the table if it does not exist yet
# =======================

def addLecId(dept, num, id, term):

    result = get_db("SELECT * FROM lectures WHERE course_id='" + id + "' AND term = '" + term + "';")

    if len(result) == 0:
        command = "INSERT INTO lectures (dept, course_num, course_id, term)"
        command+="VALUES ("
        command+="'" + dept + "', "
        command+="'" + num + "', "
        command+="'" + id + "', "
        command+="'" + term + "'); "
        cursor.execute(command)
        connection.commit()

# =======================
# Given an id and term for a lecture, adds it to the table if it does not exist yet
# =======================

def addDisId(lec_id, id, term):

    result = get_db("SELECT * FROM discussions WHERE course_id='" + id + "' AND term = '" + term + "';")

    if len(result) == 0:
        command = "INSERT INTO discussions (lec_id, course_id, term)"
        command+="VALUES ("
        command+="'" + lec_id + "', "
        command+="'" + id + "', "
        command+="'" + term + "'); "
        cursor.execute(command)
        connection.commit()

# =======================
# Given an id and term for a lecture, adds it and its information to the table
# This function assumes the lecture record already exists
# =======================

def updateLec(id, term, lec):

    command = "UPDATE lectures "
    command+= "SET "
    command+= "lec_name = '" + lec["sect"] + "', "
    command+= "lec_status = '" + lec["enrollment"]["status"] + "', "
    command+= "lec_capacity = '" + json.dumps(lec["enrollment"]) + "', "
    command+= "lec_w_status ='" + lec["enrollment"]["waitlist"]["status"] + "', "
    command+= "lec_w_capacity ='" + json.dumps(lec["enrollment"]["waitlist"]) + "', "
    command+= "lec_day='" + lec["days"] + "', "
    command+= "lec_time_s='" + lec["time"]["start"] + "',"
    command+= "lec_time_e='" + lec["time"]["end"] + "'," 
    command+= "lec_location='" + lec["location"] + "'," 
    command+= "lec_inst='" + lec["instructor"] + "'"  
    command+= "WHERE course_id='" + id + "' AND term='" +term + "';"

    cursor.execute(command)
    connection.commit()

# =======================
# Given an id and term for a discussion, adds it to the table if it does not exist yet
# =======================

def updateDis(id, term, lec):

    command = "UPDATE discussions "
    command+= "SET "
    command+= "dis_name = '" + lec["sect"] + "', "
    command+= "dis_status = '" + lec["enrollment"]["status"] + "', "
    command+= "dis_capacity = '" + json.dumps(lec["enrollment"]) + "', "
    command+= "dis_w_status ='" + lec["enrollment"]["waitlist"]["status"] + "', "
    command+= "dis_w_capacity ='" + json.dumps(lec["enrollment"]["waitlist"]) + "', "
    command+= "dis_day='" + lec["days"] + "', "
    command+= "dis_time_s='" + lec["time"]["start"] + "',"
    command+= "dis_time_e='" + lec["time"]["end"] + "'," 
    command+= "dis_location='" + lec["location"] + "'," 
    command+= "dis_inst='" + lec["instructor"] + "'"  
    command+= "WHERE course_id='" + id + "' AND term='" +term + "';"

    cursor.execute(command)
    connection.commit()

##########################
# Below are functions to retrieve data from the database in meaningful ways
##########################


# =======================
# Given two course names, returns all courses that exists between them
# example:
#   (MATH 31A, MATH 32B) => [MATH 31A, MATH 31B, MATH 32A, MATH 32B]  
# =======================

def getCourseRange(start, end):

    #seperate courses 
    tmp_s = start.split()
    start_dept = tmp_s[0]
    start_num = tmp_s[1]

    tmp_e = end.split()
    end_dept = tmp_e[0]
    end_num = tmp_e[1]

    #check the index number of start course
    chk = "SELECT course_order FROM courses WHERE dept='" + start_dept + "' AND course_num='" + start_num + "';"
    cursor.execute(chk)
    result = cursor.fetchall()
    #print(result)
    start_num = result[0][0]

    #check the index number of end course
    chk = "SELECT course_order FROM courses WHERE dept='" + end_dept + "' AND course_num='" + end_num + "';"
    cursor.execute(chk)
    result = cursor.fetchall()
    #print(result)
    if len(result) == 0:
        print("error")
        return []
    end_num = result[0][0]
    #print(end_num)

    #get course in that range
    chk = "SELECT dept, course_num FROM courses WHERE dept='" + start_dept + "' AND course_order BETWEEN " + str(start_num) + " AND " + str(end_num) + ";"
    cursor.execute(chk)
    result = cursor.fetchall()

    response = []

    for r in result:
        response.append((trim(r[0]) + " " + trim(r[1])))

    return response


# =======================
# Given two course names, returns all courses that exists between them
# example:
#   (MATH 31A, MATH 32B) => [MATH 31A, MATH 31B, MATH 32A, MATH 32B]  
# =======================

def getCourseLevel(dept, level):


    #check the index number of start course
    chk = "SELECT dept, course_num FROM courses WHERE dept='" + dept + "';"
    cursor.execute(chk)
    result = cursor.fetchall()
    #print(result)

    num_min = 0
    num_max = 0

    if level =="upperdiv":
        num_min = 100
        num_max = 199

    response = []
    
    for res in result:
        number = int(trim_nondigit(res[1]))
        if number >= num_min and number <= num_max:
            response.append(trim(res[0]) + " " + trim(res[1]))

    return response

#helper function to trim off nondigits and whitespaces
def trim_nondigit(s):
    while not s[-1].isdigit():
        s = s[0:-1]
    while not s[0].isdigit():
        s = s[1:]

    return s



#helper function to trim off whitespaces
def trim(s):
    while s[-1] == " ":
        s = s[0:-1]
    return s



