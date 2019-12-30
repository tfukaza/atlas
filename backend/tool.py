##############################
# This excutable wraps other modules to provide a CLI tool
# to perform varios operations 
##############################

import db
import scrape
import re

# =========================
# The function takes a range of terms and a course,
# and returns a list of offered lecture (course) id's for each term, if any
# ========================= 
"""
def getIds(terms=["20W"], course):

    #seperate courses 
    tmp_s = course.split()
    dept = tmp_s[0]
    num = tmp_s[1]

    db.open_connection("../../db.config")

    c = db.get_db("SELECT dept, course_num, course_title, course_unit FROM courses WHERE dept='" + dept + "' AND course_num = '" + num + "');")
    c = c[0]

    result = {}

    for t in terms:
        r = scrape.scrapeLectureId(t, c[0], c[1], c[2], c[3])
        r[t] = r 
    
    print(result)
    return result
"""
# =========================
# The function takes a range of terms and a list of courses,
# and returns a list of offered lecture (course) id's for each term, 
# along with basic descriptions for each of them. 
# ========================= 

def get_mini_db(terms, courses):

    result = {}

    db.open_connection("../../config")

    for course in courses:

        #seperate courses 
        tmp_s = course.split()
        dept = tmp_s[0]
        num = tmp_s[1]

        c = db.get_db("SELECT dept, course_num, course_title, course_unit, course_desc FROM courses WHERE dept='" + dept + "' AND course_num = '" + num + "';")
        c = c[0]

        info={}

        #info["dept"] = trim(c[0])
        #info["num"] = trim(c[1])
        info["title"] = trim(c[2])
        info["unit"] = trim(c[3])
        info["desc"] = trim(c[4])

        lec = []

        for t in terms:
            c = db.get_db("SELECT course_id FROM lectures WHERE dept='" + dept + "' AND course_num = '" + num + "' AND term = '" + t + "';")
            lec.append({t:c})

        res={}

        res["info"] = info
        res["lec"] = lec

        result[course] = res

    db.close_connection()

    return result

# Helper function that "simplifies" a list
# This function will process special keywords like %through
# and make the list less readable but more computer friendly

def simplifyReq(req):

    print("connecting to database")
    db.open_connection("../../config")

    response = []

    if isinstance(req, str):
        return req

    for i in range(0, len(req)):

        if isinstance(req[i], str):
            #we can skip keywords, as they are not classes
            if req[i] == "%and" or req[i][0:3] == "%or":
                response.append(req[i])
                continue
            elif req[i][0:8] == "%through":
                start = req[i - 1]
                end = req[i + 1]

                response.pop(-1)

                #list of courses to exclude
                ex = req[i].split("?")
                ex = ex[1:]
                #print(ex)

                #get the list of courses specified in the expression "course through course"
                thru = db.getCourseRange(start, end)

                for t in thru[0:-1]:
                    isEx = False
                    for e in ex:
                        if e == t:
                            isEx = True
                    
                    if not isEx:
                        response.append(t)
            elif req[i][0:3] == "%up":
                #list of courses to exclude
                ex = req[i].split("?")
                dept = ex[1]
                ex = ex[2:]

                #get the list of courses specified in the expression "course through course"
                thru = db.getCourseLevel(dept, "upperdiv")

                for t in thru[0:-1]:
                    isEx = False
                    for e in ex:
                        if e == t:
                            isEx = True
                    
                    if not isEx:
                        response.append(t)

            else:
                response.append(req[i])
        else:
            response.append(simplifyReq(req[i]))
    
    return response

    db.close_connection()

# Helper function that "flattens" a req list
# Returns a list of every course in the req list
def flattenReq(req):  

    response = []

    for r in req:

        if isinstance(r, str):
            #we can skip keywords, as they are not classes
            if r == "%and" or r[0:3] == "%or":
                continue
            else:
                response.append(r)
        else:
            response = response + flattenReq(r)

    return response

#function that takes a list in a string format, and returns it as a list

def string2list(string):

    string = re.split("[',]+", string)


    result = []
    print(string)
    for t in string:

        if t == "[":
            result.append([])
        
        elif t == "]":
            tmp = result[-1]
            result.pop(-1)

            if len(result) == 0:
                result = [tmp]
            else:
                result[-1] = tmp 
        
        else:
            result[-1].append(t)

    return result[0]

#helper function to trim off whitespaces
def trim(s):
    while s[-1] == " ":
        s = s[0:-1]
    return s


if __name__ =="__main__":
    print(get_mini_db(["20W", "20S"], "COM+SCI 32"))
    
    

