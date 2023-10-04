The topic is a recipe website where you can publish food recipes.

- Users can create accounts and log in.

- Users can add their own recipes, edit their own recipes and like and comment on other users' recipes. As I like the idea of giving as much likes as you feel grateful, giving likes is not limited.

- The recipes include the name of the publisher and the amount of likes.

- Users can also create private recipes that do not show to others.

- Users have profile pages where all their published recipes are shown. 

- Users can search for other users' profiles using their usernames as search words.

- Users can send messages to each other through their profile pages.

- All public recipes are shown on the main page.

- Users can search public recipes with search words.

- Admin users can delete other users' recipes and users can delete their own recipes.


# Set up guide:
This project expects you to have PostgreSQL and Python 3 installed.


Clone this repository. Navigate to the root directory.

You can have virtualenv installed by using pip install virtualenv. This might make easier to remove unnecessary
dependencies after testing my application.


If you are using virtualenv, first use the command 
```bash
virtualenv venv
```
to create a virtual environment.


Start the virtual environment use 
```bash
source venv/Scripts/activate
```
or
```bash
source venv/bin/activate
```


Inside virtualenv or normally use 
```bash
pip install -r requirements.txt
```
to install dependencies.


To initialize the database use the command 
```bash
psql -U username -d database -a -f schema.sql
```
where the username is your psql username and the database is some database that you have created. 


Do also create a .env file with the values DATABASE_URL="postgresql:///database" and SECRET_KEY="secretkey" where database is the name of your database and secretkey is some string.


To start the website use the command
```bash
flask run
```
