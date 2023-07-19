# Tietokantasovellus
Aihe: verkkopeli
Each user must create an account and log in. There are two types of accounts: normal users and administrators. Administrators can delete other accounts and their data.
A reference to the users' game characters are saved inside their accounts.
The characters have data about their statuses such as hitpoints and attack damage.
Users can create new map where to play the game with other players. The map contains enemies.
There is a simple text chat.
The goal of the game is to kill monsters and not die, so the game part will be really simple with probably only one type of player characters and one type of monsters.

Instead of being in a schema file, the databases are created in the models.py file.

I am developing this project with the help of this tutorial: https://www.youtube.com/watch?v=dam0GPOAvVI and some bootstraps from https://getbootstrap.com/. I also used the following documentations: https://flask-login.readthedocs.io/en/latest/ 