
import json
import parser 
import tool

class Agent:
    def __init__(self, name):
        self.req = []         # list of required courses/agents
        #self.taken = []         # list of completed courses
        #self.chk = None        # function to evaluate requirement (leaf only)

        #self.unit = 0           # number of taken units  
        #self.course = 0         # number of taken courses
        self.rules=[]
        self.name = name
        self.rules = []

        self.upd = None          # function to update above status


class OptAgent:
    def __init__(self, name):
        #self.agent = []         # list of required courses/agents
        #self.root_agent = []
        #self.rules = []
        self.options = [] #["", [], [], []] 
        self.name = name
       
        self.upd = None          # function to update above status

# Root agents are agents that have customized functions to evaluate major progress
# Unlike leaf agents, which operate on course, root agents operate on leaf agents

class RootAgent:
    def __init__(self, name):
        self.ref = []
        self.rules = []
        self.isClosed = False

        self.upd = None          # function to update status
        self.name = name

class RuleAgent:
    def __init__(self, name):
        self.ref = []
        self.name = name

def rec_print(result, depth = 0):

    print("".join(["\t" * depth]), end=" ")
    print("REQ:")

    for r in result:

        print("".join(["\t" * depth]), end=" ")
        print("Agent: " + r.name)


        if isinstance(r, OptAgent):
            print("".join(["\t" * depth]), end=" ")
            print("OPT: " + r.name)
            #depth = depth + 1
            for o in r.options:
                print("".join(["\t" * depth]), end=" ")
                print("option: " + o[0])
                rec_print(o[1], depth + 1)
                print("".join(["\t" * depth]), end=" ")
                grp_print(o[2], depth + 1)
        else:
            #print("".join(["\t" * depth]), end=" ")
            #print("param: " + r.name)
            for rule in r.rules:
                print("".join(["\t" * depth]), end=" ")
                print(rule.name)
                print("".join(["\t" * depth]), end=" ")
                print(rule.ref)
            print("".join(["\t" * depth]), end=" ")
            print(r.req)
            print("".join(["\t" * depth]), end=" ")
            print(r.chk)
            print("".join(["\t" * depth]), end=" ")
            print(r.upd)
        
        print("".join(["\t" * depth]), end=" ")
        print("---")

def grp_print(result, depth = 0):

    for g in result:
        print("".join(["\t" * depth]), end=" ")
        print("GROUP: " + g.name)
        for r in g.ref:
            print("".join(["\t" * depth]), end=" ")
            print("ref:" + r)

def parse():

    #root_buffer = []
    #req_buffer = []
    #group = []
    #opt = []
    #opt.append(OptAgent())
    #opt[-1].options.append({"id": "master", "agent": [], "root": [], "rule":[]})
    #output = ""
    indent = 0
    pre_indent = 0

    parser.build_mapping()

    with open("../frontend/majors/comsci.rq","r") as file:

        req = file.readlines()

        result = parse_req(req, 0, "expression", "")

        rec_print(result[0])
        grp_print(result[1])

def parse_req(req, l, state, req_name):

    root_buffer = []
    agent_buffer = []
    rule_buffer = []
    #group = []
    
    while l < len(req):
        

    
        line = req[l]

        #print(line)
        #print(state)

        #check and consume the indentation 
        indent = 0

        while line[0] == "\t":
            line=line[1:]
            indent = indent + 1
        #print(indent)
        
        length = len(line)

        if line[0] == "!":
            break
        
        if state == "expression":
            
            #GROUP
            if length > 2 and line[0] == "G" and line[1] == "R" and line[2] == "O":
                line = line[7:]

                #consume whitespace
                while line[0] == " " or line[0] == "\t":
                    line = line[1:]
                
                name = trim_nonalpha(line)

                if name[0:5] == "%anon":
                    name = name.split("?")
                    if len(name) > 1:
                        req_name = req_name + "." + name[1]
                    else:
                        req_name = req_name
                else:
                    req_name = name
                # Add another option 
                # By syntax this must be an instance of OptAgent 
                root_buffer.append(RootAgent(req_name))
                l = l + 1
                state = "group"

                continue
            
            #REQ
            elif length > 2 and line[0] == "R" and line[1] == "E" and line[2] == "Q":
                
                line = line[4:]
                #consume whitespace
                while line[0] == " " or line[0] == "\t":
                    line = line[1:]
                
                name = trim_nonalpha(line)

                
                if name[0:5] == "%anon":
                    name = name.split("?")
                    if len(name) > 1:
                        name = req_name + "." + name[1]
                    else:
                        name = req_name
                
                #If there is already a group in the buffer, add this req to its reference list 
                if len(root_buffer) > 0 and root_buffer[-1].isClosed == False:
                    root_buffer[-1].ref.append(name)
                
                #add this to buffer
                agent_buffer.append(Agent(name))

                state = "req"
                l = l + 1
                continue
            
            #OPT
            elif length > 2 and line[0] == "O" and line[1] == "P" and line[2] == "T":
                
                line = line[4:]
                #consume whitespace
                while line[0] == " " or line[0] == "\t":
                    line = line[1:]
                
                name = trim_nonalpha(line)

                if name[0:5] == "%anon":
                    name = name.split("?")
                    if len(name) > 1:
                        req_name = req_name + "." + name[1]
                    else:
                        req_name = req_name
                else:
                    req_name = name

                #If there is already a group in the buffer, add this req to its reference list 
                if len(root_buffer) > 0 and root_buffer[-1].isClosed == False:
                    root_buffer[-1].ref.append(req_name)
                
                #add this to buffer
                agent_buffer.append(OptAgent(req_name))

                state = "OPT"
                l = l + 1
                continue

            #RULE
            elif length > 2 and line[0] == "R" and line[1] == "U" and line[2] == "L":
                
                s = line.split()
                name = s[1]
                
                #rules in <expression> mst be global
                #add the rule to the rule list
                rule_buffer.append(RuleAgent(name))

                state="rule-global"
                l = l + 1
                continue


            #/option
            elif length > 2 and line[0] == "/" and line[1] == "o" and line[2] == "p":
                state = "opt"
                l = l + 1
                return [agent_buffer, root_buffer, rule_buffer, l]
            
            elif length > 2 and line[0] == "/" and line[1] == "g" and line[2] == "r":
                state = "group"
                l = l + 1
                return [agent_buffer, root_buffer, rule_buffer, l]
            
            else:
                l = l + 1
                continue
            
        elif state == "req":

            #course param
            if length > 2 and line[0] == "c" and line[1] == "o" and line[2] == "u":
                line = line[7:]

                #consume whitespace
                while line[0] == " " or line[0] == "\t":
                    line = line[1:]
                


                req_list = []
                #if the courses are already parsed
                if line[0] == "[":
                    #convert it to an object 
                    req_list = tool.string2list(trim_nonalpha(line))
                if line[0] == "%":
                    req_list = [trim_nonalpha(line)]
                #otherwise, parse the list
                else:
                    req_list = parser.parseReq(trim_nonalpha(line))

                #process req list
                req_list = tool.simplifyReq(req_list)

                agent_buffer[-1].req = req_list
                l = l + 1
                continue 
            
            #course param
            elif length > 2 and line[0] == "c" and line[1] == "h" and line[2] == "k":
                line = line[5:]
                agent_buffer[-1].chk = trim_nonalpha(line)
                l = l + 1
                continue
                
            elif length > 2 and line[0] == "u" and line[1] == "p" and line[2] == "d":
                line = line[5:]
                agent_buffer[-1].upd = trim_nonalpha(line)
                l = l + 1
                continue
            
            elif length > 2 and line[0] == "/" and line[1] == "R" and line[2] == "E":
                #This indicates a requirement is over
                state = "expression"
                l = l + 1
                continue
            
            elif length > 2 and line[0] == "R" and line[1] == "U" and line[2] == "L":
            
                    s = line.split()
                    name = s[1]

                    #rule in <REQ> must be local
                    agent_buffer[-1].rules.append(RuleAgent(name))

                    state="rule-local"
                    l = l + 1
                    continue
                #else if this rule is global
            #TODO RULE binded to group
            else:
                l = l + 1
                continue


        elif state == "OPT":
            #option
            if length > 2 and line[0] == "o" and line[1] == "p" and line[2] == "t":

                line = line[7:]

                #consume whitespace
                while line[0] == " " or line[0] == "\t":
                    line = line[1:]
                
                name = trim_nonalpha(line)
                # Add another option 
                # By syntax this must be an instance of OptAgent 

               
                agent_buffer[-1].options.append([name, [], [], [] ])
                print("ENTER OPT")
                #recursively parse all agents and rules in this option
                rec_result = parse_req(req, l+1, "expression", req_name)
                #record the result to the option
                agent_buffer[-1].options[-1][1] = rec_result[0].copy()
                agent_buffer[-1].options[-1][2] = rec_result[1].copy()
                agent_buffer[-1].options[-1][3] = rec_result[2].copy()
                print("EXIT OPT")
                state="OPT"
                l = rec_result[3]
                continue

            #/OPT
            elif length > 2 and line[0] == "/" and line[1] == "O" and line[2] == "P":
                state = "expression"
                l = l + 1 
                continue
            else:
                l = l + 1
                continue

        elif state == "rule-local":
            #course
            if (length > 2 and line[0] == "c" and line[1] == "o" and line[2] == "u") or line[0] == "A" or line[0] == "B":
                line = line[7:]
                #consume whitespace
                while line[0] == " " or line[0] == "\t":
                    line = line[1:]

                req_list = []
                #if the courses are already parsed
                if line[0] == "[":
                    #convert it to an object 
                    req_list = tool.string2list(trim_nonalpha(line))
                #otherwise, parse the list
                else:
                    req_list = parser.parseReq(trim_nonalpha(line))

                agent_buffer[-1].rules[-1].ref = req_list
                l = l + 1
                continue
            
            elif length > 2 and line[0] == "/" and line[1] == "R" and line[2] == "U":
                state = "req"
                l = l + 1
                continue

        elif state == "rule-global":
            #course
            if length > 2 and line[0] == "c" and line[1] == "o" and line[2] == "u":
                line = line[7:]
                #consume whitespace
                while line[0] == " " or line[0] == "\t":
                    line = line[1:]

                req_list = []
                #if the courses are already parsed
                if line[0] == "[":
                    #convert it to an object 
                    req_list = tool.string2list(trim_nonalpha(line))
                #otherwise, parse the list
                else:
                    req_list = parser.parseReq(trim_nonalpha(line))

                rule_buffer[-1].ref = req_list
                l = l + 1
                continue
            
            elif length > 2 and line[0] == "/" and line[1] == "R" and line[2] == "U":
                state = "expression"
                l = l + 1
                continue
        
        elif state == "group":
            if length > 2 and line[0] == "u" and line[1] == "p" and line[2] == "d":
                line = line[5:]
                root_buffer[-1].upd = trim_nonalpha(line)
                l = l + 1
                continue

            elif length > 2 and line[0] == "g" and line[1] == "r" and line[2] == "o":
                #recursively parse all agents and rules in this option
                rec_result = parse_req(req, l+1, "expression", req_name)
                #record the result
                agent_buffer = agent_buffer + rec_result[0].copy()
                # before updating the list of root agents, make sure to update the ref list of the 
                # group class for this group.
                for a in rec_result[0]:
                    root_buffer[-1].ref.append(a.name)
                
                #TODO ensure req's are not added to closed groups
                root_buffer = rec_result[1].copy() + root_buffer
                rule_buffer = rule_buffer + rec_result[2].copy()
            
                state="group"
                l = rec_result[3]
                continue

             #/GROUP
            elif length > 2 and line[0] == "/" and line[1] == "G" and line[2] == "R":
                state = "expression"
                l = l + 1 
                continue

        
    return [agent_buffer, root_buffer, rule_buffer, l]

    """

    for r in req_buffer:
        print(r.name)
        print(r.req)
        print(r.chk)
        print(r.upd)
        print("---")
    """

def trim_nonalpha(s):
    while not s[-1].isalpha() and not s[-1].isdigit():
        s = s[0:-1]
    return s

if __name__ == "__main__":
    parse()