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

## Usage
:fire:**Warning:**:fire: Atlas is currently in early prototype phase. Functionality is extremely limited and unstable. Various features and specs are subject to change frequently.

#### Step 1:
Open `backend/index.html` 

#### Step 2:
In the textbox located at the top, type in the courses you have completed so far. Currently, each course needs to be formatted as `<course's departent code> <course number>`. A department code needs to be in all caps, and use `+` in place of a space. For example, the course *Computer Science 111* will be written as `COM+SCI 111`. 

If there are multiple courses, they need to be seperated by a comma, with no whitespace in between the comma and the course names. For example, if you have taken CS111 and CS118, you would write `COM+SCI 111,COM+SCI 118`.

#### Step 3:
Hit the submit button. 

