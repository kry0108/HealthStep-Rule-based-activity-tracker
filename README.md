HealthStep – Health Activity and Progress Tracking System
 Project Overview

HealthStep is a rule-based health activity and progress tracking web application developed using Python and Django.

The system helps users evaluate their health-related information, receive suitable health activities, and track their progress over time. 
The main goal of the project is to provide a simple and user-friendly platform for maintaining healthy daily activities and monitoring progress.

 Objectives
To provide a digital platform for health activity management.
To evaluate users based on their entered health information.
To assign suitable activities using predefined rules.
To allow users to track their activity progress.
To reduce the need for manual health activity tracking.
To provide a simple and easy-to-use web interface.
  Features
1. User Registration and Login
New users can create an account.
Registered users can securely log in.
Users can access their personal health and activity information.
2. Health Evaluation
Users enter required health-related information.
The system evaluates the entered information.
A rule-based approach is used to determine suitable activities.
3. Activity Assignment
Health activities are assigned based on predefined rules.
Activities can include exercise, walking, hydration, and other healthy habits.
Users can view their assigned activities.
4. Progress Tracking
Users can track their assigned activities.
Activity completion can be recorded.
Users can monitor their progress over time.
5. User Dashboard
Displays relevant user information.
Provides access to health evaluation and assigned activities.
Allows users to monitor their overall activity progress.
🛠️ Technologies Used
Technology	Purpose
Python	Backend programming
Django	Web framework
HTML	Web page structure
CSS	Styling and layout
JavaScript	Client-side functionality
SQLite / MySQL	Database
Git & GitHub	Version control and project management
 Project Structure
HealthStep/
│
├── manage.py
│
├── healthstep/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── <your_app>/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── requirements.txt
├── .gitignore
└── README.md

Replace <your_app> with the actual Django app name used in your project.

 Installation and Setup
1. Clone the Repository
git clone YOUR_GITHUB_REPOSITORY_URL
2. Open the Project Folder
cd HealthStep
3. Create a Virtual Environment
python -m venv venv
4. Activate the Virtual Environment

Windows PowerShell:

.\venv\Scripts\Activate.ps1

If PowerShell execution policy causes an error, you can use Command Prompt:

venv\Scripts\activate
5. Install Required Packages
pip install -r requirements.txt
6. Apply Database Migrations
python manage.py migrate
7. Create an Admin User
python manage.py createsuperuser

Follow the instructions displayed in the terminal.

8. Start the Development Server
python manage.py runserver

Open the application in your browser:

http://127.0.0.1:8000/
 Main Modules

The HealthStep system consists of the following major modules:

User Registration and Authentication
Health Evaluation
Health Activity Assignment
Activity Progress Tracking
User Dashboard
Admin Management
 System Workflow
User Registration/Login
          ↓
   Health Evaluation
          ↓
   Rule-Based Analysis
          ↓
 Activity Assignment
          ↓
 User Performs Activities
          ↓
   Progress Tracking
          ↓
    Progress Display
 Security

The project uses Django's built-in authentication and security features for handling user accounts and application access.

Sensitive information such as passwords, secret keys, and environment variables should not be committed to the GitHub repository.

 Future Enhancements
Add personalized health recommendations.
Add graphical progress reports.
Add daily/weekly/monthly activity statistics.
Add notification and reminder functionality.
Add more health evaluation rules.
Add REST API support.
Improve UI/UX and mobile responsiveness.
Deploy the application to a cloud platform.
 Project Type

Academic / College Project

Project Name: HealthStep
Domain: Health & Wellness
Framework: Django
Language: Python
