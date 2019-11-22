import urllib.request
import urllib.parse
import re

#class for each course
class Course:
        def __init__(self, name="", id="", level="lower", units=0, desc="", req=[[]], misc=0):
            self.name = name
            self.id = id
            self.level = level
            self.units = units
            self.desc = desc
            self.req = req
            self.misc = misc

def hasdigit(string):
    for c in string:
        if c.isdigit() == True:
            return True
    return False 

def parseDiv(html):
    
    html = html[f:] #delete chars before the div
    f = html.find("<h3>")
    html = html[f+4:] #delete chars before the h3
    f = html.find(".") #find where course ID ends
    id = html[0:f-1]

    html = html[f+1:]
    f = html.find("</h3>") #find where course name ends
    name = html[0:f-1]

    f = html.find("<p>Units: ")
    html = html[f+11:]
    units = int(html[0])

    f = html.find("<p>")
    html = html[f+3:]

    f = html.find("equisites: ")
    html = html[f+12:]
    e = html.find("equisites: ")


    req = parseReq(html)


def parseReq(html, major=""):

    token = html.split()
    print(token)
    result = []

    i = 0
    l = len(token)
    r_tmp = [] #stores the current req
    s_tmp = "" #builds a name
    m_tmp = "" #The major current being parsed
    pre_m = False #If the previous token was the name of a major

    state = "idle" #state of the parser

    while i < l:
       
        #if the token is 'course', the major name should be the current major
        if token[i] == "course":
            i = i + 1
            m_tmp = major
            continue
          
        
        #if the token is "courses"
        if token[i] == "courses":
            i = i + 1
            m_tmp = major
            continue

        #if the token is "choose one from"
        if token[i] == "one":
            if (i + 1) < l and token[i + 1] == "course":
                state = "one from"
                i = i + 3
                continue
            else:
                i = i + 1
                continue

        #if we are in a OR operation with token "one from"
        if token[i] == "or":
            if state == "one from":                     #if the "or" is the last part of a "choose one from" substring
                state = "last or"                       #set state to indicate the next class will be the last in an OR substring
            else:
                state = "or"                            #otherwise indicate this is an OR substring
            i = i + 1
            continue

        #if entering AND substring, and ensure and is not part of a major name
        if token[i] == "and" and pre_m == False:
            state = "idle"  
            i = i + 1
        else:

            if hasdigit(token[i]) == True:              #If this is a name of a class 
                pre_m = False
                if state == "last or" or (state == "or" and (token[i][-1] == ',' or i == l - 1)):#if this is the end of a OR substring
                    r_tmp.append(m_tmp + " " + token[i])      #add the next token as a potential required class
                    result.append(r_tmp.copy())
                    r_tmp.clear()                       #clear the tmp list
                    state = "idle"                      #reset state to default

                else:                                   #state is "idle"
                    if state == "idle" and len(r_tmp) > 0:#if there is a course that was already in r_tmp
                        result.append([r_tmp[0]])
                        r_tmp = r_tmp[1:]
                        r_tmp.append(m_tmp + " " + token[i])  
                    else:
                        r_tmp.append(m_tmp + " " + token[i])  #add this as a potential requirement
                   
            
            else:                                       #The only other possibility is that this token is part of the name of a major
                if pre_m == False:                      
                    m_tmp = token[i]
                    pre_m = True
                else:
                    m_tmp = m_tmp + " " + token[i] 
                
            i = i + 1


    if len(r_tmp) > 0:
        result.append(r_tmp)

    return result




def main():

    #The main course description page
    url="https://www.registrar.ucla.edu/Academics/Course-Descriptions"
    #request the webpage
    request = urllib.request.Request(url)
    response  = urllib.request.urlopen(request)

    #store the result in a string
    html = response.read().decode("utf-8")

    i = 0
    majors = []
    search_href = "a href=\"/Academics/Course-Descriptions/Course-Details?SA="

    while 1:
        f = html.find(search_href, i)
        if f < 0:
            break;
        else:
            html = html[f:] #delete chars before the href
            html = html[57:] #delete the href
            e = html.find('&') # see where the parameter ends
            id = urllib.parse.unquote(html[0:e])
            html = html[e:]

            f = html.find(">", i)
            e = html.find('</a>') # see where the parameter ends
            name = html[f+1:e-1]

            majors.append((id, name)) #add the major id and name tuple to list
            i = e
    
    #for m in majors:
    #    print(m)



    #major_id = "AERO+ST"
    #major_url="https://www.registrar.ucla.edu/Academics/Course-Descriptions/Course-Details?SA="
    #major_url+=major_id
    #major_url+="&funsel=3"

    #major_request = urllib.request.Request(url)
    #major_response  = urllib.request.urlopen(request)

    #html = major_response.decode("UTF-8")

    #while 1:
    #    f = html.find("media-body", i)
    #    if f < 0:
    #        break;
    #    else:
    #        html = html[f:]
    #        e = html.find("</div>")
    #
    #        parseDiv(html[0:e])
    #        html = html[e:]



    #print(response.read().decode("utf-8"))

    test = "Chemistry 20B, Life Sciences 2, 3, Mathematics 33B, Physics 1C"
    print(parseReq(test, "CS"))


if __name__ =="__main__":
    main()