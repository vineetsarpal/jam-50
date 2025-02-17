# Jam 50
#### A Flask based web application for booking jam sessions.
#### Video Demo: {video_url}

## About
This is my Final Project for Harvard's CS50x Introduction to Computer Science course. It's a web application designed to connect musicians with the listed jam spaces, allowing them to easily explore, and book jam spaces plus view their booking history.

## Features
* User authentication (Register and Login)
* Explore and Book Jam Spaces
* View Booking history
* Guest access for browsing without an account
* Admin access to manage (add, delete) spaces

## Usage
* Register for an account or continue as a guest
* Explore available jam spaces and make bookings
* View your booking history in the 'Bookings' tab
* Admins can manage spaces

## Built With
* Flask - Web framework
* Python - Programming language
* HTML - Markup Language
* Jinja - Web templating engine
* Bootstrap - CSS Framework
* SQLite - Database

## Project Details
#### Filewise breakdown
* 'instance' directory - contains the sqlite db
    * jam.db - database file that is preloaded with admin, and guest user data required for the application. All passwords in the db are hashed.
* 'static' directory - contains static files like images, and CSS stylesheet
    * music.png - logo image
    * styles.css - CSS style sheet
* 'templates' directory - contains the HTML documents
    * add_space.html - web page to add a new space (admin only)
    * bookings.html - web page to view user's  booking history
    * credits.html - web page to credit the author's of the external images used in the website
    * error.html - web page to display error messages
    * index.html - home page
    * layout.html - layout HTML document that encapsulates other HTML documents and includes common elements like the navbar, and footer
    * login.html - web page for user login 
    * register.html - web page for user regisration and the ability to continue(login) as a guest user
    * space.html - web page to display details of a single Jam space, and the ability to book or delete (admin only)
    * spaces.html - web page to display all Jam spaces
* app.py - the main python file that instantiates the flask app, the db, defines all routes, and all the functionalities
* helpers.py - contains helper funcitons utilized by the app 
* models.py - conatins the 
* requirements.txt - text file containing the list of all Python libraries and modules imported

## Design Decision
* Database choice
    * This project utilizes SQLite as its database engine. SQLite is lightweight and portable, making it a suitable choice for the purposes of this Project. The database file is committed to the repo to provide for a simplified intitial setup with the essential admin and guest user accounts being preloaded. This ensures the Core application features work out-of-the-box.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.