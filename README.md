![](atlas-min.png)

# About
Currently, Bruins often have a hard time figuring out what classes they should take for upcoming quarters. This is largely because information about major requirements are very dispersed and disorganized. More specifically, to find all information regarding major requirements, students need to visit...

* UCLA course description homepage to browse details of offered courses.
* UCLA admission office homepage to determine what major requirements are.
* MyUCLA (student web portal) to determine what courses are offered for the upcoming quarter.
* BruinWalk.com to check ratings of professors.

The goal of Atlas is to provide a centralized web portal that aggregates information in the above websites
into a simple, intuitive interface. 
  
# For Developers
Following sections will provide an overview of Atlas's system

## Components
Atlas has three main components, each with its own sub-repository on GitHub

### atlas-frontend

The frontend is built using React. It is also responsible for running `atlas-audit.js`, which is the algorithm used to audit major progress. When running an audit, the frontend will retrieve major requirement information from `atlas-majors`.

### atlas-backend

The main role of the backend is to scrape major requirement information, store them in a database, and generate files for `atlas-major`. Currently considering migrating to AWS. 

### atlas-majors

`atlas-majors` is the repository that stores major requirement information. Currently considering hosting at the same endpoint as the frontend to prevent CORS. 

## Usage
:fire:**Warning:**:fire: Atlas is currently in early prototype phase. Functionality is extremely limited and unstable. Various features and specs are subject to change frequently.

#### Step 1:
Navigate to `atlas-frontend/frontend`

#### Step 2:
Execute `npm run start`

#### Step 3:
In the textbox located at the top, type in the courses you have completed so far. Currently, each course needs to be formatted as `<course's departent code> <course number>`. A department code needs to be in all caps, and use `+` in place of a space. For example, the course *Computer Science 111* will be written as `COM+SCI 111`. 

If there are multiple courses, they need to be separated by a comma, with no whitespace in between the comma and the course names. For example, if you have taken CS111 and CS118, you would write `COM+SCI 111,COM+SCI 118`.

#### Step 4:
Hit the submit button. 

