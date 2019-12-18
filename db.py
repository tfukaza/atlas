import psycopg2
import json

f = None
usr = ""
passwd = ""
host = ""
port = ""
database = ""

connection = None
cursor = None

def open_connection(path="config"):

    global f 
    global usr 
    global passwd 
    global host 
    global port 
    global database 

    global connection 
    global cursor 


    print("Opening config file")
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

    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("Connected to: ", record, "\n")

#This function is to be used only when initializing the database for the first time
def init_db():

    cursor.execute("""
    CREATE TABLE "courses"
    (
        "dept"          char(50),
        "course_num"    char(50),
        "course_title"  char(50),
        "course_unit"   char(50),
        "course_type"   char(50),
        "course_req"    json
    );

    CREATE TABLE "lectures"
    (
        "dept"          char(50),
        "course_num"    char(50),
        "course_id"     char(50),
        "term"          char(50),     
        "lec_name"      char(50),
        "lec_status"    char(50),
        "lec_capacity"  json,
        "lec_w_status"  char(50),
        "lec_w_capacity"json,
        "lec_day"       char(50),
        "lec_time_s"    char(50),
        "lec_time_e"    char(50),
        "lec_location"  char(50),
        "lec_inst"      char(50)

    );

    CREATE TABLE "discussions"
    (
        "course_id"     char(50),
        "term"          char(50),     
        "dis_name"      char(50),
        "dis_status"    char(50),
        "dis_capacity"  json,
        "dis_w_status"  char(50),
        "dis_w_capacity"json,
        "dis_day"       char(50),
        "dis_time_s"    char(50),
        "dis_time_e"    char(50),
        "dis_location"  char(50),
        "dis_inst"      char(50)
    );
    
    """)
    connection.commit()

def execute_db(q):

    cursor.execute(q)
    result = cursor.fetchall()
    connection.commit()

    return result

def close_connection():
 
    if(connection):
        cursor.close()
        connection.close()
    else:
        print("")


#given a class info formatted as a list (in JSON style), adds it to the db
def addCourse(course):

    command = """INSERT INTO courses"""
    command+="VALUES ("
    command+=course["dept"] + ", "
    command+=course["course_title"] + ", "
    command+=course["course_unit"] + ", "
    command+=course["course_type"] + ", "
    command+=json.dumps(course["course_req"]) + ");"

    execute_db(command)