##############################
# This excutable wraps other modules to provide a CLI tool
# to perform varios operations 
##############################

import db
import scrape

# =========================
# The function takes a range of terms and a course,
# and returns a list of offered lecture (course) id's for each term, if any
# ========================= 

def getIds(terms=["20W"], course):

    #seperate courses 
    tmp_s = course.split()
    dept = tmp_s[0]
    num = tmp_s[1]

    db.open_connection("../../db.config")

    c = db.get_db("SELECT dept, course_num, course_title, course_unit FROM courses WHERE dept='" + dept + "' AND course_num = '" + num + "');")
    c = c[0]

    result = {}

    for t in terms:
        r = scrape.scrapeLectureId(t, c[0], c[1], c[2], c[3])
        r[t] = r 
    
    print(result)
    return result


if __name__ =="__main__":
    getIds(terms=["20W", "20S"], "COM+SCI 32")
    
    

