##############################
# This module contains the scraper that collects various information 
# from corresponding websites. 
##############################

import urllib.request
import urllib.parse
import re
import psycopg2
from pyquery import PyQuery as pq 
import json
import aiohttp
import asyncio
from concurrent.futures import FIRST_COMPLETED

import parser 
import db

dept_dict = []
dept = []

#helper function to trim off whitespaces
def trim(s):
    while s[-1] == " ":
        s = s[0:-1]
    return s

# =======================
# This function invokes all neccesary functions needed to update lecture information
# in the database to its latest state
# =======================

def updateLecture():

    db.open_connection("../../config")

    #get all lectures listed
    lectures = db.get_db("SELECT course_id, term FROM lectures")

    for lec in lectures:

        #get the latest info for the lecture and its discussions
        discussions = scrapeLectureInfo(trim(lec[1]), trim(lec[0]))
        print(discussions[0])
        #update lecture info
        db.updateLec(trim(lec[0]), trim(lec[1]), discussions[0])

        
        #update discussions
        for dis in discussions[1:]:
            print(dis)
            db.updateDis(dis["course_id"], trim(lec[1]), dis)
        
    db.close_connection()

# helper function to generate URL to get course info based on term and ID
def getLectureInfoURL(term, id):

    url="https://sa.ucla.edu/ro/Public/SOC/Results?t="
    url+=term
    url+="&sBy=classidnumber&id="
    url+=id
    url+="&btnIsInIndex=btn_inIndex"

    return url

# This function will take a class id and term, and return their latest info
def scrapeLectureInfo(term, id):

    url=getLectureInfoURL(term, id)
    #request the webpage
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)

    #store the result in a string
    html = response.read().decode()

    #print(html)
    #pass it into PyQuery for parsing
    query = pq(html, parser='html')

    #get the columns
    #name
    name = query(".sectionColumn .cls-section p a")
    
    #name=name[1:]
    
    #print(pq(name[0]).text())
    #print(pq(name[0]).attr("title"))
    #status
    stat = query(".statusColumn p")
    stat=stat[1:]
    #print(pq(stat[0]).text())

    #waitlist
    waitlist = query(".waitlistColumn p")
    waitlist=waitlist[1:]
    #print(pq(waitlist[0]).text())

    #day
    day = query(".dayColumn p")
    day=day[1:]
    #print(pq(day[0]).text())

    #time
    time = query(".timeColumn")
    time=time[1:]
    #print(pq(time[0]).text())

    #location
    loc = query(".locationColumn")
    loc=loc[1:]
    #print(pq(time[0]).text())

    #instructor
    inst = query(".instructorColumn")
    inst=inst[1:]
    #print(pq(inst[0]).text())

    lec=[]

    #process scraped info
    for i in range(0, len(name)):
        lec.append(formatStat(  pq(name[i]).text(), 
                                pq(name[i]).attr("title"),
                                pq(stat[i]).text(), 
                                pq(waitlist[i]).text(), 
                                pq(day[i]).text(), 
                                pq(time[i]).text(), 
                                pq(loc[i]).text(),
                                pq(inst[i]).text()
                            ))
    
    return lec

# A helper function to properly format lecture/discussion info

def formatStat(name, id, stat, waitlist, day, time, loc, inst):

    info={}

    #=====name=====
    info["sect"] = name

    #=====id=======
    id_begin=id.find("for") + 4
    info["course_id"] = id[id_begin:]
    
    s={}
  
    #=====stat======
    #if this class has been closed by department
    if stat.find("Closed by") != -1:
        s["status"] = "Closed by Dept"
        s["taken"] = "n/a"
        s["cap"] = "n/a"
    #if the class is active
    else:
        new = stat.find('\n')
        tmp_stat = stat[0:new]
        s["status"] = tmp_stat
        
        #if there are still slots
        if tmp_stat == "Open":
            #get next line
            line = stat[new:]
            #parse
            of = line.find("of")
            end = line.find("Enrolled")
            s["taken"] = line[1:of]
            s["cap"] = line[of+3:end-1]

        else:
            #get next line
            line = stat[new:]
            #parse
            par = line.find("(")
            end = line.find(')')
            s["taken"] = line[par+1:end]
            s["cap"] = line[par+1:end]


    #=====waitlist=====
    w={}
    #if there is no waitlist
    if waitlist.find("No") != -1:
        w["status"] = "None"
        w["taken"] = "n/a"
        w["cap"] = "n/a"
    #if the waitlist is full
    elif waitlist.find("Full") != -1:
        w["status"] = "Full"
        par = waitlist.find("(")
        end = waitlist.find(")")
        w["taken"] = waitlist[par+1:end] 
        w["cap"] = waitlist[par+1:end] 
    #id waitlist is open
    else:
        w["status"] = "Open"
        of = waitlist.find("of")
        end = waitlist.find("Taken")
        w["taken"] = waitlist[0:of-1] 
        w["cap"] = waitlist[of+2:end-1]
    
    s["waitlist"] = w

    info["enrollment"] = s

    info["days"] = day

    #=====time======
    t = {}

    #if time is listed as "varies"
    if time.find("aries") != -1:
        t["start"] = "Varies"
        t["end"] = "Varies"
    #if day was "Not scheduled"
    elif day.find("Not scheduled") != -1:
        t["start"] = "n/a"
        t["end"] = "n/a"
    #otherwise, process time as usual
    else:
        t_line_i = time.find("\n")
        time = time[t_line_i+1:]

        t_line_i = time.find("-")
        t_start = time[0:t_line_i-1]
        t_end = time[t_line_i+1:]

        t["start"] = t_start
        t["end"] = t_end

    info["time"] = t

    #=====location======
    if len(loc) == 0:
        loc = "n/a"
    info["location"] = loc

    #=====instructor======
    info["instructor"] = inst


    return info

# =======================
# This function will access the databse for all the courses, 
# and for each of them, adds the currently offered lectures and its id to the database
# =======================

def scrapeLectureList(term = "20W"):

    asyncio.run(scrapeLectureList_1(term))
    #await scrapeLectureList_1(term)

async def scrapeLectureList_1(term = "20W"):

    #loop=asyncio.get_event_loop()

    db.open_connection("../../config")


    #get a list of every courses
    #for each, get the department, course number, course title, and course units
    courses = db.get_db("SELECT dept, course_num, course_title, course_unit FROM courses")

    #for each course, use the obtained info to get the available lectures and its course_id
    
    pending = set()
    
    for c in courses[0:]:

        # halt loop if thread pool is full
        while len(pending) > 200:
            # check if the tasks are finshed
            done, pending = await asyncio.wait(pending, return_when = FIRST_COMPLETED)

            for d in done:
                ids = d.result()
                for i in ids["ids"]:
                    db.addLecId(ids["dept"], ids["num"], i, term)
        
                    # Initialize info for the lecture, as well as discussions (if applicable)
                    # get the list of lecture + discussions
                    #d_list = scrapeLectureInfo(term, i)
                    #print(d_list)
                    #we can skip the first element, as it is the lecture itself
                    # iterate through the discussions, and add it tdatabase
                    #for d in d_list[1:]:
                    #    db.addDisId(i, d["course_id"], term)
                #remove the task

            """
            i = 0
            while i < len(pool):
                    #print(pool[i].get_stack())
                    #if a task is done
                    if pool[i].done():
                        #get the result and record it
                        ids = pool[i].result()
                        for i in ids:
                            db.addLecId(trim(c[0]), trim(c[1]), i, term)

                            # Initialize info for the lecture, as well as discussions (if applicable)
                            # get the list of lecture + discussions
                            #d_list = scrapeLectureInfo(term, i)
                            #print(d_list)
                            #we can skip the first element, as it is the lecture itself
                            # iterate through the discussions, and add it tdatabase
                            #for d in d_list[1:]:
                            #    db.addDisId(i, d["course_id"], term)
                        #remove the task
                        pool.pop(i)
                    else:
                        i = i + 1
            """
        dept = trim(c[0])
        dept_id = trim(c[0]).replace("&", "%26")
        number = trim(c[1])
        title=trim(c[2]).replace(" ", "+")
        unit=trim(c[3])

        #if number != "33":
        #    continue

        #scrape for corresponding lectures
        
        #TODO make session concurrent, not requests
        #should be easy, just swap the task with resp.text()
        pending.add(asyncio.create_task(scrapeLectureId(term, dept, dept_id, number, title, unit)))
        #asyncio.run(pool[-1])

        
        #ids = scrapeLectureId(term, dept_id, number, title, unit)
        
        #print(ids)

        #add each id to database
        #for i in ids:
            #db.addLecId(trim(c[0]), trim(c[1]), i, term)

            # Initialize info for the lecture, as well as discussions (if applicable)
            # get the list of lecture + discussions
            #d_list = scrapeLectureInfo(term, i)
            #print(d_list)
            #we can skip the first element, as it is the lecture itself
            # iterate through the discussions, and add it tdatabase
            #for d in d_list[1:]:
                #db.addDisId(i, d["course_id"], term)


    #finish up any reamaining connections
    while len(pending) > 0:
        # check if the tasks are finshed
        done, pending = await asyncio.wait(pending, return_when = FIRST_COMPLETED)

        for d in done:
            ids = d.result()
            for i in ids["ids"]:
                db.addLecId(ids["dept"], ids["num"], i, term)

    print("Finished connection")


    db.close_connection()

# Given a course and its info, this function will return a list of course id's 
# for all lectures offered for the specified term
# This function is async to improve performance

async def scrapeLectureId(term, dept, dept_id, class_id, class_name, units):

    
    #print("created")

    #https://sa.ucla.edu/ro/Public/SOC/Results?t=
    # 20W
    # &sBy=units
    # &meet_units=4.0
    ## &sName=Computer+Science+%28COM+SCI%29
    # &subj=COM+SCI
    # &crsCatlg=M51A+-+Logic+Design+of+Digital+Systems
    # &catlg=0051A+M
    ## &cls_no=%25&btnIsInIndex=btn_inIndex"
    url="https://sa.ucla.edu/ro/Public/SOC/Results?t="
    url+=term
    url+="&sBy=units"
    
    url+="&meet_units="
    url+=units

    #url+="&sName="
    #url+=dept_name
    #url+="+%28"
    #url+="%29&"
    
    url+="&subj="
    url+=dept_id

    url+="&crsCatlg="
    url+=class_id
    url+="+-+"
    url+=class_name
    
    #process the catalog number
    url+="&catlg="

    #if the catalog number starts with a sequence of letters it must be moved to the end of the number, seperated by a space
    #The format is [4 digits][+ or alpha][+][front alpha (if any)]
    front_id_alpha = ""
    rear_id_alpha = ""

    if len(class_id) > 1:
        while class_id[0].isalpha():
            front_id_alpha+=class_id[0]
            class_id = class_id[1:]

        while class_id[-1].isalpha():
            rear_id_alpha=class_id[-1] + rear_id_alpha
            class_id = class_id[0:-1]

        #At this point class_id should only contain digits

        #pad 0's so there are 4 digits
        tmp_l = 4 - len(class_id)
        if tmp_l > 0:
            class_id = ("0" * tmp_l) + class_id

        #add the rear alpha back
        class_id+=rear_id_alpha

        #if there was a front alpha, pad "+" accordingly and add it to the rear
        if len(front_id_alpha) > 0:
            tmp_a = 2 - len(rear_id_alpha)
            class_id+=("+" * tmp_a)
            class_id+=front_id_alpha
    
        url+=class_id
    else:
        if class_id[0].isalpha():
            url+="0000" + class_id[0]
        else:
            url+="000" + class_id[0]


    #request the webpage
    #request = urllib.request.Request(url)
    #response = urllib.request.urlopen(request)

    #store the result in a string
    #html = response.read().decode()
    ids=[]

    html=""

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                html = await resp.text()
                #if resp.status != 200:
                ##    print("Error featch")
                #    return ['000000000']
                #else: 
                #    html = str(r, 'utf-8')
    
    except asyncio.TimeoutError:
        print("Timeout")
        return {"dept":dept, "num":class_id, "ids":['000000000']}
    except:
        print("Error")
        return {"dept":dept, "num":class_id, "ids":['000000000']}
    

    print(class_id)
    print(url)

    #pass it into PyQuery for parsing
    query = pq(html, parser='html')

    lec_table = query(".class-not-checked")
    
    
    for lec in lec_table:
        lec_id = pq(lec).attr('id')
        id_end = lec_id.find("_")

        lec_id = lec_id[0:id_end]
        ids.append(lec_id)

    #print("completed")
    ids = {"dept":dept, "num":class_id, "ids":ids}
        
    return ids

# =======================
# This function enumerates the database with a list of all courses offered
# =======================

# This function scrapes for the list of departments 
def scrapeDept():

    print("scraping department list...")

    #The main course description page
    url="https://www.registrar.ucla.edu/Academics/Course-Descriptions"
    #request the webpage
    request = urllib.request.Request(url)
    response  = urllib.request.urlopen(request)

    #store the result in a string
    html = response.read().decode()
    #pass it into PyQuery for parsing
    query = pq(html, parser='html')
    dept = []
    i = 0

    db.open_connection("../../config")

    dept_li = query("a[href *= '/Academics/Course-Descriptions/Course-Details?SA=']")

    #for every department that was found, record its info
    for li in dept_li:

        #get the href of the li 
        href = pq(li).attr('href')
        #get the name contained in the li
        name = pq(li).text()
        

        id_begin = href.find("?SA=")
        id_end = href.find("&")
        id = href[id_begin + 4:id_end]
        id = id.replace('%26','&')

        db.addDept("A", id, name)
        #dept.append((id, name)) #add the dept id and name tuple to list

    #manually add some translatons
    db.addDept("M", 'C&EE', 'Civil Engineering')
    db.addDept("M", 'EC+ENGR', 'Electrical Engineering')
    db.addDept("M", 'C&EE', 'Civil ENGR')
    db.addDept("M", 'EC+ENGR', 'Electrical ENGR')
    db.addDept("M", 'AERO+ENGR', 'Mechanical and Aerospace ENGR')
    db.addDept("M", 'CHEM', 'Chemistry')
    db.addDept("M", 'MAT+SCI', 'Materials Science')
    db.addDept("M", 'SEMITIC', 'SEMITICs')

    db.close_connection


#This is the main scraper that checks all courses offered and records them in the database
def scrapeCourses():
    
    scrapeDept()

    #connect to database
    print("connecting to database")
    db.open_connection("../../config")
    #db.delete_db()
    #db.init_db()
    
    dept = db.get_db("SELECT dept_id, dept_name FROM departments WHERE mode = 'A'")
    dept_mapping = db.get_db("SELECT dept_id, dept_name FROM departments")

    print("scraping")
    
    #for every department
    for d in dept:

        #if d[0] != "COM+SCI":
        #    continue

        dept_id = d[0]

        print("scraping " + d[1])

        #obtain a list of every course in that department
        dept_url="https://www.registrar.ucla.edu/Academics/Course-Descriptions/Course-Details?SA="
        #make sure to encode '&' as "%26"
        dept_url+=trim(dept_id.replace("&", "%26"))
        dept_url+=trim("&funsel=3")

        dept_request = urllib.request.Request(dept_url)
        dept_response  = urllib.request.urlopen(dept_request)
        print(dept_url)

        #store the result in a string
        html = dept_response.read().decode("utf-8")
        #pass it into PyQuery for parsing
        query = pq(html, parser='html')

        # query a list of courses
        course_div = query(".media-body")

        i = 0

        #for each course
        for div in course_div:
            i = i + 1
            #retrieve description of course
            course_info = parseDesc(pq(div), dept_id, dept_mapping, i)
            print(course_info["course_num"])

            

            #skip if there is a class with no description
            if course_info["course_title"] == "void":
                print("skipping")
                continue
            
            #add it to database, skip if it already exists
            db.updateCourse(course_info)

    #close connection with database
    db.close_connection()

# This function takes a HTML file for a course description, parses it,
# and returns an object containing the formatted info. 

def parseDesc(html, major="", dept=[], num = 0):

    #C = Course()
    s={}

    query = pq(html, parser='html')

    s["dept"] = major #.replace("+", "-")

    title = query("h3").text()  #find the course title

    id_end = title.find(".")    
    c_id = title[0:id_end]      #get course ID 
    
    s["course_order"] = num

    #scrape for the course id

    s["course_num"] = c_id
    #print(c_id)

    name = title[id_end + 2:]   #get course title 
    
    s["course_title"] = name.replace("'", "''")

    #scrape course units
    unit_p = query("p").eq(0).text()
    unit="" 
    unit_end = unit_p.find(":")

    #change formatting depending on whether if units are fixed or varibale
    if unit_p.find("to") != -1:
        unit2_end = unit_p.find("to")
        unit = unit_p[unit_end+2:unit2_end-1]
        unit+=".0"
        unit+="-"
        unit+=unit_p[unit2_end+3:]
        unit+=".0"
    elif unit_p.find("or") != -1:
        unit2_end = unit_p.find("or")
        unit = unit_p[unit_end+2:unit2_end-1]
        unit+=".0"
        unit+="/"
        unit+=unit_p[unit2_end+3:]
        unit+=".0"
    else:
        unit = unit_p[unit_end+2:]
        unit+=".0"
    
    s["course_unit"] = unit

    #scrape course description
    desc_p = query("p").eq(1).text()

    #if there is a description (some courses have no description)
    if len(desc_p) > 0:

        #handle cases where description starts with a disclaimer
        if desc_p[0] == '(':
            e = desc_p.find(')')
            desc_p = desc_p[e:]

        #handle cases where description starts with another disclaimer
        if desc_p[0] == '(':
            e = desc_p.find(')')
            desc_p = desc_p[e:]

        #get the next sentence, which should state the type of the course
        type_end = desc_p.find(".")
        type_tmp = desc_p[0:type_end]

        c_type = ""

        #get the type of course
        types = ['Laboratory','Lecture','Seminar','Tutorial']
        for t in types:
            if type_tmp.find(t) != -1:
                c_type = t

        s["course_type"] = c_type

       

        desc_p = desc_p[type_end+1:]
        
        #find the sentence that has the requisites
        req_begin = desc_p.find("equisites: ")
        if req_begin == -1:
            req_begin = desc_p.find("equisite: ")
            if req_begin != -1:
                req_begin = req_begin + 11
        else:
            req_begin = req_begin + 12

        #call parser if there is a requisite
        if req_begin != -1:
            
            #req_tmp = desc_p[req_begin + 11:]
            req_end = desc_p.find(".")
            """
            ====PREREQ PARSER DISBALED FOR NOW======
            result = parser.parseReq(req_tmp[0:req_end], major, dept)
            
            if result == []:
                print(c_id)
                print(req_tmp[0:req_end])
                print(parser.tokenizeReq(req_tmp[0:req_end], dept))
                print("Req parsing error:\t" + c_id)

            s["course_req"] = parser.formatList(result)
            desc_p = desc_p[req_end+2:]
            """
            s["course_req"] = "pending"

            

        else:
            s["course_req"] = "none"
            #s+=","
        

        #get the last sentence, which contains info about the grading scheme
        #iterate backwards from the end to find the second last period
        itr = 2
        while len(desc_p) - itr >= 0 and desc_p[len(desc_p) - itr] != '.':
            itr = itr + 1

        grading_p = desc_p[len(desc_p) - itr + 1:]
        scheme=""

        if grading_p.find("etter") != -1:
            scheme+="L" 
        if grading_p.find("P/NP") != -1:
            scheme+="P" 
        if grading_p.find("S/U") != -1:
            scheme+="S" 
        
        s["course_grade"] = scheme

        desc_tmp = desc_p[0:len(desc_p) - itr + 1]
        desc_tmp = desc_tmp.replace("'", "''")
        

        s["course_desc"] = desc_tmp

    else:
        s["course_title"] = "void"

    return s
