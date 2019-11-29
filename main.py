import urllib.request
import urllib.parse
import re
from pyquery import PyQuery as pq 

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


def parseDiv(html, major=""):
    
    C = Course()

    query = pq(html, parser='html')
    title = query("h3").text()

    id_end = title.find(".") #find where course ID ends
    c_id = title[0:id_end]
    print(c_id)

    name = title[id_end + 2:]
    print(name)

    unit_p = query("p").eq(0).text()
    unit="" 
    unit_end = unit_p.find(":")

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
    
    print(unit)

    desc_p = query("p").eq(1).text()

    if desc_p[0] == '(':
        e = desc_p.find(')')
        desc_p = desc_p[e:]

    type_end = desc_p.find(".")
    type_tmp = desc_p[0:type_end]

    c_type = ""

    types = ['Laboratory','Lecture','Seminar','Tutorial']
    for t in types:
        if type_tmp.find(t) != -1:
            c_type = t

    desc_p = desc_p[type_end+1:]

    print(c_type)

    req_begin = desc_p.find("equisites: ")

    if req_begin != -1:
        req_tmp = desc_p[req_begin + 11:]
        req_end = desc_p.find(".")
        print(parseReq(desc_p[0:req_end]))
        desc_p = desc_p[req_end+1:]

    else:
        print("no req")


    #print(desc_p[:-3])

    print("---------")
  
    return C


def hasDigit(string):
    for c in string:
        if c.isdigit() == True:
            return True
    return False 

def isWordNum(string):
    if string == "one" or string == "two" or string == "three" or string == "four" or string == "five":
        return True
    return False

def isLevel(string):
    if string == "graduatelevel":
        return True
    return False

def isDept(string):
    if string == "CS":
        return True
    return False

def isField(string):
    if string == "FieldI":
        return True
    return False


def parseReq(html, major=""):

    tok = html.split() 
    l = len(tok)
    i = 0
    while i < l:
        if tok[i][-1] == ',':
            tok[i] = tok[i][0:-1] 
            tok.insert(i+1, ',')
            l = l + 1
            i = i + 2
        else:
            i = i + 1

    print(tok)
    result = []
    eq_class = []
    cur_course = ""
    cur_dept = ""

    i = 0
    stack = []
    stack.insert(0, ["expression", tok, [-1, -1]])
   
    #parseExp("expression", token)
    #, [-1, -1]

    while 1:

        state  = stack[0][0]
       
        tokens  = stack[0][1]
        rule = stack[0][2]
        size  = len(tokens)
        #ret = stack[0][3]
        print(state)
        print(tokens)
       
        #print(eq_class)

        #if there are no tokens, it means the entire string was parsed
        if len(tokens) == 0:
            if cur_course != "":
                eq_class.append(cur_course)                         #finalize the equivalent class
            result.append(eq_class.copy())                        #finalize the result
            break

        #[expression]
        if state == "expression":

            #if this is a backtrack after parsing "eq_class"
            #Notice that in this state, we really don;t need to check the rule#,
            # as no other tokens begin with , and, , or and - it's just being done to keep it consistant with other states
            #It's also a safety measure in case unexpcted syntax appears
            if rule[0] != -1:
                # , and [expression]
                if size > 1 and tokens[0] == ',' and tokens[1] == 'and':
                    eq_class.append(cur_course)                         #finalize the equivalent class
                    result.append(eq_class.copy())                           #add the eq_class accumulated so far, as ', and' implies that eq_class was another requirement
                    stack.insert(0, ["expression", tokens[2:], [-1, -1]])          #recursive
                    continue
                
                # , [expression]
                elif size > 1 and tokens[0] == ',' and tokens[1] == "or":
                    eq_class.append(cur_course)                         #finalize the equivalent class
                    tmp = eq_class                        #", or" implies that the class so far was optional  
                    eq_class.clear()
                    if len(tmp) == 1:
                        eq_class = tmp.copy()
                    else:
                        eq_class = [tmp.copy()]
                    stack.insert(0, ["expression", tokens[2:], [-1, -1]])          #recursive
                
                # , [expression]
                elif size > 1 and tokens[0] == ',' and tokens[1] != "or":
                    eq_class.append(cur_course)                         #finalize the equivalent class
                    result.append(eq_class.copy())                           #"," is another way to say "and". We can say for sure, since ", or" would already have been handled above
                    eq_class.clear()
                    stack.insert(0, ["expression", tokens[1:], [-1, -1]])          #recursive
                    continue
                
                """ # and [eq_class]
                elif tokens[0] == 'and':
                    eq_class.append(cur_course)                         #finalize the equivalent class
                    result.append(eq_class.copy())                           #"," is another way to say "and". We can say for sure, since ", or" would already have been handled above
                    eq_class.clear()
                    stack.insert(0, ["eq_class", tokens[1:], [-1, -1]])          #recursive
                    continue
                """
                #elif len(token) == 0, we are done. else, syntax error

            # otherwise, we need to check if the non-terminal is a [eq_class]
            else:
                stack.insert(0, ["eq_class", tokens, [-1, -1]])
                continue
        
        #[eq_class]
        if state == "eq_class":
            
          
            #if this is a backtrack 
            if rule[0] != -1:
                #...after parsing "course"
                if rule[0] == 4:
                    # , or [expression]
                    """if size > 1 and tokens[0] == ',' and tokens[1] == 'or':
                        eq_class.append(cur_course)                         #finalize the equivalent class
                        tmp = eq_class.copy()                           #", or" implies that the class so far was optional  
                        eq_class.clear()
                        if len(tmp) == 1:
                            eq_class = [tmp]
                        else:
                            eq_class = [tmp]
                        stack.insert(0, ["expression", tokens[2:], [-1, -1]])          #recursive
                        continue
                """
                    # or [eq_class]
                    if size > 1 and tokens[0] == 'or':
                        eq_class.append(cur_course)                         #finalize the equivalent class
                        #eq_class.append(eq_class)                           #", or" implies that the class so far was optional  
                        stack.insert(0, ["eq_class", tokens[1:], [-1, -1]])          #recursive
                        continue

                    #else, we are done with this equivalence class
                    else:
                        stack.pop(0)
                        stack[0][1] = tokens
                        stack[0][2] = [1, -1]
                        continue
                #..after parsing "or_list"
                if rule[0] == 2:
                    #it means the or list finished parsing
                    stack.pop(0)
                    stack[0][1] = tokens
                    stack[0][2] = [1, -1]
                    continue



            
            #[course]
            #if not a backtrack, we must start looking for a non-terminal that matches 
            else:
                 #[number]
               
                if isWordNum(tokens[0]):
                    """
                    #[level] [department] courses
                    if isLevel(tokens[1]) and isDept(tokens[2]) and tokens[3] == 'courses':
                        # not in [selection]
                        if tokens[4] == 'not' and tokens[5] == 'in':
                            stack[0][0] = "expression"                             #if this succeeds, return to the "expression state"
                            stack.insert(0, ("selection", tokens[6:]))
                        #in [selection]
                        elif tokens[4] == 'in':
                            stack[0][0] = "expression" 
                            stack.insert(0, ("selection", tokens[5:]))
                        else:
                            print("Syntax Error")
                            return []

                    # courses in [selection]
                    elif tokens[1] == 'courses' and tokens[2] == 'in':
                        stack.insert(0, ("selection", tokens[3:]))
                    """
                    #one course in [Field]
                    if len(tokens) > 2 and (tokens[1] == 'course' or tokens[1] == "courses") and tokens[2] == 'in' and isField(tokens[3]):
                        eq_class.append(tokens[0] + " in " + tokens[3])
                        stack.pop(0)
                        stack[0][1] = tokens[4:]
                        stack[0][2] = [2, -1]
                        continue
                    #one course from [or list]  
                    
                    elif tokens[1] == 'course' and tokens[2] == 'from':
                        print("OR list")
                        stack.insert(0, ["or_list", tokens[3:], [-1,-1]])
                        continue
                    else:
                        print("Syntax Error")
                        return []
                
                else:
                    stack.insert(0, ["course", tokens, [-1, -1]])
                    continue

         #[eq_class]
        if state == "or_list":
            
            #if backtrack
             if rule[0] != -1:

                 #
                if size > 1 and tokens[0] == ',' and tokens[1] == 'or':
                    eq_class.append(cur_course)                         #finalize the equivalent class
                    #eq_class.append(eq_class)                           #", or" implies that the class so far was optional  
                    stack.insert(0, ["course", tokens[2:], [-1, -1]])          #recursive
                    #stack[0][1] = tokens[2:]
                    #stack[0][2] = [2, -1]
                    continue
                
                # or [eq_class]
                elif size > 1 and tokens[0] == ',':
                    eq_class.append(cur_course)                         #finalize the equivalent class
                    #eq_class.append(eq_class)                           #", or" implies that the class so far was optional  
                    stack.insert(0, ["course", tokens[1:], [-1, -1]])          #recursive
                    #stack[0][1] = tokens[1:]
                    #stack[0][2] = [2, -1]
                    continue
                #if above 2 fails, it implies termination of or list
                #TODO: use index to be more explicit about where the backtrack is from
                else:
                    eq_class.append(cur_course)
                    eq_class.clear()
                    stack.pop(0)
                    stack[0][1] = tokens
                    stack[0][2] = [2, -1]
                    continue
             else:
                stack.insert(0, ["course", tokens, [-1, -1]])
                continue
            

        if state == "course":

            #if this is a backtrack
            if rule[0] != -1:
                if tokens[0] == "with":
                    print("Not supported yet")
                else:
                    stack.pop(0)
                    stack[0][1] = tokens
                    stack[0][2] = [4, -1]
                    continue
            
            else:
                stack.insert(0, ["course_id", tokens, [-1, -1]])

        if state  == "course_id":
            if (tokens[0] == "course" or tokens[0] == "courses") and hasDigit(tokens[1]):
                cur_dept = "this_dept"
                cur_course = cur_dept + " " + tokens[1]
                stack.pop(0)
                stack[0][1] = tokens[2:]
                stack[0][2] = [5, -1]
                continue
            elif isDept(tokens[0]) and hasDigit(tokens[1]):
                cur_dept = tokens[0]
                cur_course =  tokens[0] + " " + tokens[1]
                stack.pop(0)
                stack[0][1] = tokens[2:]
                stack[0][2] = [5, -1]
                continue
            elif hasDigit(tokens[0]):
                cur_course = cur_dept + " " + tokens[0]
                stack.pop(0)
                stack[0][1] = tokens[1:]
                stack[0][2] = [5, -1]
                continue
            else:
                print("Syntax Error")
                return []

    return result

"""
def parseExp(state, tokens):

    result = []

    #[expression] = 
    if state == "expression":

        result = parseExp("eq_class", tokens)
        # [eq_class] [subexpression]
        if len(result) != 0



    return result

"""
"""
def parseReq(html, major=""):

    token = html.split()
    #print(token)
    result = []

    i = 0
    l = len(token)
    r_tmp = [] #stores the current req
    s_tmp = "" #builds a name
    m_tmp = "" #The major current being parsed
    pre_m = False #If the previous token was the name of a major

    state = "idle" #state of the parser

    while i < l:

        #handle expressions '[number] course from [list of courses or field]'
       
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

        #if the token is "choose one (course) from"
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
                    r_tmp.append(cleanID(m_tmp + " " + token[i]))      #add the next token as a potential required class
                    result.append(r_tmp.copy())
                    r_tmp.clear()                       #clear the tmp list
                    state = "idle"                      #reset state to default

                else:                                   #state is "idle"
                    if state == "idle" and len(r_tmp) > 0:#if there is a course that was already in r_tmp
                        result.append([r_tmp[0]])
                        r_tmp = r_tmp[1:]
                    
                    r_tmp.append(cleanID(m_tmp + " " + token[i]))  
                    #add this as a potential requirement
                   
            
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
"""

def cleanID(s):
        
    while s[0] == ' ' or s[0] == ',':
        s = s[1:]
    
    while s[-1] == ' ' or s[-1] == ',':
        s = s[:-1]

    return s

def main():
    """
    #The main course description page
    url="https://www.registrar.ucla.edu/Academics/Course-Descriptions"
    #request the webpage
    request = urllib.request.Request(url)
    response  = urllib.request.urlopen(request)

    #store the result in a string
    html = response.read().decode()
    #pass it into PyQuery for parsing
    query = pq(html, parser='html')

    i = 0
    dept = []

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

    for m in dept:
        print(m)

    """

    """dept_id = "AERO+ST"
    dept_url="https://www.registrar.ucla.edu/Academics/Course-Descriptions/Course-Details?SA="
    dept_url+=dept_id
    dept_url+="&funsel=3"

    dept_request = urllib.request.Request(dept_url)
    dept_response  = urllib.request.urlopen(dept_request)

    #store the result in a string
    html = dept_response.read().decode("utf-8")
    #pass it into PyQuery for parsing
    query = pq(html, parser='html')

    courses = []
    course_div = query(".media-body")


    """
    #for div in course_div:
    #    courses.append(parseDiv(pq(div)))
   
    test="two courses in FieldI, or course 20 and one course in FieldI"
    #test="two courses in FieldI"


    print(parseReq(test))

    #print(courses)

    #print(response.read().decode("utf-8"))


if __name__ =="__main__":
    main()