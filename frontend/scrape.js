async function scrapeLectureInfo(term, id){

    url = "https://api.allorigins.win/get?url=";
    
    tmp_url="https://sa.ucla.edu/ro/Public/SOC/Results?t=";
    tmp_url+=term;
    tmp_url+="&sBy=classidnumber&id=";
    tmp_url+=id;
    tmp_url+="&btnIsInIndex=btn_inIndex";
    
    url+=encodeURIComponent(tmp_url);

    let res = await fetch(url);
    let data = await res.text();

    //console.log(data);

    return sLIhelper(data);

}

function sLIhelper(data){

    let dummy = document.createElement('html');
    dummy.innerHTML = JSON.parse(data)["contents"];

    let name = dummy.querySelectorAll(".sectionColumn .cls-section p a");

    let stat = dummy.querySelectorAll(".statusColumn p");

    let waitlist = dummy.querySelectorAll(".waitlistColumn p");

    //let day = dummy.querySelectorAll(".dayColumn p");

    let time = dummy.querySelectorAll(".timeColumn p");

    let loc = dummy.querySelectorAll(".locationColumn p");

    let inst = dummy.querySelectorAll(".instructorColumn");

    let lec = [];

    //console.log(name);

    for (let i = 1; i < name.length; i++){

        lec.push(formatStat(
            name[i-1].textContent,
            name[i].getAttribute("title"),
            stat[i].textContent,
            waitlist[i].textContent,
            time[i*2-1].textContent,
            time[i*2].textContent,
            loc[i].textContent,
            inst[i].textContent
        ));
    }

    //console.log(JSON.stringify(lec)); 

    return lec;

    //return JSON.stringify(lec);
}

function padNonChar(str){

    //console.log(str);

    if (typeof(str) != "string")
        return "";

    if (str.length <= 2)
        return "";

    let s = 0;
    let e = str.length-1;

    while(!(str[s].charCodeAt(0) >= 65 && str[s].charCodeAt(0) <= 122) && s < e)
        s++;
    while(  !(str[e].charCodeAt(0) >= 65 && str[e].charCodeAt(0) <= 122) && 
            !(str[e].charCodeAt(0) >= 48 && str[e].charCodeAt(0) <= 57) && 
            e > s)
        e--;
            

    return str.substring(s,e+1);

}

function formatStat(name, id, stat, waitlist, day, time, loc, inst){

    //console.log(time);

    let info = {};

    //=====name=====
    info["sect"] = name;

    //=====id=======
    //let id_begin=id.find("for") + 4
    info["course_id"] = "n/a";

    let s={};
  
    //=====stat======
    //if the class is active
    if (stat.indexOf("Open") != -1){
        s["status"] = "Open";

        let of = stat.indexOf("of");
        let end = stat.find("Enrolled");
        s["taken"] = stat.substring(4, of-1);
        s["cap"] = stat.substring(of+3, end-1);

    }
    //waitlist
    else if (stat.indexOf("Waitlist") != -1){
        s["status"] = "Waitlist";

        let par = stat.indexOf("(");
        let end = stat.indexOf(")");
        s["taken"] = stat.substring(par+1, end);
        s["cap"] = s["taken"];

    }
    //Closed
    else if (stat.indexOf("Closed") != -1){
        s["status"] = "Closed";

        let par = stat.indexOf("(");
        let end = stat.indexOf(")");
        s["taken"] = stat.substring(par+1, end);
        s["cap"] = s["taken"];
    }
    //Closed by Dept
    else {
        s["status"] = "Closed by Dept";

        s["taken"] = "n/a";
        s["cap"] = s["taken"];
    }

    //=====waitlist=====
    let w={}
    //if there is no waitlist
    if (waitlist.indexOf("No") != -1){
        w["status"] = "None";
        w["taken"] = "n/a";
        w["cap"] = "n/a";
    }
    //if the waitlist is full
    else if (waitlist.indexOf("Full") != -1){
        w["status"] = "Full";
        let par = waitlist.indexOf("(");
        let end = waitlist.indexOf(")");
        w["taken"] = waitlist.substring(par+1, end); 
        w["cap"] = waitlist.substring(par+1, end); 
    }
    //id waitlist is open
    else{
        w["status"] = "Open";
        let of = waitlist.indexOf("of");
        let end = waitlist.indexOf("Taken");
        w["taken"] = waitlist.substring(0,of-1); 
        w["cap"] = waitlist.substring(of+2, end-1);
    }
    
    s["waitlist"] = w;
    
    info["enrollment"] = s;

    info["days"] = day;

    //=====time======
    let t = {};

    //console.log(time);

    //if time is listed as "varies"
    if (time.indexOf("aries") != -1){
        t["start"] = "Varies";
        t["end"] = "Varies";
    }
    //if day was "Not scheduled"
    else if (day.indexOf("Not scheduled") != -1){
        t["start"] = "n/a";
        t["end"] = "n/a";
    }
    //otherwise, process time as usual
    else{
        let time_split = time.split("-");

        t["start"] = time_split[0];
        t["end"] = time_split[1];
    }

    info["time"] = t;

    //=====location======
    if (loc.length == 0){
        loc = "n/a";
    }

    info["location"] = padNonChar(loc);

    //=====instructor======
    info["instructor"] = inst;

    //console.log(info);
    return info;

}


//This function will scrape a lecture given its course id

async function scrapeLectureId(term, url){

    //https://sa.ucla.edu/ro/Public/SOC/Results?t=20WsBy=units&meet_units=4.0&subj=COM+SCI&crsCatlg=M51A+-+Logic+Design+of+Digital+Systems&catlg=0051A+M

    url = url.split("@");
    url = url[0] + term + url[1];
    
    //request the webpage
    let res = await fetch(url);
    let data = await res.text();

    let dummy = document.createElement("html");
    dummy.innerHTML= JSON.parse(data)["contents"];

    lec_table = querySelectorAll(".class-not-checked");
    ids=[];
    
    lec_table.forEach(lec => {
        let lec_id = lec.id;
        let id_end = lec_id.search("_");

        lec_id = lec_id.substring([0,id_end]);
        ids.push(lec_id);
    });
        
    return ids;
}