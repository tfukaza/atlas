# Atlas
Atlas is a web portal aimed to provide an easy way for students at UCLA (University of California, Los Angeles) to browse course and major information. 

## About
Currently, Bruins often have a hard time figureing out what classes they should take for upcoming quarters. Part of the reason is because the resources neccesary to decide what classes to take are extremely disorganized and decentralized. More specifically, students need to visit...

* UCLA course description homepage to browse details of offered courses.
* UCLA admission office homepage to determine what major requirements are.
* MyUCLA (student web portal) to determine what courses are offered for the upcoming quarter.
* BruinWalk.com to check ratings of professors.

The goal of Atlas is to provide a centralized web portal that provides all neccesary information to help students plan their courses.
  
## Components
Atlas has two components, the frontend and the backend. As of 12/2019, Atlas is using a model that delegates most computing to client side in order to reduce operating cost of backend services.


### Frontend

The frontend is a web portal that provides all neccesary information. It uses Javascript to handle the majority of neccesary computation. Currently it is in prototype phase, and only supports CS and CSE majors. 

TODO (Prototype):

- [ ] Build basic web interface.
- [ ] Given a list of taken courses, be able to return what other courses have to be completed to finish major.
- [ ] For above courses, scrape for up-to-date descriptions, enrollment status, etc.
- [ ] (?) Create a class planner interface to schedule courses (Similar to G Calender).

### Backend

Frankly, the backend code that exists as of 12/2019 is a relic of an earlier prototype that assumed a service model that deligated most of the computing to the server side via public APIs. Its current purpose is mainly to aid the development of frontend code by providing functions to efficiently accumulate, organize and browse courses offered by UCLA. 

The program is written in Python 3, which scrapes neccesarily data, parses them, stores them in a SQL database (PostgreSQL), and uses Flask to provide a public API.  

TODO (Prototype):

- [ ] Build a parser to scrape and store course information in an SQL database.
- [ ] Provide functions to easily retreive data neccesary to develop frontend code
- [ ] Extend scraper to collect information regarding GE courses

