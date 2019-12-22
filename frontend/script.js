
class Agent{

    constructor(req, evalF, desc, unit, course, upd){

        this.req = req;          // list of required courses/agents
        this.taken = [];         // list of completed courses
        this.evalF = evalF;        // function to evaluate requirement (leaf only)

        this.done = false;       // if req is met or not
        this.unit = 0;           // number of taken units  
        this.course = 0;         // number of taken courses
        this.req_unit = unit;    // number of required units  
        this.req_course = course;// number of required courses
        this.desc = desc;

        this.upd = upd;          // function to update above status
    }

    evaluate(c){
        return this.evalF(c);
    }

    update(){
        return this.upd()
    }
}

class RootAgent {

    constructor(desc, agents, s, e, upd){

        this.agents = agents;    //list of leaf agents
        this.s = s;
        this.e = e;

        this.done = false;       // if req is met or not
        this.upd = upd;          // function to update status
        this.desc = desc;
    }

    update(){
        return this.upd()
    }

}


function chkProgress(){

    var courses = document.getElementById("list").value;
    //console.log(parseCourse(courses));
    //var chk = ['%and', 'CS180', ['%or-one', 'CS 120', 'CS 130']];
    //var chk = ['PHYSICS 4AL','PHYSICS 1B', 'MATH 32A','MATH 33A','MATH 31B'];
    var chk = parseCourse(courses);
    //var chk = ['%and', 'PHYSICS 1A','PHYSICS 1B','PHYSICS 1C', ['%and', 'COM+SCI 12', 'COM+SCI 14'], ['%or?one', 'PHYSICS 4AL','PHYSICS 4BL', 'PHYSICS 4CL']]
    console.log(chkCOMSCI(chk));
    //console.log(chkReq(chk, 'COM+SCI 14'));

}

//Helper function to parse the list of comma-seperated course names into a list

function parseCourse(c_list){

    let courses = [];

    s_list = c_list.split(",");

    return s_list;
    
}

//Don't forget to use bind
function chkAllReq(c){
    //console.log(this);
    result = chkReq(this.req, c)
    if (result["res"]){
        this.req = result["list"];
        this.course = this.course + 1;
        this.taken.push(c); 
        return true;
    }
    return false;
}

function updateLeaf_1(){
    if (this.course >= this.req_course){
        this.done = true;
    }
    //console.log(this);
}


function chkCOMSCI(courses){

    //init agents
    let agents= [];
    //Agents at the beginning of the array are leafs, while rear agents are non-leafs

    // Preparation for the Major
    // Computer Science 1, 31, 32, 33, 35L
    
    agents.push(
        new Agent(  ['%and', 'COM+SCI 1','COM+SCI 31','COM+SCI 32','COM+SCI 33','COM+SCI 35L', 'COM+SCI M51A'],
                chkAllReq,
                "Prep-1",
                -1,
                3,
                updateLeaf_1
            )
    );
    agents[agents.length-1].evalF.bind(agents[agents.length-1]);
    agents[agents.length-1].upd.bind(agents[agents.length-1]);

    // Mathematics 31A, 31B, 32A, 32B, 33A, 33B, 61
    agents.push(
        new Agent(  ['%and', 'MATH 31A','MATH 31B','MATH 32A','MATH 32B','MATH 33A','MATH 33B','MATH 61'],
                chkAllReq,
                "Prep-2",
                -1,
                3,
                updateLeaf_1
            )
    );
    agents[agents.length-1].evalF.bind(agents[agents.length-1]);
    agents[agents.length-1].upd.bind(agents[agents.length-1]);

    // Physics 1A, 1B, 1C, and 4AL or 4BL.
    agents.push(
        new Agent(  ['%and', 'PHYSICS 1A','PHYSICS 1B','PHYSICS 1C', ['%or?one', 'PHYSICS 4AL','PHYSICS 4BL', 'PHYSICS 4CL']],
                chkAllReq,
                "Prep-2",
                -1,
                3,
                updateLeaf_1
            )
    );
    agents[agents.length-1].evalF.bind(agents[agents.length-1]);
    agents[agents.length-1].upd.bind(agents[agents.length-1]);

    //non-leaf agent
    let root_agents= [];

    function update_1(){

        let isDone = false
        let netCourse = 0

        for (let a = this.s; a <= this.e; a++){
            if (this.agents[a].done){
                isDone = true;
            }
            netCourse += this.agents[a].course;
        }

        if (isDone && netCourse >= 4){
            this.done = true;
        }

    }

    root_agents.push(
        new RootAgent(  
            "major-2",
            agents,
            1,
            2,
            update_1
            )
    );

    root_agents[root_agents.length-1].upd.bind(root_agents[root_agents.length-1]);


    //This is an object, not an array
    let response = {};
    response["req"] = [];

    //for each course...
    for (let c = 0; c < courses.length; c++){

        //check each requirement and see which requirement it fulfills
        for (let a = 0; a < agents.length; a++){ 

            //if ( this requirement is already fulfilled, move on to the next requirement
            if (agents[a].done){
                continue;
            }
            
            // See if this course satisifies a requirement
            let res = agents[a].evaluate(courses[c]);
            // If it does, move onto the next course
            if (res){
                continue;
            }
        }
    }
    // At this point agent.req in each agent will contain the remaining course
    // that has to be taken. 

    //Call update on all agents
    agents.forEach(a => a.update());
    root_agents.forEach(a => a.update());

    console.log(agents);

    // TODO inspect edge cases manually
    // Credit is not allowed for both Computer Science 170A and Electrical and Computer Engineering 133A unless at least one of them is applied as part of the science and technology requirement or as part of the technical breadth area. 
    
    // inpect all leaf agents, and for all unfinshed req, record the courses that can be taken
    for (let a = 0; a < agents.length; a++){
        ag = agents[a]
        tmp = {}
        //if this course has been completed
        if (ag.done){
            tmp["desc"] = "*" + ag.desc; //add a star to indicate completion
            tmp["req"] = []; 
        }
        else{
            tmp["desc"] = ag.desc;
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
            tmp["desc"] = "*" + a.desc; //add a star to indicate completion
            tmp["req"] = []; 
            //mark all child agents as done as well
            for (let i = a.s; i <= a.e; i++){
                response["req"][i]["desc"] = "*" +  response["req"][i]["desc"];
                response["req"][i]["req"] = [];
            }
        }
        else{
            tmp["desc"] = a.desc;
            tmp["req"] = [];
        }

        tmp["taken"] = [];

        response["req"].push(tmp);

    });

    return response;
}


// A helper function 
// Given a list of requirements and a course...
// If the course satisfies some requirement, returns true and a new req list
// If not, returns false with the same list as before

function chkReq(req, course){

    //console.log("inspecting" + req);

    if (typeof(req) == "string"){
        console.log("isstring");
        if (req.localeCompare(course) == 0)
            return {"res":true, "list":[]};
        else
            return {"res":false, "list":req};
    }

    

    // if the list is empty, all req has been met
    if (req.length == 0)
        return {"res":true, "list":[]};
    
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
    let isDemolish = false;
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
                    console.log(orCount);
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
