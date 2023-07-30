The topic is a recipe website where you can publish food recipes.

- Users can create accounts and log in.

- Users can add their own recipes, edit their recipes and like other peoples recipes.

- The recipes include the name of the publisher and the amount of likes.

- Users can also create private recipes that do not show to others.

- All public recipes are shown on the main page.

- Users can search public recipes with search words.

- Admin users can delete other users' recipes.

To initialize the database use the command psql -U username -d database -a -f schema.sql  where the username is your psql username and the database is some database that you have created.

To start the website use the command source venv/Scripts/activate or the command source venv/bin/activate and run the main.py file with flask run

create a .env file with DATABASE_URL="postgresql:///database"  and SECRET_KEY=""