/*  This JS file contains the framework used to express  
*   major requirements in a systematical way
*/
//======================
//Global variables
//======================

//agents
let agents= [];
//root agents
let root_agents= [];
//rules
let rules = [];
//global list of completed courses 
let taken = []

//======================
//Class declarations
//======================

/*  Agent classes are abstract representations of a major requirements.
*   Each agent contains a list of courses in this.req.
*   For every course that the user completes, the function assinged to chk
*   is called with the course name as the parameter.
*   After all checks are complete, upd will be called once to
*   determine if this requirement has been completed or not.
*/ 
class Agent{

    constructor(name, req){

        this.name = name;       //name of this requirement

        this.req = req;         // list of required courses/agents
        this.taken = [];        // list of completed courses
        this.rules= [];         //List of rules unique to this agent
        
        this.chk = null;        // function to evaluate requirement (leaf only)
        this.upd = null;        // function to update above status

        this.done = false;      // if req is met or not
        this.unit = 0;          // number of taken units  
        this.course = 0;        // number of taken courses
        
    }
}
/*  Root Agent classes are similar to Agent classes, except for two key differences
    First, root agents operate on other agents, not courses.
    Second, there is no chk function - only the upd function.
*/ 
class RootAgent {

    constructor(name, ref){

        this.name = name;

        this.ref = ref;    //list of leaf agents

        this.done = false;       // if req is met or not
        this.upd = null;
    
    }
}
/*  Rules are various restrictions imposed on major requirements
    All rules are checked every time a new course is evaluated against each agent.
    In other words, rules will be called O(c * a * r) times.
*/
class Rule{
    constructor(name, ref, chk = null){

        //this.name = name;
        this.ref = ref;    
        this.chk = chk;
    }
}


/*
    Below are functions that can be passed to agents and rules.
    Be sure to bind them accordingly
*/

//Agent check functions

//Given a course, check if it satisfies a requirement
//If yes, update agent parameters and return true
//If no, return false
function check(c){

    //check if this course satisifes all rules
    r_len = this.rules.length

    for (let i = 0; i < r_len; i++){
        //evaluate the rule
        let chk = this.rules[i](c);
        if (!chk)
            return false;
    }

    //evaluate the course
    result = chkReq(this.req, c)

    if (result["res"]){
        this.req = result["list"];
        if (this.req.length == 0){
            this.done = true;
        }
        this.course = this.course + 1;
        this.taken.push(c); 
        taken.push(c); 
        //console.log("OK");
        return true;
    }
    //console.log("fail");
    return false;
}

//Agent update functions

//Update status of agent
function finish(course, unit){
    if (this.course >= course && this.unit >= unit){
        this.done = true;
    }
}

//Root agent update functions

//Update status of root agent
//This is used when the total unit/course in the group needs
//to exceed a certain threshold, with no restriction on which class to take from which subgroup 
function finish_agent(courses, units){

    let net_course = 0;
    let net_unit = 0;

    //inspect all agents it refers to
    this.ref.forEach(r => {
        //search for the agent this refers to 
        agents.forEach(a =>{
            //if we have found the referred agent, inspect it
            if (a.name.localeCompare(r) == 0){
                net_course+=a.course;
                net_unit+=a.course;
            }
        });
    });

    if (net_course >= courses && net_unit >= units){
        this.done = true;
    }
}

//Update status of root agent
//This is used when the total unit/course in the group needs
//to exceed a certain threshold, 
//and in addition at least N subgroup has to have done == true
function finish_agent_subgrp(courses, units, subgrp){

    let net_course = 0;
    let net_unit = 0;
    let net_grp = 0;

    //inspect all agents it refers to
    this.ref.forEach(r => {
        //search for the agent this refers to 
        agents.forEach(a =>{
            //if we have found the referred agent, inspect it
            if (a.name.localeCompare(r) == 0){
                net_course+=a.course;
                net_unit+=a.course; 
                if (a.done == true){
                    net_grp++;
                }
            }
           
        });
    });

    if (net_course >= courses && net_unit >= units && net_grp >= subgrp){
        this.done = true;
    }
}

//Rule functions

//Given a set and a course,
//return true if this course is not in the set, or other courses in the set has not been used for the major yet
//return false if another course in the set has already been used for the major
function subset_restriction(set, course){

    //if course is not in set, this restriction is not applicable, return true
    let isInSet = false;
    set.forEach(e => {
        if (course.localeCompare(e) == 0){
            isInSet = true;
        }
    }); 

    if(!isInSet){
        return true;
    }
    isInSet = true;
    //see if another course in the set has been used already
    set.forEach(s => {
        taken.forEach(t => {
            if (t.localeCompare(s) == 0){
                isInSet = false;
                console.log(s  + "," + t);
            }
        });
    }); 
   

    return isInSet;
}

//For a given set, the function will first inspect to see if course is in set
//If not, it will return True, as this rule is not applicable
//Otherwise, it will see if the course has been taken yet for any other requirement
//If yes, it will return False
function not_used_for_other(set, course){

    let isInSet = false;

    set.forEach(e => {
        if (course.localeCompare(e) == 0){
            isInSet = true;
        }
    }); 

    if (!isInSet)
        return true;
    
    taken.forEach(e => {
        if (course.localeCompare(e) == 0){
            isInSet = false;
        }
    });

    return isInSet;
}

//TODO
//Credit for A is allowed only if B has not been applied for credit yet 



//====================
// Functions to audit
//====================
//Main function to audit the major progress

function audit_run(courses, option){

    let res = audit_build(option);

    //let agents = res["agents"];
    //let root_agents = res["root_agents"];
    //let rules = res["rules"];

    let response = {};
    response["req"] = [];
    response["not"] = [];

    console.log(courses);

    //for each course...
    for (let c = 0; c < courses.length; c++){
        //console.log(courses[c]);
        let isVio = false;
        //check if this course conflicts with any restrictions that prevent it from being applied towards major completion
        for (let t = 0; t < rules.length; t++){
            //if this course violates any restrictions imposed...
            //console.log(courses[c]);
            if (!rules[t].chk(courses[c])){
                //skip this course, and record it
                response["not"].push(courses[c]);
                isVio = true;
            }
        }

        if(isVio)
            continue;

        //check each requirement and see which requirement it fulfills
        for (let a = 0; a < agents.length; a++){ 
            //console.log(agents[a].name);
            //if ( this requirement is already fulfilled, move on to the next requirement
            if (agents[a].done){
                continue;
            }

            //check to make sure all local rules are satisfied
            let isOK = true;
            agents[a].rules.forEach(e=>{
                if ((courses[c]) == false){
                    isOK = false;
                    //console.log("ret");
                    return;
                }
            });

            if(!isOK){
                //console.log("fail rule");
                continue;
            }
            
            // See if this course satisifies a requirement
            //console.log(courses[c]);
            let res = agents[a].chk(courses[c]);
            // If it does, move onto the next course
            if (res){
                //console.log("brak");
                break;
            }
        }
    }
    // At this point agent.req in each agent will contain the remaining course
    // that has to be taken. 

    //Call update on all agents
    agents.forEach(a => a.upd());
    root_agents.forEach(a => a.upd());

    //console.log(agents);

    // TODO inspect edge cases manually
    // Credit is not allowed for both Computer Science 170A and Electrical and Computer Engineering 133A unless at least one of them is applied as part of the science and technology requirement or as part of the technical breadth area. 
    
    // inpect all leaf agents, and for all unfinshed req, record the courses that can be taken
    for (let a = 0; a < agents.length; a++){
        
        ag = agents[a]
        tmp = {}
        //if this course has been completed
        if (ag.done){
            tmp["name"] = "*" + ag.name; //add a star to indicate completion
            tmp["req"] = []; 
        }
        else{
            tmp["name"] = ag.name;
            tmp["req"] = flattenReq(ag.req);
        }

        tmp["taken"] = ag.taken;

        response["req"].push(tmp);
    }

    // inpect all root agents
    root_agents.forEach(function(a){
      
        tmp = {}
        //if this req has been completed
        if (a.done){
            tmp["name"] = "*" + a.name; //add a star to indicate completion
            tmp["req"] = []; 
            /*//mark all child agents as done as well
            for (let i = a.s; i <= a.e; i++){
                response["req"][i]["name"] = "*" +  response["req"][i]["name"];
                response["req"][i]["req"] = [];
            }*/
        }
        else{
            tmp["name"] = a.name;
            tmp["req"] = [];
        }

        tmp["taken"] = [];

        response["req"].push(tmp);

    });

    return response;
}

// Given a list of requirements and a course...
// If the course satisfies some requirement, returns true and a new req list
// If not, returns false with the same list as before

function chkReq(req, course){

    //console.log(req);

    if (typeof(req) == "string"){
        //console.log("isstring");
        if (req.localeCompare(course) == 0)
            return {"res":true, "list":[]};
        else
            return {"res":false, "list":req};
    }

    

    // if the list is empty, all req has been met and there is nothing t satisfy
    if (req.length == 0)
        return {"res":false, "list":[]};
    
    if (req.length == 1){
        if (typeof(req) == "string"){
            if (req.localeCompare(course) == 0)
                return {"res":true, "list":[]};
            else
                return {"res":false, "list":req};
        }
        else
            return chkReq(req[0], course);

    }

    //console.log(req[0].substring(0,3));

    
    //if the first element is not %and or %or, it is a list of elements
    if ((req[0].substring(0,4)).localeCompare("%and") != 0 && 0 != (req[0].substring(0,3)).localeCompare("%or")){
        //if this course satisifies a req
        if (req[0].localeCompare(course) == 0)
            return {"res":true, "list":[]};
        else
            return {"res":false, "list":req};
    }
 
    let isAND = false;
    //let isDemolish = false;
    let orCount = 1;
   
    //console.log(req[0]);

    if (req[0].substring(0,4).localeCompare("%and") == 0){
        isAND = true;
        //console.log(isAND);
    }
    else
        orCount = word2num(req[0].substring(4));
    
    // If the list is an %and, if a match is found return (req - course)
    // If %or, if a match is found return [] 

    for(let i = 1; i < req.length; i++){

        //if this is a string, inspect it
        if (typeof(req[i]) == "string"){
            //console.log("String:" + req[i]);
            if (req[i].localeCompare(course) == 0){
                //console.log("match" + req[i] + course);
                //if the list is an AND, remove this from the list 
                if (isAND){
                    req.splice(i,1);
                    //If there are more elements in the AND list, return true and the remaining req
                    if (req.length > 1)
                        return {"res":true, "list":req};
                    //if this was the last element, return []
                    else
                        return {"res":true, "list":[]};
                }
                //if OR...
                else{
                    orCount--;
                    //console.log(orCount);
                    //if we have satisfied all req for an OR
                    if (orCount == 0){
                        return {"res":true, "list":[]};
                    }
                    //else we still have to select elements from this list
                    req[0] = "%or?" + num2word(orCount);
                    req.splice(i, 1);
                    
                    return {"res":true, "list":req};
                }  
            }
            else
                continue;
        }
        //if this is a another list, recursively check
        else{
            //console.log("List:");
            //console.log(req[i]);
            result = chkReq(req[i], course);
            //console.log(result);
            //if the course satisifies some requirement
            if (result["res"]){
                if (isAND){
                    // remove the element
                    //console.log(req);
                    req.splice(i, 1);
                    //console.log(req);
                    // if there still requirements (e.g. list is another AND)
                    if (result["list"].length > 0){
                        //add reaming requirements to req
                        req.splice(i, 0, result["list"]);
                    }
                    return {"res":true, "list":req};
                }
                else{
                    //remove the element
                    req.slice(i, 1);
                    //if there still requirements (e.g. list is another AND)
                    if (result["list"].length > 0){
                        // add reaming requirements to req
                        
                        req.splice(i, 0, result["list"]);
                        return {"res":true, "list":req};
                    }
                    else{
                        orCount--;
                        //if we have satisfied all req for an OR
                        if (orCount == 0)
                            return {"res":true, "list":[]};
                        // else we still have to select elements from this list
                        req[0] = "%or?" + num2word(orCount);
                        req.splice(i, 0);
                        return {"res":true, "list":req};
                    }
                }
            }
            else
                continue;
        }
    }
    //If none of the req matched, return false
    return {"res":false, "list":req};
}

//====================
//Helper functions
//====================

function word2num(word){
    if (word == "one")
        return 1;
    else if (word == "two")
        return 2;
    else if (word == "three")
        return 3;
    else if (word == "four")
        return 4;
    else
        return 5;
}

function num2word(num){
    if (num == 1)
        return "one";
    else if (num == 2)
        return "two";
    else if (num == 3)
        return "three";
    else if (num == 4)
        return "four";
    else
        return "five";
}

// Helper function that "flattens" a req list
// Returns a list of every course in the req list
function flattenReq(req){  

    response = [];

    if(req.length == 0)
        return response;

    req.forEach(function(r){

        if (typeof(r) == "string"){
            //we can skip keywords, as they are not classes
            if (r == "%and" || r.substring(0,3) == "%or")
                return;
            else
                response.push(r);
        }
        else
            response = response.concat(flattenReq(r));
    });

    return response;

}
