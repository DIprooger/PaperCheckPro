# Diploma project

## General description of the project
**Project name**: to come up with a name.

Project's point: Develop a Django-based web application 
for checking school papers with grading and description of errors.

## **Technical Stack** ????
* **Backend**: Django (**Python**)                                                                                      
* **Frontend**: (if needed): Python, HTML(Django templates), CSS(if needed)                                             
* **Database**: PostgreSQL \ MySQL                                                                                      
* **API**: **Django REST framework**                                                                                    
* **Additional tools**: **Docker** (for application containerization), **Nginx**                                        

## **Functional Requirements** 
**Functionality**
* Creating a SuperUser
* The SuperUser can add a list of students
* The SuperUser can add work to be printed to the students
* SuperUser - add works to be checked
* SuperUser Comment on some errors or add a solution
* Users are students. Access their profile to view checked and graded works


### **Models**
* **Work**: id, name_work, name_student, date, file_work, evaluation, 
created_at, updated_at, deleted_at, deleted                                                                   
* **SuperUser**: id, username, email, password, class, 
created_at, updated_at, deleted_at, deleted
* **User**: id, username, email, password, class, work, created_at,                                                         
updated_at, deleted_at, deleted             


