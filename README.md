# Atlas (temporary name)
Atlas is a system curently under development, aimed to provide an easy way for students at 
UCLA (University of California, Los Angeles) to browse course and major information. 

## The Problem
Currently, when UCLA students want to sign up for a class,
they need to cross-examine a monumental amount of documentation, course lists, 
and sample schedules to decide what classes they have taken, what class they can take, and what class they want to take. 
Probably the easiest way to do this is the DAR system, but even that is often difficult to navigate.

## Solution
The ultimate goal of Atlas is to provide a web portal where students can easily browse and search courses and major requirements. 

## Phases
Currently the Atlas is in early prototype phase - in other words, still testing the basic functionalities neccesary for the system to work. 
The prototype development is divided into the following phases.

### Phase 1
Develop a web scraper to accumate various information for each course

- [ ] Course...
   - [x] Number
   - [x] Name
   - [ ] ID
   - [ ] grade level (lower/upper/grad)
- [x] Awarded units
- [x] Description
- [x] Type (lecture/lab/seminar/tutorial)
- [x] Requisites
- [ ] Schedule
   - [ ] Currently offered lectures
   - [ ] Currently offered discussion sections
   - [ ] Enrollment status 
 
### Phase 2
Accumulate a database of major requirements. This part will most likely be done manually.

### Phase 3
Store the collected data in an SQL database

### Phase 4
Build a web application to allow browsing/searching of classes.

## The Parser
The core of the web scraper in Phase 1 is a parser that takes a list of course prerequisites written in English and generates a 
Python list that expresses the requisite as equivilence classes.

Analysis shows that the prerequisite desciptions are written with the following grammar, expressed Backus-Naur:

```
<expression> ::=  <eq_class> | 
                  <eq_class>”, and” <expression> |
                  <eq_class>”,” <expression> |
                  <eq_class> “and” <expression> |

<eq_class> ::=    <course> | 
                  <course>”, or” <expression> | 
                  <course> “or” <eq_class> |
                  <number> <level> <department> “courses not in” <selection> | 
                  <number> <level> <department> “courses in” <selection> | 
                  <number> “courses in” <selection> | 
                  <number> “course in” <Field> |
                  <number> “course from” <or list>  

<or list> ::=     <course>”, or” <course> | 
                  <course>”,” <or list>

<selection> ::=   <Field>
                  <number> “to” <number> “series”

<course> ::=      <course_id> “with a grade of” <grade> “or better”
                  <course_id> “, or equivalent”
                  <course_id>

<course_id>:: =   “course” <course_num> |
                  “courses” <course_num> |
                  <department> <course_num> |
                  <course_num> 

```

Needless to say, the parser should implement this grammar. 




