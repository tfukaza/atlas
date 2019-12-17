import urllib.request
import urllib.parse
import re
import psycopg2
from pyquery import PyQuery as pq 

import parser 


"""
#class for each course
class Course:
    def __init__(self, name="", id="", level="lower", units="", desc="", req=[[]], misc=0):
        self.id = id
        self.name = name
        self.dpt = ""
        self.level = level
        self.units = units
        self.c_type = ""
        self.sameas = []
        self.desc = desc
        self.req = req
        self.misc = misc
"""

def scrapeDiv(html, major="", dept=[]):
    
    #C = Course()
    s=""
    s+="{"

    query = pq(html, parser='html')

    s+=("'dept':'" + major + "',")

    title = query("h3").text()  #find the course title

    id_end = title.find(".")    
    c_id = title[0:id_end]      #get course ID 
    
    s+=("'course_id':'" + c_id + "',")
    #print(c_id)

    name = title[id_end + 2:]   #get course title 
    s+=("'course_title':'" + name + "',")

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
    
    s+=("'course_unit':'" + unit + "',")

    #scrape course description
    desc_p = query("p").eq(1).text()

    #if there is a description (some courses have no description)
    if len(desc_p) > 0:

        #handle cases where description starts with a disclaimer
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

        s+=("'course_type':'" + c_type + "',")

        s+="'course_req':"

        desc_p = desc_p[type_end+1:]

        #find the sentence that has the requisites
        req_begin = desc_p.find("equisites: ")

        #call parser if there is a requisite
        if req_begin != -1:
            req_tmp = desc_p[req_begin + 11:]
            req_end = req_tmp.find(".")
            result = parser.parseReq(req_tmp[0:req_end], major, dept)
            if result == []:
                print(c_id)
                print(parser.tokenizeReq(req_tmp[0:req_end], dept))

            s+=parser.list2Json(result, True)
            #s+=","
            desc_p = desc_p[req_end+1:]

        else:
            s+="{'course':'no req'}"
            #s+=","
    s+="}"

    return s

def scrapeStat():

    term = "20W"

    dept_name="Computer+Science"
    dept_id="COM+SCI"

    units="4.0"
    class_id="32"
    class_name="Introduction+to+Computer+Science+II"

    url="https://sa.ucla.edu/ro/Public/SOC/Results?t="
    url+=term
    url+="&sBy=units&meet_units="
    
    
    url+=units
    url+="&sName="
    
    url+=dept_name
    
    url+="+%28"
    
    url+="%29&subj="
    
    url+=dept_id
    url+="&crsCatlg="
   
    url+=class_id
    url+="+-+"
    
    url+="&catlg="
    
    url+="00"
    url+=class_id

    #request the webpage
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)

    #store the result in a string
    html = response.read().decode()

    #print(html)
    #pass it into PyQuery for parsing
    query = pq(html, parser='html')

    lec_table = query(".class-not-checked")

    for lec in lec_table:
        lec_id = pq(lec).attr('id')
        id_end = lec_id.find("_")

        lec_id = lec_id[0:id_end]
        print("---------")
        print(lec_id)
    
        lec_url="https://sa.ucla.edu/ro/public/soc/Results?t="
        lec_url+=term
        lec_url+='&sBy=classidnumber&id='
        lec_url+=lec_id
        lec_url+="&btnIsInIndex=btn_inIndex"

        #request the webpage
        request = urllib.request.Request(lec_url)
        response = urllib.request.urlopen(request)

        #store the result in a string
        html = response.read().decode()

        #print(html)
        #pass it into PyQuery for parsing
        query = pq(html, parser='html')

        dis_table = query("p[class='hide-small']")

        for dis in dis_table[1:]:
            print(pq(pq(dis).children()).text())



def main():
    
    #"""
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

    dept_li = query("a[href *= '/Academics/Course-Descriptions/Course-Details?SA=']")

    for li in dept_li:

        #get the href of the li 
        href = pq(li).attr('href')
        #get the name contained in the li
        name = pq(li).text()
        

        id_begin = href.find("?SA=")
        id_end = href.find("&")
        id = href[id_begin + 4:id_end]
        id = id.replace('%26','&')

        dept.append((id, name)) #add the dept id and name tuple to list

    #print(dept)

    dept_dict = dept.copy()

    for m in dept_dict:
       print(m)

    print("adding manual naming")

    dept_dict.append(('C&EE', 'Civil Engineering'))
    dept_dict.append(('EC+ENGR', 'Electrical Engineering'))
    dept_dict.append(('C&EE', 'Civil ENGR'))
    dept_dict.append(('EC+ENGR', 'Electrical ENGR'))
    dept_dict.append(('AERO+ENGR', 'Mechanical and Aerospace ENGR'))
    dept_dict.append(('CHEM', 'Chemistry'))
    dept_dict.append(('MAT+SCI', 'Materials Science'))
    dept_dict.append(('SEMITIC', 'SEMITICs'))

    
    print("scraping")

    i = 0
    
    for d in dept[11:]:

        print("scraping " + d[1])
        print(i)
        i = i + 1

        dept_id = d[0]
        
        dept_url="https://www.registrar.ucla.edu/Academics/Course-Descriptions/Course-Details?SA="
        #make sure to encode '&' as "%26"
        dept_url+=dept_id.replace("&", "%26")
        dept_url+="&funsel=3"

        dept_request = urllib.request.Request(dept_url)
        dept_response  = urllib.request.urlopen(dept_request)
        print(dept_url)
        #store the result in a string
        html = dept_response.read().decode("utf-8")
        #pass it into PyQuery for parsing
        query = pq(html, parser='html')

        courses = []
        course_div = query(".media-body")


        
        for div in course_div:
            courses.append(scrapeDiv(pq(div), dept_id, dept_dict))
            #print(courses[-1])

    
    """
    #test="two courses in FieldI, or course 20 and one course in FieldI"
    test=[]
    test.append("CS 100")
    test.append("CS 100 or CS 200")
    test.append("CS 100 and CS 200")
    test.append("one course from CS 100, CS 200, CS 300, or CS 400")
    test.append("CS 100 or CS 200 or CS 300 or CS 400")
    test.append("CS 100 and CS 101, or CS 400")
    test.append("two courses in FieldI")
    test.append("two courses in FieldI, or course 20 and one course in FieldI")
    test.append("CS 100 foo")

    """
    """
    #test="two courses in FieldI, or course 20 and one course in FieldI"
    test=[]
    #test.append(("courses 32, 33, 35L", "COM+SCI"))
    test.append(("courses 120A, 120B, 120C, or one year of introductory Middle Egyptian", "COM+SCI"))
    test.append(("course 10 or 10W or 20 or comparable knowledge in Asian American studies", "COM+SCI"))
    test.append(("three courses from COM+SCI 100 through COM+SCI 400", "COM+SCI"))
    test.append(("three courses from COM+SCI 100 through COM+SCI 400", "COM+SCI"))
    for i in test:
        print(i[0])
        s = parser.parseReq(i[0], i[1], dept_dict)
        print(s)
        #print(parser.list2Json(s))
        print("--------------------")
    """
    
    """
    #print(courses)

    #print(response.read().decode("utf-8"))
    """

    #parseStat()


if __name__ =="__main__":
    main()

