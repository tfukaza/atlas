import db


# agents are objects that manages major requirements
# they keep states that record:
# - If the requirement it manages has been satisfied or not
# - how many units have been completed for the requirement
# - how many courses
# - list of required courses 
# In additon, each agent has a function that evaluates if the requirement is satisfied
# For a non-leaf agent, this will usually evaluate total units of child agents, etc.
# A leaf agent will usually have a public list of required courses,
# which an evaluator will inspect and update the state of the agent 
# The agent's function will then inspect its own state, and update 
# other stats as needed

class Agent:
    def __init__(self, req, eval, desc, unit, course, upd):
        self.req = req          # list of required courses/agents
        self.taken = []         # list of completed courses
        self.eval = eval        # function to evaluate requirement (leaf only)

        self.done = False       # if req is met or not
        self.unit = 0           # number of taken units  
        self.course = 0         # number of taken courses
        self.req_unit = unit    # number of required units  
        self.req_course = course# number of required courses
        self.desc = desc

        self.upd = upd          # function to update above status

    def evaluate(self, c):
        return self.eval(self, c)

    def update(self):
        return self.upd(self)

# Root agents are agents that have customized functions to evaluate major progress
# Unlike leaf agents, which operate on course, root agents operate on leaf agents

class RootAgent:
    def __init__(self, desc, agents, s, e, upd):
        self.agents = agents          # list of leaf agents
        self.s = s
        self.e = e

        self.done = False       # if req is met or not
        self.upd = upd          # function to update status
        self.desc = desc

    def evaluate(self, c):
        return self.eval(self, c)

    def update(self):
        return self.upd(self)

# Used by nonleaf agents to alert caller that this is not a leaf, ie 
# cannot evaluate a class
def notLeaf(self, c):
    return False

# given a course, checks to see if it satsifies a req
# This is the most basic function to check requirements
# If yes, removes the requirement from req, updates stats, and returns true
# If no, returns False
# TODO consider number of units as well
# TODO consider passing list as arrays so any number of arguments can be passed easily
def chkAllReq(self, c):
    result = chkReq(self.req, c)
    
    if result[0] == True:
        self.req = result[1]
        self.course = self.course + 1
        self.taken.append(c) 
        return True
    
    return False

def updateLeaf_1(self):
    if self.course >= self.req_course:
        self.done = True


#def ifSatMin(n):
#    return lambda m, n : True if m >= n else False
 
# Given a major and a list of completed courses, 
# this function will return a JSON list of courses that can be taken for each major requirement.
# Note the function does NOT send enrollement info of course - just the name of courses
def checkReq(major="CS", courses=[]):

    if major == "CS":
        return chkCOMSCI(courses)

# Given a list of complete course, return what courses needs to be taken for 
# each requirement

def chkCOMSCI(courses):

    #init agents
    agents=[]
    #Agents at the beginning of the array are leafs, while rear agents are non-leafs

    # Preparation for the Major
    # Computer Science 1, 31, 32, 33, 35L
    
    agents.append(
        Agent(  ['%and', 'COM+SCI 1','COM+SCI 31','COM+SCI 32','COM+SCI 33','COM+SCI 35L', 'COM+SCI M51A'],
                chkAllReq,
                "Prep-1",
                -1,
                3,
                updateLeaf_1
            )
    )
    # Mathematics 31A, 31B, 32A, 32B, 33A, 33B, 61
    agents.append(
        Agent(  ['%or', 'MATH 31A','MATH 31B','MATH 32A','MATH 32B','MATH 33A','MATH 33B','MATH 61'],
                chkAllReq,
                "Prep-2",
                -1,
                3,
                updateLeaf_1
            )
    )
    # Physics 1A, 1B, 1C, and 4AL or 4BL.
    agents.append(
        Agent(  ['%or', 'PHYSICS 1A','PHYSICS 1B','PHYSICS 1C', 'PHYSICS 4AL','PHYSICS 4BL', 'PHYSICS 4CL'],
                chkAllReq,
                "Prep-2",
                -1,
                3,
                updateLeaf_1
            )
    )

    #non-leaf agent
    root_agents=[]

    def update_1(self):

        isDone = False
        netCourse = 0

        for a in self.agents[self.s:self.e+1]:
            if a.done == True:
                isDone = True
            netCourse = netCourse + a.course

        if isDone and netCourse >= 4:
            self.done = isDone

    root_agents.append(
        RootAgent(  
            "major-2",
            agents,
            1,
            2,
            update_1
            )
    )

    response = {}
    response["req"] = []

    #for each course...
    for c in courses:

        #check each requirement and see which requirement it fulfills
        for a in agents: 

            #If this requirement is already fulfilled, move on to the next requirement
            if a.done == True:
                continue
            
            # See if this course satisifies a requirement
            res = a.evaluate(c)
            # If it does, move onto the next course
            if res:
                continue
    
    # At this point agent.req in each agent will contain the remaining course
    # that has to be taken. 

    #Call update on all agents
    for a in agents:
        a.update()

    for a in root_agents:
        a.update()

    # TODO inspect edge cases manually
    # Credit is not allowed for both Computer Science 170A and Electrical and Computer Engineering 133A unless at least one of them is applied as part of the science and technology requirement or as part of the technical breadth area. 
    
    # inpect all leaf agents, and for all unfinshed req, record the courses that can be taken
    for a in agents:
      
        tmp = {}
        #if this course has been completed
        if a.done == True:
            tmp["desc"] = "*" + a.desc #add a star to indicate completion
            tmp["req"] = [] 
        else:
            tmp["desc"] = a.desc
            tmp["req"] = flattenReq(a.req)

        tmp["taken"] = a.taken

        response["req"].append(tmp)

    # inpect all root agents
    for a in root_agents:
      
        tmp = {}
        #if this req has been completed
        if a.done == True:
            tmp["desc"] = "*" + a.desc #add a star to indicate completion
            tmp["req"] = [] 
            #mark all child agnets as done as well
            for i in range(a.s,a.e+1):
                response["req"][i]["desc"] = "*" +  response["req"][i]["desc"]
                response["req"][i]["req"] = []
        else:
            tmp["desc"] = a.desc
            tmp["req"] = []

        tmp["taken"] = []

        response["req"].append(tmp)


    return response



# A helper function 
# Given a list of requirements and a course...
# If the course satisfies some requirement, returns True and a new req list
# If not, returns False with the same list as before

def chkReq(req, course):

    if isinstance(req, str):
        if req == course:
            return (True, [])
        else:
            return (False, req)

    #if the list is empty, all req has been met
    if len(req) == 0:
        return (True, [])
    
    if len(req) == 1:
        if isinstance(req, str):
            if req == course:
                return (True, [])
            else:
                return (False, req)
        else:
            return chkReq(req[0], course)

    #if the first element is not %and or %or, it is a list of elements
    if req[0][0:4] != "%and" and req[0][0:3] != "%or":
        #if this course satisifies a req
        if req[0] == course:
            return (True, [])
        else:
            return (False, req)
 
    isAND = False
    isDemolish = False
    orCount = 1
    if req[0][0:4] == "%and":
        isAND = True
    else:
        orCount = word2num(req[0][4:])
    
    # If the list is an %and, if a match is found return (req - course)
    # If %or, if a match is found return [] 

    for i in range(1, len(req)):

        #if this is a string, inspect it
        if isinstance(req[i], str):
            if req[i] == course:
                #if the list is an AND, remove this from the list 
                if isAND:
                    req.pop(i)
                    #If there are more elements in the AND list, return True and the remaining req
                    if len(req) > 1:
                        return (True, req)
                    #if this was the last element, return []
                    else:
                        return (True, [])
                #if OR...
                else:
                    orCount = orCount - 1 
                    #if we have satisfied all req for an OR
                    if orCount == 0:
                        return (True, [])
                    #else we still have to select elements from this list
                    req[0] = "%or?" + num2word(orCount)
                    req.pop(i)
                    
                    return (True, req)        
                    
            else:
                continue
        #if this is a another list, recursively check
        else:
            result = chkReq(req[i], course)
            #if the course satisifies some requirement
            if result[0] == True:
                if isAND:
                    #remove the element
                    req.pop(i)
                    #if there still requirements (e.g. list is another AND)
                    if len(result[1]) > 0:
                        #add reaming requirements to req
                        req.insert(i, result[1])
                    return (True, req)
                else:
                    #remove the element
                    req.pop(i)
                    #if there still requirements (e.g. list is another AND)
                    if len(result[1]) > 0:
                        #add reaming requirements to req
                        req.insert(i, result[1])
                        return (True, req)
                    else:
                        orCount = orCount - 1 
                        #if we have satisfied all req for an OR
                        if orCount == 0:
                            return (True, [])
                        #else we still have to select elements from this list
                        req[0] = "%or?" + num2word(orCount)
                        req.pop(i)
                        return (True, req) 

            else:
                continue
    
    #If none of the req matched, return False
    return (False, req)


def word2num(word):
    if word == "one":
        return 1
    elif word == "two":
        return 2
    elif word == "three":
        return 3
    elif word == "four":
        return 4
    else:
        return 5

def num2word(num):
    if num == 1:
        return "one"
    elif num == 2:
        return "two"
    elif num == 3:
        return "three"
    elif num == 4:
        return "four"
    else:
        return "five"
