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
    result.append([])
    res_counter = 0
    expression=[]
    eq_class = []
    cur_course = ""
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
        #print(state)
        #print(tokens)
        #print(rule)
        #print("-------------")

        #if there are no tokens, it means the entire string was parsed
        if len(tokens) == 0:
            if cur_course != "":
                eq_class.append(cur_course)                         #finalize the equivalent class
            result[res_counter].append(eq_class.copy())                        #finalize the result
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
                    cur_course = ""
                    result[res_counter].append(eq_class.copy())                           #add the eq_class accumulated so far, as ', and' implies that eq_class was another requirement
                    eq_class.clear()
                    stack.insert(0, ["expression", tokens[2:], [-1, -1]])          #recursive
                    continue
                
                # , [expression]
                elif size > 1 and tokens[0] == ',' and tokens[1] == 'or':
                    if cur_course != "":
                        eq_class.append(cur_course)                         #finalize the equivalent class
                    cur_course = ""
                    result[res_counter].append(eq_class.copy())                           #"," is another way to say "and". We can say for sure, since ", or" would already have been handled above
                    eq_class.clear()

                    result.append([])
                    res_counter = res_counter + 1
                    stack.insert(0, ["expression", tokens[2:], [-1, -1]])          #recursive
                    continue
                
                # , [expression]
                elif size > 1 and tokens[0] == ',' and tokens[1] != "or":
                    eq_class.append(cur_course)                         #finalize the equivalent class
                    cur_course = ""
                    result[res_counter].append(eq_class.copy())                           #"," is another way to say "and". We can say for sure, since ", or" would already have been handled above
                    eq_class.clear()
                   
                    stack.insert(0, ["expression", tokens[1:], [-1, -1]])          #recursive
                    continue
                
                # and [eq_class]
                elif tokens[0] == 'and':
                    eq_class.append(cur_course)                         #finalize the equivalent class
                    cur_course = ""
                    result[res_counter].append(eq_class.copy())                           #"," is another way to say "and". We can say for sure, since ", or" would already have been handled above
                    eq_class.clear()
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
                    stack.pop(0)
                    stack[0][1] = tokens
                    stack[0][2] = [1, -1]
                    continue
                #...after parsing "course"
                if rule[0] == 4:
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
                elif rule[0] == 2:
                    #it means the or list finished parsing
                    stack.pop(0)
                    stack[0][1] = tokens
                    stack[0][2] = [1, -1]
                    continue

                else:
                    stack.pop(0)
                    stack[0][1] = tokens
                    stack[0][2] = [1, -1]  



            
            #[course]
            #if not a backtrack, we must start looking for a non-terminal that matches 
            else:
                 #[number]
               
                if isWordNum(tokens[0]):
                    #[num] year of [course]
                    if len(tokens) > 2 and tokens[1] == "year" and tokens[2] == "of":
                        cur_course=("%term-" + tokens[0] + ":")
                        stack.insert(0, ["name", tokens[3:], [-1, -1]])
        
                    #one course in [Field]
                    elif len(tokens) > 2 and (tokens[1] == 'course' or tokens[1] == "courses") and tokens[2] == 'in' and isField(tokens[3]):
                        eq_class.append("%" + tokens[0] + "-" + tokens[3])
                        stack.pop(0)
                        stack[0][1] = tokens[4:]
                        stack[0][2] = [2, -1]
                        continue
                    #one course from [or list]  
                    
                    elif (tokens[1] == 'course' or tokens[1] == 'courses') and tokens[2] == 'from':
                        #print("OR list")
                        if tokens[0] != "one":
                            eq_class.append("%" + tokens[0] + "-")
                        stack.insert(0, ["or_list", tokens[3:], [-1,-1]])
                        continue
                    else:
                        print("Syntax Error")
                        return []
                elif tokens[0] == "comparable" and tokens[1] == "knowledge":
                    cur_course=("%comp" + ":")
                    stack.insert(0, ["name", tokens[3:], [-1, -1]])
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

                elif size > 0 and tokens[0] == 'through':
                    #NOTE
                    #this is a special case that requires special syntax
                    eq_class[-1]+="through"   
                    eq_class.append(cur_course)                         #finalize the equivalent class
                    #eq_class.append(eq_class)                           #", or" implies that the class so far was optional  
                    stack.insert(0, ["course", tokens[2:], [-1, -1]])          #recursive
                    #stack[0][1] = tokens[2:]
                    #stack[0][2] = [2, -1]
                    continue
                
                # or [eq_class]
                elif size > 0 and tokens[0] == ',':
                    eq_class.append(cur_course)                         #finalize the equivalent class
                    #eq_class.append(eq_class)                           #", or" implies that the class so far was optional  
                    stack.insert(0, ["course", tokens[1:], [-1, -1]])          #recursive. Note adding or list to stack has the same effect
                    #stack[0][1] = tokens[1:]
                    #stack[0][2] = [2, -1]
                    continue
                #if above fails, it implies termination of or list, record eq class
                #TODO: use index to be more explicit about where the backtrack is from
                else:
                    eq_class.append(cur_course)
                    result[res_counter].append(eq_class.copy())
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
                #backtrack from name
                #possibly not used
                if rule[0] == 6:
                    stack.pop(0)
                    stack[0][1] = tokens
                    stack[0][2] = [4, -1]
                    continue

                else:
                    #with grade of
                    if tokens[0] == "with":
                        cur_course += ("%grade-" + tokens[4])

                    #(or <course>)
                    #elif tokens == "(or":
                    #    cur_course = ["%or", cur_course, tokens[1]]
                    
                    else:
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
                cur_course = cur_dept + " " + tokens[1]
                stack.pop(0)
                stack[0][1] = tokens[2:]
                stack[0][2] = [5, -1]
                continue
            elif isDept(tokens[0], dict) and hasDigit(tokens[1]):
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

        if state == "name":
            
            while len(tokens) > 0 and isDelim(tokens[0]) == False:
                cur_course += (tokens[0] + " ")
                tokens = tokens[1:]
            
            stack.pop(0)
            stack[0][1] = tokens
            stack[0][2] = [6, -1]

    #print(result)
    return result

#convert list to JSON
#note that True mans OR
def list2Json(list, stmt=True):

    s=""
    counter = 0
    #if the type of list content is a string, terminate and return it
    if isinstance(list, str):
        s+=("'course':" + "'" + list + "'")
        return s

    #if there is only 1 req in an OR, skip to next level
    if stmt and len(list) == 1:
        s+=list2Json(list[0], False)
        return s

    #list of options
    if stmt:
        for i in range(0,len(list)):
            s+=("'opt" + str(counter) + "':{")
            s+=list2Json(list[i],False)
            s+="}"

            counter = counter + 1

            if counter < len(list):
                s+=","
          
    #list of requirements
    else:
        for i in range(0,len(list)):
            s+=("'req" + str(counter) + "':{")
            s+=list2Json(list[i],True)
            s+="}"
            counter = counter + 1

            if counter < len(list):
                s+=","
            
    return s



