import scrape
import evalReq
import parser
import db

def main():
   
    #scrape.reset()

    #initialize the database
    #db.open_connection("../../config")
    #db.delete_db()
    #db.init_db()
    #db.close_connection()

    #scrape.scrapeCourses()

    scrape.scrapeLectureList("20W")
    scrape.scrapeLectureList("20S")
    #scrape.scrapeLectureList("20F")
    
    #scrape.updateLecture()
    #scrape.buildDict()
    #print(evalReq.chkCOMSCI(['COM+SCI 1','COM+SCI 31','COM+SCI 32','COM+SCI 33','COM+SCI 35L', 'COM+SCI M51A', 'MATH 32A']))
    
    #print(evalReq.checkReq("CS", ['PHYSICS 1A', 'PHYSICS 1B','MATH 32A','MATH 32B','MATH 61']))

    """
    
    #test="two courses in FieldI, or course 20 and one course in FieldI"
    test=[]
    
    test.append("COM+SCI 100")
    #test.append("COM+SCI 100 or COM+SCI 200")
    #test.append("COM+SCI 100 and COM+SCI 200")
    test.append("one course from COM+SCI 100, COM+SCI 200, COM+SCI 300, or COM+SCI 400")
    #test.append("COM+SCI 100 or COM+SCI 200 or COM+SCI 300 or COM+SCI 400")
    test.append("COM+SCI 100 and COM+SCI 101, or COM+SCI 400")
    #test.append("two courses in FieldI")
    #test.append("two courses in FieldI, or course 20 and one course in FieldI")
    #test.append("COM+SCI 100 foo")
    #test.append("courses 120A, 120B, 120C, or one year of introductory Middle Egyptian")
    #test.append("course 10 or 10W or 20 or comparable knowledge in Asian American studies")
    test.append("three courses from COM+SCI 111 through COM+SCI CM187")
    #test.append("two courses from 10 (or 10W), 20, and 30 (or 30W) and one course from 104A through M108, 187A, or 191A")
    test.append("Mathematics 3B or 32A, Physics 1B or 5B or 5C or 6B, with grades of C or better")
    #test.append("course 32 or Program in Computing 10C with grade of C- or better, and one course from Biostatistics 100A, Civil Engineering 110, Electrical Engineering 131A, Mathematics 170A, or Statistics 100A")
    #test.append("one course from 31, Civil Engineering M20, Mechanical and Aerospace Engineering M20, or Program in Computing 10A, and Mathematics 3B or 31B")
    #test.append("courses 143 or 180 or equivalent")
    #test.append("course 181 or compatible background")
    
    
    #test.append("course 192A or Life Sciences 192A (may be taken concurrently), and at least one term of prior experience in same course in which collaborative learning theory is practiced and refined under supervision of instructors")
    #test.append("course 181 or compatible background")
   
    #print(scrape.dept_dict)

    for i in test:
        print(i)
        s = parser.parseReq(i, "COM+SCI", scrape.dept_dict)
        print(s)
        #e = evalReq.simplifyReq(s)
        #print(e)
        #f = evalReq.flattenReq(e)
        #print(f)
        #print(evalReq.chkReq(s, "COM+SCI 100"))
        #print(s)
        #print(evalReq.chkReq(s, "COM+SCI 101"))
        #print(parser.list2Json(s))
        print("--------------------")
    
    
    """



    """
    
    #test="two courses in FieldI, or course 20 and one course in FieldI"
    test=[]
    #test.append(("courses 32, 33, 35L", "COM+SCI"))
    #test.append(("courses 120A, 120B, 120C, or one year of introductory Middle Egyptian", "COM+SCI"))
    #test.append(("course 10 or 10W or 20 or comparable knowledge in Asian American studies", "COM+SCI"))
    #test.append(("three courses from COM+SCI 100 through COM+SCI 400", "COM+SCI"))
    test.append(("Mathematics 3B or 32A, Physics 1B or 5B or 5C or 6B, with grades of C or better", "COM+SCI"))
    test.append(("course 32 or Program in Computing 10C with grade of C- or better, and one course from Biostatistics 100A, Civil Engineering 110, Electrical Engineering 131A, Mathematics 170A, or Statistics 100A", "COM+SCI"))

    for i in test:
        print(i[0])
        s = parser.parseReq(i[0], i[1], dept_dict)
        print(s)
        #print(parser.list2Json(s))
        print("--------------------")
    """
    

if __name__ =="__main__":
    main()
