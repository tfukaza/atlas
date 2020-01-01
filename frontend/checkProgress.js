
function chkProgress(){

    var courses = document.getElementById("list").value;
    courses = parseCourse(courses);

    let res = audit_run(courses, {"sci-tech":"1", "major-5": "NANO"});
    console.log(res);
    //TODO
    updateDOM(res);
}


// TODO
// Function that takes the result of chkReq, and updates DOM accordingly
// DOM is assumed to have been set up already. 
function updateDOM(res){

    res["req"].forEach(function(r){

        var id = r["name"];

        if (id[0] == "*"){
            //console.log(padNonChar(id));
            var q = document.getElementsByClassName(padNonChar(id));
            //console.log(q);
            q[0].classList.add("done");
        }

    });
    
}

// TODO
// Function that takes the result of chkReq, fetches updated info for each course,
//and enumerates the DOM
function updateLec(res){
    res["req"].forEach(function(r){

        var courses = r["req"];

        info = [];

        courses.forEach(function(c){
            scrapeLectureId("20W", urls[c]);
        });

    });
}

//Helper function to parse the list of comma-seperated course names into a list

function parseCourse(c_list){

    let courses = [];

    s_list = c_list.split(",");

    return s_list;
    
}


