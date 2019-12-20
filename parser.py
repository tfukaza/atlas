import json

def tokenizeReq(string, dept_dict):

    #print("tokenizing")

    #l = list(string)

    for name in dept_dict:
        string = string.replace(name[1], name[0])
    """
    #these manually handle rare expressions
    eq_dict=[]
    eq_dict.append(("equivalent", "%equivalent"))
    eq_dict.append(("compatible background", "%compatible"))
    eq_dict.append((" (may be taken concurrently)", "%con"))
    eq_dict.append(("at least one term of prior experience in same course in which collaborative learning theory is practiced and refined under supervision of instructors", "%%prior-exp"))

    for name in eq_dict:
        string = string.replace(name[0], name[1])
    """

    #s = "".join(l)
    s = string
    #print(s)

    tok = s.split() 
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

    return tok

def cleanID(s):
        
    while s[0] == ' ' or s[0] == ',':
        s = s[1:]
    
    while s[-1] == ' ' or s[-1] == ',':
        s = s[:-1]

    return s

def hasDigit(string):
    for c in string:
        if c.isdigit() == True:
            return True
    return False 

def isWordNum(string):
    if string == "one" or string == "two" or string == "three" or string == "four" or string == "five":
        return True
    return False

def isDept(string, dept_dict):
    for name in dept_dict:
        if string == name[0]:
            return True
    return False

def isField(string):
    if string == "FieldI":
        return True
    return False

def isDelim(string):
    if string == "," or string == "and" or string == "or":
        return True
    return False


def parseReq(html, major="", dict = []):

    tok = tokenizeReq(html, dict)
    result = []
    expression=[]
    cur=""
    cur_dept = ""
    
    eq=[[]]

    i = 0
    
    stack = []
    stack.insert(0, ["expression", tok, [-1, -1]])
   
    counter = 0

    while 1:

        counter = counter + 1

        if counter == 100:
            print("possible infinite loop")
            break

        state  = stack[0][0]
       
        tokens  = stack[0][1]
        rule = stack[0][2]
        size  = len(tokens)
       
        if False:
            print(state)
            print(tokens)
            print(rule)
            print(eq)
            print("-------------")

        #if there are no tokens, it means the entire string was parsed
        if len(tokens) == 0:
            if cur != "":
                eq[-1].append(cur)                        
        
            #append any remaining elements
            while len(eq) > 1:
                tmp = eq[-1]
                eq.pop(-1)
                if len(tmp) > 0:
                    while len(tmp) == 1 and not isinstance(tmp, str):
                        tmp = tmp[0]
                    
                    if isinstance(tmp, list):
                        eq[-1].append(tmp.copy())
                    else:
                        eq[-1].append(tmp)
            
            while len(eq) == 1 and not isinstance(eq, str):
                eq = eq[0]

            #exit loop
            result = eq    
            break

        #<expression>
        if state == "expression":

            # if this is a backtrack after parsing "eq_class"
            # Notice that in this state, we really don;t need to check the rule #,
            # as no other tokens begin with , and, , or and - it's just being done to keep it consistant with other states
            # It's also a safety measure in case unexpcted syntax appears
            if rule[0] != -1:
                # ,and and ,or are strong conjunctions, meaning it is by defintion the highest level of expression.
                # Thus we can assume all preceeding subexpressions have terminated,
                # and assume there is another subexpression following the token
                # , and [expression]
                if size > 1 and tokens[0] == ',' and tokens[1] == 'and':
                  
                    #append any remaining elements
                    while len(eq) > 1:
                        tmp = eq[-1]
                        eq.pop(-1)
                        if len(tmp) > 0:
                            eq[-1].append(tmp.copy())
                    
                    #clean up embedded lists
                    tmp = eq
                    while len(tmp) == 1 and not isinstance(tmp, str):
                        tmp = tmp[0]

                    # Add AND, and create a new eq list for the following subexpression
                    # This will be appended to the AND expression after the parser ends 
                    #if tmp is a list, make sure to use copy() if tmp is a list
                    if isinstance(tmp, list):
                        eq = [["%and", tmp.copy()],[]]
                    else:
                        eq = [["%and", tmp],[]]
                   

                    stack.insert(0, ["expression", tokens[2:], [-1, -1]])         
                    continue
                
                # ,or <expression>
                elif size > 1 and tokens[0] == ',' and tokens[1] == 'or':
                    
                    #append any remaining elements
                    while len(eq) > 1:
                        tmp = eq[-1]
                        eq.pop(-1)
                        if len(tmp) > 0:
                            eq[-1].append(tmp.copy())
                    
                    #clean up embedded lists
                    tmp = eq
                    while len(tmp) == 1 and not isinstance(tmp, str):
                        tmp = tmp[0]

                    #add OR
                    #if tmp is a list, make sure to use copy() if tmp is a list
                    if isinstance(tmp, list):
                        eq = [["%or?one", tmp.copy()],[]]
                    else:
                        eq = [["%or?one", tmp],[]]
                    
                   
                    stack.insert(0, ["expression", tokens[2:], [-1, -1]])         
                    continue
                   
                #TODO
                elif size > 1 and tokens[0] == ',' and tokens[1] == "with":
                    stack[0][1]= tokens[7:]
                    continue

                # , <expression>
                elif size > 1 and tokens[0] == ',':
                    
                    #append any remaining elements
                    while len(eq) > 1:
                        tmp = eq[-1]
                        eq.pop(-1)
                        if len(tmp) > 0:
                            eq[-1].append(tmp.copy())
                    
                    #check the most recent eq class
                    chk = eq[-1][0]

                    #',' has a higher precedence than "or" (but not ",or"), so if the last eq class is an "or"
                    # we must treat , as a strong conjuntion 
                    if isinstance(chk, str) and chk.find("%or") != -1:
                    
                        #clean up embedded lists
                        tmp = eq
                        while len(tmp) == 1 and not isinstance(tmp, str):
                            tmp = tmp[0]

                        #add AND
                        #if tmp is a list, make sure to use copy() if tmp is a list
                        if isinstance(tmp, list):
                            eq = [["%and", tmp.copy()],[]]
                        else:
                            eq = [["%and", tmp],[]]
                    
                        stack.insert(0, ["expression", tokens[1:], [-1, -1]])         
                        continue
                    #otherwise, treat ',' as a weak conjunction, i.e. same as "and"
                    else:
                        #if this is already a list of AND, simply append 
                        if len(eq) > 0 and len(eq[-1]) > 0 and eq[-1][0] == "%and":
                            if cur != "":
                                eq[-1].append(cur)   
                        #if this is a new list of AND, create the neccesary subexpression
                        else:
                            #pop the last expression
                            tmp = eq[-1]
                            eq.pop(-1)

                            #clean up embedded list
                            while len(tmp) == 1 and not isinstance(tmp, str):
                                tmp = tmp[0]

                            #if tmp is a list, make sure to use copy() if tmp is a list
                            if isinstance(tmp, list):
                                eq.append(["%and", tmp.copy()]) 
                            else:
                                eq.append(["%and", tmp]) 
                            
                            cur = ""
                    
                        stack.insert(0, ["expression", tokens[1:], [-1, -1]])         
                        continue
             

                # 'and' is a weak conjunction, meaning it may be part of a subexpression
                # Thus we cannot terminate preceding expressions
                # Instead, we simply create another subexpression and append it to the most recent expression
                elif tokens[0] == 'and':
                  
                    #if this is already a list of AND, simply append 
                    if len(eq) > 0 and eq[-1][0] == "%and":
                        if cur != "":
                            eq[-1].append(cur)   
                    #if this is a new list of AND, create the neccesary subexpression
                    else:
                        #pop the last expression
                        tmp = eq[-1]
                        eq.pop(-1)

                        #clean up embedded list
                        while len(tmp) == 1 and not isinstance(tmp, str):
                            tmp = tmp[0]

                        #if tmp is a list, make sure to use copy() if tmp is a list
                        if isinstance(tmp, list):
                            eq.append(["%and", tmp.copy()]) 
                        else:
                            eq.append(["%and", tmp]) 
                        
                        cur = ""
                   
                    stack.insert(0, ["expression", tokens[1:], [-1, -1]])         
                    continue
                
                
                #if all cases don't match, it is an error
                else:
                    print("syntax error")
                    return[]

            #if not a callback, we need to check if the non-terminal is a <eq_class>
            else:
                stack.insert(0, ["eq_class", tokens, [-1, -1]])
                continue
        
        #<eq_class>
        if state == "eq_class":
            
            #if this is a backtrack 
            if rule[0] != -1:

                #backtrack from <name>
                if rule[0] == 6:
                    if cur != "":
                        eq[-1].append(cur)    
                    cur = ""    
                    stack.pop(0)
                    stack[0][1] = tokens
                    stack[0][2] = [1, -1]
                    continue

                #after <course>
                elif rule[0] == 4:
                   
                    # or <eq_class>
                    if tokens[0] == 'or':
                       
                        # If we are already in an OR expression, sppend
                        if len(eq) > 0 and eq[-1][0].find("%or") != -1:
                            if cur != "":
                                eq[-1].append(cur)
                            cur=""
                        # If this is a start of an OR expression, create the expression
                        else:
                            tmp = eq[-1]
                            eq.pop(-1)

                            #clean up embedded list
                            while len(tmp) == 1 and not isinstance(tmp, str):
                                tmp = tmp[0]

                            if isinstance(tmp, str):
                                eq.append(["%or?one", tmp]) 
                            else:
                                eq.append(["%or?one", tmp.copy()]) 
                            cur = ""

                        stack.insert(0, ["eq_class", tokens[1:], [-1, -1]])         
                        continue
                    
                # If all above cases fail, we are at the end of this expression
                # we do not append the current eq class, as that is up to the <expression> level
                cur = ""    
                stack.pop(0)
                stack[0][1] = tokens
                stack[0][2] = [1, -1]
                continue
                
            #if not a backtrack, we must start looking for a non-terminal that matches 
            else:
                #<number>
                if isWordNum(tokens[0]):
                    #<num> year of <course>
                    if len(tokens) > 2 and tokens[1] == "year" and tokens[2] == "of":
                        cur=("%term-" + tokens[0] + ":")
                        stack.insert(0, ["name", tokens[3:], [-1, -1]])
        
                    #one course in <Field>
                    elif len(tokens) > 2 and (tokens[1] == 'course' or tokens[1] == "courses") and tokens[2] == 'in' and isField(tokens[3]):
                        eq[-1].append("%field-" + tokens[0] + ":" + tokens[3])
                        
                        stack.pop(0)
                        stack[0][1] = tokens[4:]
                        stack[0][2] = [2, -1]
                        continue

                    #one course from <or list>
                    elif (tokens[1] == 'course' or tokens[1] == 'courses') and tokens[2] == 'from':
                        eq.append([("%or?" + tokens[0])])
                        stack.insert(0, ["or_list", tokens[3:], [-1,-1]])
                        continue

                    else:
                        print("Syntax Error")
                        return []
                
                # comparable knowledge
                elif tokens[0] == "comparable" and tokens[1] == "knowledge":
                    cur=("%comp" + ":")
                    stack.insert(0, ["name", tokens[3:], [-1, -1]])

                else:
                    stack.insert(0, ["course", tokens, [-1, -1]])
                    continue

        #<or_list>
        if state == "or_list":
            
            #if backtrack
            if rule[0] != -1:

                #if this just returned from a final course
                if rule[1] == 1:
                    if cur != "":
                        eq[-1].append(cur)
                    cur = ""
                    stack.pop(0)
                    stack[0][1] = tokens
                    stack[0][2] = [2, -1]
                    continue

                #,or || ,and 
                elif size > 1 and tokens[0] == ',' and (tokens[1] == 'or' or tokens[1] == "and"):
                    #indictate that this is the final course in a or list
                    stack[0][2][1] = 1

                    stack.insert(0, ["course", tokens[2:], [-1, -1]])        
                    continue

                elif size > 0 and tokens[0] == 'through':
                    eq[-1].append("%through")
                    cur = ""
                                    
                    stack.insert(0, ["course", tokens[1:], [-1, -1]])          
                    continue
                
                # ,
                elif size > 0 and tokens[0] == ',':
                    stack.insert(0, ["course", tokens[1:], [-1, -1]])         
                    continue

                #if above fails, it implies termination of or list, record eq class
                else:
                    if cur != "":
                        eq[-1].append(cur)
                    cur = ""
                    stack.pop(0)
                    stack[0][1] = tokens
                    stack[0][2] = [2, -1]
                    continue

            else:
                stack.insert(0, ["course", tokens, [-1, -1]])
                continue
            
        #<course>
        if state == "course":

            #if this is a backtrack
            if rule[0] != -1:
                #backtrack from <name>
                #possibly not used
                if rule[0] == 6:
                    stack.pop(0)
                    stack[0][1] = tokens
                    stack[0][2][0] = 4
                    continue

                else:
                    #with grade of
                    #CURRENTLY NOT HANDLED
                    if tokens[0] == "with":
                        #cur += ("%grade-" + tokens[3])
                        eq[-1].append(cur)
                        cur = ""
                        stack.pop(0)
                        stack[0][1] = tokens[6:]
                        stack[0][2][0] = 4

                    #(<req>)
                    elif tokens[0][0] == "(":
                        #(or <course>)
                        if tokens[0] == "(or":
                            cur = ["%or?one", cur, (major + " " + tokens[1][0:-1])]
                            eq[-1].append(cur)
                            cur = ""
                            stack.pop(0)
                            stack[0][1] = tokens[2:]
                            stack[0][2][0] = 4
                            continue
                        #some other rare expression, parse as it is
                        else:
                            cur+="%"+tokens[0][1:]
                            tokens = tokens[1:]
                            while True:
                                cur+="-" + tokens[0]
                                tmp = tokens[0]
                                tokens = tokens[1:]
                                if tmp[-1] == ")":
                                    break
                            
                            eq[-1].append(cur)
                            cur = ""
                            stack.pop(0)
                            stack[0][1] = tokens
                            stack[0][2][0] = 4

                    #end of expression
                    else:
                        if cur != "":
                            eq[-1].append(cur)
                        cur = ""
                        stack.pop(0)
                        stack[0][1] = tokens
                        stack[0][2][0] = 4
                        continue
            
            else:
                stack.insert(0, ["course_id", tokens, [-1, -1]])
                continue

        if state  == "course_id":
            if (tokens[0] == "course" or tokens[0] == "courses") and hasDigit(tokens[1]):
                cur_dept = major
                cur = cur_dept + " " + tokens[1]
                stack.pop(0)
                stack[0][1] = tokens[2:]
                stack[0][2] = [5, -1]
                continue
            elif isDept(tokens[0], dict) and hasDigit(tokens[1]):
                cur_dept = tokens[0]
                cur =  tokens[0] + " " + tokens[1]
                stack.pop(0)
                stack[0][1] = tokens[2:]
                stack[0][2] = [5, -1]
                continue
            elif hasDigit(tokens[0]):
                if cur_dept=="":
                    cur_dept = major
                cur = cur_dept + " " + tokens[0]
                stack.pop(0)
                stack[0][1] = tokens[1:]
                stack[0][2] = [5, -1]
                continue
            elif tokens[0].find("%") != -1:
                    cur = tokens[0]
                    stack.pop(0)
                    stack[0][1] = tokens[1:]
                    stack[0][2] = [5, -1]
            #We have a rare expression, eg "compatible background" "equivalent"
            else:
                cur="%"
                while len(tokens) > 0 and not isDept(tokens[0], dict):
                    cur+=tokens[0]+"-"
                    tokens = tokens[1:]

                stack.pop(0)
                stack[0][1] = tokens
                stack[0][2] = [5, -1]
                

        if state == "name":
            
            while len(tokens) > 0 and isDelim(tokens[0]) == False:
                cur += (tokens[0] + " ")
                tokens = tokens[1:]
            stack.pop(0)
            stack[0][1] = tokens
            stack[0][2] = [6, -1]

    return result


def formatList(list):

    if list == []:
        return "???"

    s={}

    #if the type of list content is a string, terminate and return it
    if isinstance(list, str):
        return list
    
    #if there is only 1 req, skip to next level
    if len(list) == 1:
        s=formatList(list[0])
        return s


    if list[0] == "%and":
        tmp_list=[]
        
        for i in list[1:]:
            tmp_list.append(formatList(i))

        s["req"] = tmp_list
        

    elif list[0].find("%or") != -1:

        tmp_list = {}
        tmp_list["num"] = list[0][4:]
        options = []
        
        for i in list[1:]:
            options.append(formatList(i))
            
        tmp_list["list"] = options

        s["opt"] = tmp_list
    
    return s








