The topic is a recipe website where you can publish food recipes.

- Users can create accounts and log in.

- Users can add their own recipes, edit their own recipes and like other users' recipes.

- The recipes include the name of the publisher and the amount of likes.

- Users can also create private recipes that do not show to others.

- Users have profile pages where all their published recipes are shown. 

- Users can send messages to each other through their profile pages.

- All public recipes are shown on the main page.

- Users can search public recipes with search words.

- Admin users can delete other users' recipes and users' can delete their own recipes.


Things that are working now:

- Account creation and login.
- Creating public and private recipes, liking other users' recipes, and deleting your own recipes.
- Main page shows all public recipes.


# Set up guide:

Clone this repository. Navigate to the root directory.

There you can have virtualenv installed by using pip install virtualenv. This might make easier to remove unnecessary
dependencies after testing my application.

inside virtualenv or normally use 
```bash
pip install -r requirements.txt
```
to install dependencies


To initialize the database use the command 
```bash
psql -U username -d database -a -f schema.sql
```
where the username is your psql username and the database is some database that you have created. Do also create a .env file with the values DATABASE_URL="postgresql:///database" and SECRET_KEY="secretkey" where database is the name of you database and secretkey is some string.



If you installed virtualenv, to start the virtual environment use
```bash
source venv/Scripts/activate
```
or the command
```bash
source venv/bin/activate
```


To start the website use the command
```bash
flask run
```
