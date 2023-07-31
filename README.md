The topic is a recipe website where you can publish food recipes.

- Users can create accounts and log in.

- Users can add their own recipes, edit their recipes and like other peoples recipes.

- The recipes include the name of the publisher and the amount of likes.

- Users can also create private recipes that do not show to others.

- Users have profile pages where all their published recipes are shown. 

- Users can send messages to each other through their profile pages.

- All public recipes are shown on the main page.

- Users can search public recipes with search words.

- Admin users can delete other users' recipes.


# Set up guide:

You can have virtualenv installed by using pip install virtualenv. This might make easier to remove unnecessary
dependencies after testing my application.

Start the application with 
```bash
source venv/Scripts/activate
```
or
```bash
source venv/bin/activate
```

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

To start the website use the command 
```bash
source venv/Scripts/activate
```
or the command
```bash
source venv/bin/activate
```
and run the main.py file with 
```bash
flask run
```
