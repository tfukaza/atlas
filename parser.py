import json

def tokenizeReq(string, dept_dict):

    #print("tokenizing")

    #l = list(string)

    for name in dept_dict:
        string = string.replace(name[1], name[0])

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

def isLevel(string):
    if string == "graduatelevel":
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

    #print(tok)
    result = []
    #result.append([])
    #res_counter = 0
    expression=[]
    #eq_class = []
    cur=""
    eq=[[]]
    #cur_course = ""
    cur_dept = ""

    i = 0
    stack = []
    stack.insert(0, ["expression", tok, [-1, -1]])
   
    #parseExp("expression", token)
    #, [-1, -1]

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
        #ret = stack[0][3]
        print(state)
        print(tokens)
        print(rule)
        print(eq)
        print("-------------")

        #if there are no tokens, it means the entire string was parsed
        if len(tokens) == 0:
            if cur != "":
                eq.append(cur)                         #finalize the equivalent class
            # if there is a single list in the result list, it means it is either a AND or OR that needs to have the remaining 
            # eq_class coupled to it. 
            if len(result) == 1 and isinstance(result[0], list):
                result[0].append(eq.copy())                        #finalize the result
            # if 
            else:
                result.append(eq.copy())     
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
                    #eq_class.append(cur_course)                         #finalize the equivalent class
                    #eq.append(cur)
                    #cur = ""
                    #cur_course = ""
                    #result[res_counter].append(eq_class.copy())                           #add the eq_class accumulated so far, as ', and' implies that eq_class was another requirement
                    while len(eq) > 1:
                        tmp = eq[-1]
                        eq.pop(-1)
                        eq[-1].append(tmp.copy())
                    
                    eq = [["%and", eq.copy()]]
                    #eq.clear()

                    stack.insert(0, ["expression", tokens[2:], [-1, -1]])          #recursive
                    continue
                
                # , [expression]
                elif size > 1 and tokens[0] == ',' and tokens[1] == 'or':
                    #if cur != "":
                    #   eq.append(cur)                         #finalize the equivalent class
                    #cur = ""
                    #result[res_counter].append(eq_class.copy())                           #"," is another way to say "and". We can say for sure, since ", or" would already have been handled above
                    #result = ["%or-one", eq.copy()]
                    #eq.clear()
                    while len(eq) > 1:
                        tmp = eq[-1]
                        eq.pop(-1)
                        eq[-1].append(tmp.copy())

                    eq = [["%or", eq.copy()]]
                    #if len(result) > 0 and result[0] == "%or":
                    #    result.append(eq.copy())   
                    #else:
                    #    result = ["%or", eq.copy()] 
                    #eq.clear()
                    #result.append([])
                    #res_counter = res_counter + 1
                    stack.insert(0, ["expression", tokens[2:], [-1, -1]])          #recursive
                    continue
                
                # , [expression]
                elif size > 1 and tokens[0] == ',' and tokens[1] != "or":
                    #eq_class.append(cur_course)                         #finalize the equivalent class
                    #cur_course = ""
                    #result[res_counter].append(eq_class.copy())                           #"," is another way to say "and". We can say for sure, since ", or" would already have been handled above
                    if len(eq) > 0 and eq[-1][0] == "%and":
                        if cur != "":
                            eq[-1].append(cur)   
                    else:
                        #tmp = eq[-1]
                        #eq.pop(-1)
                        #if isinstance(eq[0],str) and len(eq) == 1:
                        #    eq = ["%and", eq[0]] 
                        #else:
                        eq = [["%and", eq.copy()]]
                   
                    stack.insert(0, ["expression", tokens[1:], [-1, -1]])          #recursive
                    continue
                
                # and [eq_class]
                elif tokens[0] == 'and':
                    #eq_class.append(cur_course)                         #finalize the equivalent class
                    #cur_course = ""

                    if len(eq) > 0 and eq[-1][0] == "%and":
                        if cur != "":
                            eq[-1].append(cur)  
                    else:
                        #tmp = eq[-1]
                        #eq.pop(-1)
                        #if isinstance(eq[0],str) and len(eq) == 1:
                        #    eq = ["%and", eq[0]] 
                        #else:
                        eq = [["%and", eq.copy()]]
                    
                    #eq.clear()
                    stack.insert(0, ["expression", tokens[1:], [-1, -1]])          #recursive
                    continue
                
                #elif len(token) == 0, we are done. else, syntax error
                else:
                    print("syntax error")
                    return[]

            # otherwise, we need to check if the non-terminal is a [eq_class]
            else:
                stack.insert(0, ["eq_class", tokens, [-1, -1]])
                continue
        
        #[eq_class]
        if state == "eq_class":
            
          
            #if this is a backtrack 
            if rule[0] != -1:
                #backtrack from name
               
                if rule[0] == 6:
                    eq[-1].append(cur)      #add the last course parsed 
                    cur = ""    
                    stack.pop(0)
                    stack[0][1] = tokens
                    stack[0][2] = [1, -1]
                    continue
                #...after parsing "course"
                elif rule[0] == 4:
                    # , or [expression]
                    """if size > 1 and tokens[0] == ',' and tokens[1] == 'or':
                        eq_class.append(cur_course)                         #finalize the equivalent class
                        result[res_counter].append(eq_class.copy())                           #"," is another way to say "and". We can say for sure, since ", or" would already have been handled above
                        eq_class.clear()

                        result.append([])
                        res_counter = res_counter + 1
                        stack.insert(0, ["expression", tokens[2:], [-1, -1]])          #recursive
                        continue
                    """
                    # or [eq_class]
                    if tokens[0] == 'or':
                       
                        if len(eq) > 0 and eq[-1][0].find("%or") != -1:
                            if cur != "":
                                eq.append(cur)
                            cur=""
                            #print("i")   
                        else:
                            eq.append(["%or-one", cur]) 
                            cur = ""
                        #eq_class.append(eq_class)                           #", or" implies that the class so far was optional  
                        stack.insert(0, ["eq_class", tokens[1:], [-1, -1]])          #recursive
                        continue
                    
                    #else, we are done with this equivalence class
                    else:
                        #eq.append(cur)      #add this eq class
                        tmp = eq[-1]
                        eq.pop(-1)
                        eq[-1].append(tmp.copy())

                        cur = ""    
                        stack.pop(0)
                        stack[0][1] = tokens
                        stack[0][2] = [1, -1]
                        continue
                #..after parsing "or_list"
                
                else:
                    eq[-1].append(cur)      #add the last course parsed 

                    tmp = eq[-1]
                    eq.pop(-1)
                    eq[-1].append(tmp.copy())

                    cur = ""   
                    stack.pop(0)
                    stack[0][1] = tokens
                    stack[0][2] = [1, -1]
                    continue
                """elif rule[0] == 2:
                #it means the or list finished parsing
                eq.append(cur)      #add the last course parsed 

                #eq.append(cur)     #add this eq class
                tmp = eq[-1]
                eq.pop(-1)
                eq[-1].append(tmp.copy())

                cur = ""   
                stack.pop(0)
                stack[0][1] = tokens
                stack[0][2] = [1, -1]
                continue
                """


            
            #[course]
            #if not a backtrack, we must start looking for a non-terminal that matches 
            else:
                 #[number]
               
                if isWordNum(tokens[0]):
                    #[num] year of [course]
                    if len(tokens) > 2 and tokens[1] == "year" and tokens[2] == "of":
                        cur=("%term-" + tokens[0] + ":")
                        stack.insert(0, ["name", tokens[3:], [-1, -1]])
        
                    #one course in [Field]
                    elif len(tokens) > 2 and (tokens[1] == 'course' or tokens[1] == "courses") and tokens[2] == 'in' and isField(tokens[3]):
                        eq[-1].append("%field-" + tokens[0] + ":" + tokens[3])
                        
                        stack.pop(0)
                        stack[0][1] = tokens[4:]
                        stack[0][2] = [2, -1]
                        continue
                    #one course from [or list]  
                    
                    elif (tokens[1] == 'course' or tokens[1] == 'courses') and tokens[2] == 'from':
                        #print("OR list")
                        #if len(eq) > 0:
                        #    result.append(eq.copy())
                        
                        eq.append([("%or-" + tokens[0])])
                        #eq=[("%or-" + tokens[0])]
                        stack.insert(0, ["or_list", tokens[3:], [-1,-1]])
                        continue
                    else:
                        print("Syntax Error")
                        return []
                elif tokens[0] == "comparable" and tokens[1] == "knowledge":
                    cur=("%comp" + ":")
                    stack.insert(0, ["name", tokens[3:], [-1, -1]])
                else:
                    stack.insert(0, ["course", tokens, [-1, -1]])
                    continue

         #[eq_class]
        if state == "or_list":
            
            #if backtrack
             if rule[0] != -1:

                #
                if size > 1 and tokens[0] == ',' and (tokens[1] == 'or' or tokens[1] == "and"):
                    #eq.append(cur)                         #finalize the equivalent class
                    #eq_class.append(eq_class)                           #", or" implies that the class so far was optional  
                    stack.insert(0, ["course", tokens[2:], [-1, -1]])          #recursive
                    #stack[0][1] = tokens[2:]
                    #stack[0][2] = [2, -1]
                    continue

                elif size > 0 and tokens[0] == 'through':
                    eq[-1].append("%through")
                    cur = ""
                                        
                    stack.insert(0, ["course", tokens[1:], [-1, -1]])          #recursive
                    #stack[0][1] = tokens[2:]
                    #stack[0][2] = [2, -1]
                    continue
                
                # or [eq_class]
                elif size > 0 and tokens[0] == ',':
                    #eq.append(cur)                         #finalize the equivalent class
                    #eq_class.append(eq_class)                           #", or" implies that the class so far was optional  
                    stack.insert(0, ["course", tokens[1:], [-1, -1]])          #recursive. Note adding or list to stack has the same effect
                    #stack[0][1] = tokens[1:]
                    #stack[0][2] = [2, -1]
                    continue
                #if above fails, it implies termination of or list, record eq class
                #TODO: use index to be more explicit about where the backtrack is from
                else:
                    eq[-1].append(cur)
                    cur = ""
                    #result.append(eq.copy())
                    #eq.clear()
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
                #backtrack from name
                #possibly not used
                if rule[0] == 6:
                    #eq.append(cur)
                    stack.pop(0)
                    stack[0][1] = tokens
                    stack[0][2] = [4, -1]
                    continue

                else:
                    #with grade of
                    if tokens[0] == "with":
                        cur += ("%grade-" + tokens[4])

                    #(or <course>)
                    elif tokens[0] == "(or":
                        cur = ["%or-one", cur, ("tmp_dept" + tokens[1])]
                        eq[-1].append(cur)
                        cur = ""
                        stack.pop(0)
                        stack[0][1] = tokens[2:]
                        stack[0][2] = [4, -1]
                        continue

                    
                    else:
                        eq[-1].append(cur)
                        cur = ""
                        stack.pop(0)
                        stack[0][1] = tokens
                        stack[0][2] = [4, -1]
                        continue
            
            else:
                # num year of course
                #This is not called
                #TODO remove
                if isWordNum(tokens[0]) and len(tokens) > 2 and tokens[1] == "year" and tokens == "of":
                    stack.insert(0, ["name", tokens[3:], [-1, -1]])
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
            else:
                print("Syntax Error")
                return []

        if state == "name":
            
            while len(tokens) > 0 and isDelim(tokens[0]) == False:
                cur += (tokens[0] + " ")
                tokens = tokens[1:]
            #eq.append(cur)
            #eq.clear()
            stack.pop(0)
            stack[0][1] = tokens
            stack[0][2] = [6, -1]

    #print(result)
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








