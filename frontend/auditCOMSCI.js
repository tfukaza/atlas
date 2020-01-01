 function auditBuild(option){
    
    //init agents
    let agents= [];
    //non-leaf agent
    let root_agents= [];
    //rules
    let rules = [];
    //Agents at the beginning of the array are leafs, while rear agents are non-leafs

    let r = rules;
    let a = agents;
    let r_a = root_agents;

    // Preparation for the Major
    // Computer Science 1, 31, 32, 33, 35L
    a.push(new Agent(  
        "prep-1",
        ['%and', 'COM+SCI 1','COM+SCI 31','COM+SCI 32','COM+SCI 33','COM+SCI 35L', 'COM+SCI M51A']
        )
    );
    a[a.length-1].chk = check_req.bind(a[a.length-1]);
    a[a.length-1].upd = update_leaf_1.bind(a[a.length-1], 6, -1);

    // Mathematics 31A, 31B, 32A, 32B, 33A, 33B, 61
    a.push(new Agent(
        "prep-2",  
        ['%and', 'MATH 31A','MATH 31B','MATH 32A','MATH 32B','MATH 33A','MATH 33B','MATH 61']
    ));
    a[a.length-1].chk = check_req.bind(a[a.length-1]);
    a[a.length-1].upd = update_leaf_1.bind(a[a.length-1], 7, -1);

    // Physics 1A, 1B, 1C, and 4AL or 4BL.
    a.push(new Agent(
        "prep-3",  
        ['%and', 'PHYSICS 1A','PHYSICS 1B','PHYSICS 1C', ['%or?one', 'PHYSICS 4AL','PHYSICS 4BL']]
    ));
    a[a.length-1].chk = check_req.bind(a[a.length-1]);
    a[a.length-1].upd = update_leaf_1.bind(a[a.length-1], 4, -1);

    // Computer Science 111, 118, 131, M151B, M152A, 180, 181
    a.push(new Agent(
        "major-1",  
        ['%and', 'COM+SCI 111','COM+SCI 118','COM+SCI 131','COM+SCI M151B','COM+SCI M152A', 'COM+SCI 180', 'COM+SCI 181']
    ));
    a[a.length-1].chk = check_req.bind(a[a.length-1]);
    a[a.length-1].upd = update_leaf_1.bind(a[a.length-1], 7, -1);

    // one course from Civil and Environmental Engineering 110, Electrical and Computer Engineering 131A, Mathematics 170A, or Statistics 100A
    a.push(new Agent(
        "major-2",  
        ['%or?one', 'C&EE 110','EC+ENGR 131A','MATH 170A','STATS 100A']
    ));
    a[a.length-1].chk = check_req.bind(a[a.length-1]);
    a[a.length-1].upd = update_leaf_1.bind(a[a.length-1], 1, -1);

    //one capstone software engineering or design course from Computer Science 130 or 152B
    a.push(new Agent(
        "major-3",  
        ['%or?one', 'COM+SCI 130', 'COM+SCI 152B']
    ));
    a[a.length-1].chk = check_req.bind(a[a.length-1]);
    a[a.length-1].upd = update_leaf_1.bind(a[a.length-1], 1, -1);


    //a minimum of 20 units and five elective courses selected from Computer Science 111 through CM187
    a.push(new Agent(
        "major-4",  
        ['%and', 'COM+SCI 111', /*'%through',*/ 'COM+SCI CM187']
    ));
    a[a.length-1].chk = check_req.bind(a[a.length-1]);
    a[a.length-1].upd = update_leaf_1.bind(a[a.length-1], 5, -1);

    //12 units of technical breadth courses selected from an approved list available in the Office of Academic and Student Affairs.
    if (option["tba"] == "BIOENGR"){
        a.push(new Agent(
            "major-6",  
            ['%and', 'BIOENGR 100', /*'%through',*/ '187']
        ));
        a[a.length-1].chk = check_req.bind(a[a.length-1]);
        a[a.length-1].upd = update_leaf_1.bind(a[a.length-1], 1, -1);
    }
    else if (option["tba"] == "CH+ENGR"){
        a.push(new Agent(
            "major-6",  
            ['%and', 'CH+ENGR 100', '%through', 'CH+ENGR187']
        ));
        a[a.length-1].chk = check_req.bind(a[a.length-1]);
        a[a.length-1].upd = update_leaf_1.bind(a[a.length-1], 1, -1);
    }
    else if (option["tba"] == "C&EE"){
        a.push(new Agent(
            "major-6",  
            ['%and', 'C&EE 100', '%through', 'C&EE 187', 'CHEM 20B']
        ));
        a[a.length-1].chk = check_req.bind(a[a.length-1]);
        a[a.length-1].upd = update_leaf_1.bind(a[a.length-1], 1, -1);

        //One of the three courses can be substituted by CHEM 20B if not used to satisfy other degree requirements and additional two courses that are applied to technical breadth area are upper division.
        r.push(new Rule(
            "subset-1",
            agents
        ));
        r[r.length-1].chk=subset_restriction.bind(r[r.length-1],['CHEM 20B']);
    
    }
    else{
        a.push(new Agent(
            "major-6",  
            ['%and',  'COM+SCI 31', 'COM+SCI 32', 'COM+SCI 33', 'MATH 61', 'COM+SCI 102', '%through', '187']
        ));
        a[a.length-1].chk = check_req.bind(a[a.length-1]);
        a[a.length-1].upd = update_leaf_1.bind(a[a.length-1], 3, -1);
    }


    //

    // minimum of 12 units and three science and technology courses 
    //(not used to satisfy other requirements)
    // that may include 12 units of upper-division computer science courses
    // or 12 units of courses selected from an approved list available in the Office of Academic and Student Affairs;
    
    //Option 1: Additional CS Electives
    if (option["sci-tech"] == "1"){
        a.push(new Agent(
            "major-5",  
            ['%and', 'COM+SCI 100', /*'%through',*/ 'COM+SCI 199']
        ));
        a[a.length-1].chk = check_req.bind(a[a.length-1]);
        a[a.length-1].upd = update_leaf_1.bind(a[a.length-1], 3, -1);
    }

    //Option 2: Additional Courses from your Declared Tech Breadth Requirement
    else if (option["sci-tech"] == "2"){

        if (option["tba"] == "BIOENGR"){
            a.push(new Agent(
                "major-6",  
                ['%and', 'BIOENGR 100', /*'%through',*/ '187']
            ));
            a[a.length-1].chk = check_req.bind(a[a.length-1]);
            a[a.length-1].upd = update_leaf_1.bind(a[a.length-1], 1, -1);
        }
        else if (option["tba"] == "CH+ENGR"){
            a.push(new Agent(
                "major-6",  
                ['%and', 'CH+ENGR 100', '%through', 'CH+ENGR187']
            ));
            a[a.length-1].chk = check_req.bind(a[a.length-1]);
            a[a.length-1].upd = update_leaf_1.bind(a[a.length-1], 1, -1);
        }
        else if (option["tba"] == "C&EE"){
            a.push(new Agent(
                "major-6",  
                ['%and', 'C&EE 100', '%through', 'C&EE 187', 'CHEM 20B']
            ));
            a[a.length-1].chk = check_req.bind(a[a.length-1]);
            a[a.length-1].upd = update_leaf_1.bind(a[a.length-1], 1, -1);
    
            //One of the three courses can be substituted by CHEM 20B if not used to satisfy other degree requirements and additional two courses that are applied to technical breadth area are upper division.
            r.push(new Rule(
                "subset-1",
                agents
            ));
            r[r.length-1].chk=subset_restriction.bind(r[r.length-1],['CHEM 20B']);
        
        }
        else{
            a.push(new Agent(
                "major-6",  
                ['%and',  'COM+SCI 31', 'COM+SCI 32', 'COM+SCI 33', 'MATH 61', 'COM+SCI 102', '%through', '187']
            ));
            a[a.length-1].chk = check_req.bind(a[a.length-1]);
            a[a.length-1].upd = update_leaf_1.bind(a[a.length-1], 3, -1);
        }
    }

    //Option 3: Option 3: Courses from one of these listed Departments
    else if (option["sci-tech"] == "3"){
        if (option["sci-tech-dept"] == "BIOENGR"){
            a.push(new Agent(
                "major-6",  
                ['%and', 'BIOENGR 100', /*'%through',*/ '187']
            ));
            a[a.length-1].chk = check_req.bind(a[a.length-1]);
            a[a.length-1].upd = update_leaf_1.bind(a[a.length-1], 1, -1);
        }
        else if (option["sci-tech-dept"] == "CH+ENGR"){
            a.push(new Agent(
                "major-6",  
                ['%and', 'CH+ENGR 100', '%through', 'CH+ENGR187']
            ));
            a[a.length-1].chk = check_req.bind(a[a.length-1]);
            a[a.length-1].upd = update_leaf_1.bind(a[a.length-1], 1, -1);
        }
        else if (option["sci-tech-dept"] == "C&EE"){
            a.push(new Agent(
                "major-6",  
                ['%and', 'C&EE 100', '%through', 'C&EE 187', 'CHEM 20B']
            ));
            a[a.length-1].chk = check_req.bind(a[a.length-1]);
            a[a.length-1].upd = update_leaf_1.bind(a[a.length-1], 1, -1);
    
            //One of the three courses can be substituted by CHEM 20B if not used to satisfy other degree requirements and additional two courses that are applied to technical breadth area are upper division.
            r.push(new Rule(
                "subset-1",
                agents
            ));
            r[r.length-1].chk=subset_restriction.bind(r[r.length-1],['CHEM 20B']);
        
        }
        else{
            a.push(new Agent(
                "major-6",  
                ['%and',  'COM+SCI 31', 'COM+SCI 32', 'COM+SCI 33', 'MATH 61', 'COM+SCI 102', '%through', '187']
            ));
            a[a.length-1].chk = check_req.bind(a[a.length-1]);
            a[a.length-1].upd = update_leaf_1.bind(a[a.length-1], 3, -1);
        }
    }

    //Option 4: Option 4: Life Science Prep
    else if (option["sci-tech"] == "4"){
        a.push(new Agent(
            "major-5",  
            ['%and', 'COM+SCI 100', '%through', 'COM+SCI 199']
        ));
        a[a.length-1].chk = check_req.bind(a[a.length-1]);
        a[a.length-1].upd = update_leaf_1.bind(a[a.length-1], 3, -1);
    }
    else{
        console.log("Error");
    }




    /*
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

    let a = new RootAgent(
        "major-1T2",  
        agents
    );
    a.upd = update_1.bind(a,1,2);
    root_agents.push(a);
    */

    r.push(new Rule(
        "subset-1",
        agents
    ));
    r[r.length-1].chk=subset_restriction.bind(r[r.length-1],['C&EE 110', 'EC+ENGR 131A', 'ENGR 116', 'MATH 170A', 'MATH 170E', 'STATS 100A']);

    let audit = {};
    audit["agents"] = agents;
    audit["root_agents"] = root_agents;
    audit["rules"] = rules;

    return audit;

 }