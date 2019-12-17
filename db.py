import psycopg2

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
        "course_id"     char(50),
        "course_dept"   char(50),
        "course_title"  char(50),
        "course_req"    json
    );

    CREATE TABLE "slots"
    (
        "course_id"     char(50),
        "term"          char(50),     
        "lecture"       char(50),
        "capacity"      char(50)
    );
    
    """)

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
