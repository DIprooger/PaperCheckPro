# Diploma project

## General description of the project
**Project name**: to come up with a name.

Project's point: Web application for checking school papers.  
The application finds errors, they write them down. 
When the work is checked, a grade is given.

___

## **Technical Stack**
* **Platform**: Web application
* **Stack**: Django                                                                          
* **Frontend**: HTML, CSS                                           
* **Database**: PostgreSQL \ MySQL                                                                                      
* **API**: Django REST framework                                                                                    
* **Additional tools**: Docker   
* 
___

## **Technical requirements**                                                                        

The application must be deployed in a **Docker** container.                                                                        
Using **Django ORM** to interact with the database.   

___

## **Description of database models**
1) Model **UserStudent**:                                                                        
* `id`: Integer (Primary Key)                                                                        
* `email`: EmailField                                                                       
* `first_name`: CharField                                                                       
* `last_name`: CharField                                                                        
* `username`: CharField   
* `created_at`: DateTimeField
* `updated_at` : DateTimeField
* `deleted_at`: DateTimeField

2) Model **UserTeacher**: 
* `id`: Integer (Primary Key)                                                                        
* `email`: EmailField                                                                       
* `first_name`: CharField                                                                       
* `last_name`: CharField                                                                        
* `username`: CharField   
* `is_staff` : BooleanField
* `is_superuser` : BooleanField
* `is_verified` : BooleanField
* `is_active` : BooleanField
* `date_joined` : DateTimeField
* `last_login` : DateTimeField

3) Model **StudentWork**:                                                                        
* `id` : Integer (Primary Key)                                                                       
* `name_work`: CharField  
* `writing_date` : DateTimeField
* `student` : CharField (Foreign Key, UserStudent)
* `text_work`: TextField
* `assessment` : CharField
* `teacher` : CharField (Foreign Key, UserTeacher)
* `created_at`: DateTimeField
* `updated_at` : DateTimeField
* `deleted_at`: DateTimeField

---

## **Functional Requirements**                                                                               

**CRUD**:                                                                               

1) **UserStudent**                                                                               
* Create UserStudent (**POST**)                                                                               
* Get user by ID (**GET**)                                                                               
* Update user (**PUT/PATCH**)                                                                                
* Login (**POST**)                                                                               
* Logout (**POST**)                                                                               
* Change password (**POST**)                                                                               
* Reset password (**POST**)                                                                               

2) **UserTeacher**                                                                               
* Create UserTeacher (**POST**)                                                                               
* Get all UserStudent (**GET**)                                                                               
* Get UserStudent by ID (**GET**)
* Get UserTeacher by ID (**GET**)
* Update user (**PUT/PATCH**)                                                                               
* Delete user (**DELETE**) (soft delete **by UserStudent**, and hard delete **by admin**)                                                                               
* Login (**POST**)                                                                               
* Logout (**POST**)                                                                               
* Change password (**POST**)                                                                               
* Reset password (**POST**) 

3) **StudentWork**                                                                               
* Create StudentWork  (**POST**) (only creates **UserTeacher**)
* Get all StudentWork for UserStudent (**GET**)
* Get all the work students have created UserTeacher (**GET**)                                                                                 
* Get user's StudentWork by ID (**GET**)                                                                               
* Update StudentWork (**PUT/PATCH**)                                                                               
* Delete StudentWork (**DELETE**) (soft delete **by UserTeacher**, and hard delete **by admin**)                                                                               

**Filtering and sorting:**                                                                               
* Filtering StudentWork by execution writing_date, name_work, name student                                                                           

---

# **Permissions**                                                                               
1) **Admin**:                                                                               
* Managing all surveys                                                                                                                                                              
* Managing all users                                                                               
2) **UserStudent**:                                                                               
* Managing only himself profile                                                                               
* Have possibility to view your work
3) **UserTeacher**:                                                                               
* Managing only himself profile                                                                               
* Have possibility to view added works

---

# **User Requirements**                                                                                          
##### **UserStudent:**                                                                                          
1) **View StudentWork**                                                                                           
* **As a student, I want** to a complete list of my schoolwork.
* **As a student, I want** to receive detailed information about a particular paper.
* **As a student, want** to receive in my school work a description of my mistakes in my school work.                                                                                        

2) **Personal Profile**                                                                                          
* **As a user, I want** to be able to register and log in to save my details.                                                                                          
* **As a user, I want** to manage my profile (edit personal details and contact                                                                                           
information) to keep my information up to date.  
* 
##### **UserTeacher:**                                                                                          
1) **View StudentWork**   
* **As a teacher, I want** to add student work for checking and grading.
* **As a teacher, I want** to a complete list of my add schoolwork.
* **As a student, I want** to receive detailed information about a particular paper.
* **As a teacher, I want** to correct papers if they have been checked incorrectly.
* **As a teacher, I want** to add a description of the error if it was added by the application, 
or I think the description should be different.
* 
2) **Personal Profile**                                                                                          
* **As a user, I want to** be able to register and log in to save my details.                                                                                          
* **As a user, I want to** manage my profile (edit personal details and contact                                                                                           
information) to keep my information up to date.   
##### **Admin**                                                                                          

1) **Manage UserStudent**                                                                                          
* **As an administrator, I want to** add, edit and delete UserStudent information, 
to keep user information up to date.   
* **As an administrator, I want to** add, edit and delete UserStudent information,                                                                                     
to keep user information up to date. 
2) **Manage UserTeacher**                                                                                          
* **As an administrator, I want to** add, edit and delete UserTeacher information, 
to keep user information up to date.   
* **As an administrator, I want to** add, edit and delete UserTeacher information,                                                                                     
to keep user information up to date. 
3) **StudentWork Management**                                                                                          
* **As an administrator, I want to** add, edit and delete StudentWork information,
to keep student work information up to date. 
                                                                                        

---

## **Security**                                                                               

1) **Authentication**:                                                                                                                                                              
* Consider implementing an authentication system (e.g. **Token Authentication**).                                                                                                                                                              

2) **Data Validation**:                                                                                                                                                              
* Check for correct input data for all operations.                                                                               

---

## **Testing**                                                                               
1) **Unit tests**:                                                                               
* Writing tests to verify the functionality of all **CRUD** operations.                                                                               
2) **Integration tests**:                                                                               
* Testing the interaction of system components.                                                                               

---

## **Documentation**                                                                               

1) **README**:                                                                               
Project Description.                                                                               
List of technologies used to write the project.                                                                               
Instructions on how to install and run the application: commands one                                                                                                                                    
by one. How to run the project.                                                                                                                                     
2) **API documentation**:                                                                               
Description of endpoints, request and response formats. Examples of                                                                                                                                     
data that must be passed to process requests.                                                                                                                                       

---

### **Rules for working with **Git** for thesis writing and development. Branch organization**                                                                               
`One task - one branch`: You should create a separate branch from the                                                                                
main for each new task or functionality.                                                                                
The name of the branch should reflect the nature of the task.                                                                               

`Prohibit direct changes to the main`: All changes should be pushed into                                                                                
the main via **Pull Requests (PR)** after review and approval by other team members.                                                                               


**Commits**                                                                               
* `Many commits`: Make commits frequently to track progress and facilitate                                                                               
possible debugging.                                                                               
* `Informative commits`: Each commit should contain a clear and concise                                                                               
description of the changes made.                                                                               
* `Prefix commit system`:
    * `doc`: To add or modify documentation.                                                                               
    * `feat`: To add new functionality.                                                                               
    * `fix`: For bug fixes or debugging.                                                                               

**Working with Pull Requests (PR)**                                                                                                                                                              
* `PR Description`: Each PR should contain a detailed description of the                                                                                
changes made and references to relevant tasks or requirements.                                                                               
* `Code-review`: Prior to merging with the main, the PR should be                                                                               
code-reviewed by at least one other team member.                                                                               
* `Testing`: Before creating a PR, make sure your code passes all                                                                                
tests and meets coding standards.                                                                               

**Regular updates**
`Synchronize with main`: Regularly update your working branches by                                                                                
synchronizing them with the main branch of main to avoid merge conflicts.                                                                               

---

### **Additionally**                                                                               
**Docker**:                                                                               
* Project containerization using [**Docker**](https://www.docker.com/).                                                                               
