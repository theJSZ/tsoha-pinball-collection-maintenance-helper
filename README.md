# Pinball collection maintenance helper
###### Python / Flask / PostgreSQL project for the Spring 2023 course "Tietokantasovellus", University of Helsinki

### What and why:
In the pinball community it is not unusual to see collections of [several dozen machines](http://www.flipperikellari.fi/flipperit/). Pinball machines have a lot of ways to malfunction and especially with a large collection that sees a lot of players, some kind of system for keeping track of these is very helpful. This app aims to make it easy
* for a player (who is not necessarily the owner of the machine) to report a malfunction
* for the owner (or some other designated person) to see the reported malfunctions

The finished app should have the following features:  
###### TO DO:
* A photo can be included in the report
* An admin can invite other people to become normal users or other admins of a collection

###### DONE:
* All users log in with a username and password
* A user can create a new collection which makes them an admin with regard to that collection
* An admin can edit the collection afterwards
* Any user can report a malfunction. The report always concerns a certain machine and must include a written description of what is wrong
* The malfunction is given a severity rating from 1 (not severe, e.g. a light that is not working) to 3 (very severe, e.g. an important feature of the game is impossible to achieve because a mechanical switch not working)
* An admin can mark a malfunction as fixed (i.e. delete the entry)

### How to use (locally):
#### 1) installing
Clone the repository using your preferred method.  
Go to the root directory. Create a file called `.env` with the following contents (replacing the secret key value with an actual random string):
```
DATABASE_URL = postgresql://
SECRET_KEY = <your secret key here>
```
Launch a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```
Install required packages:
```
pip install -r requirements.txt
```
Launch your postgresql server. I do it by `start-pg.sh` but there may be other ways?

You probably want to create a new database in order to not mess with your existing one. You can do that by launching the interpreter: `psql` and using the command `CREATE DATABASE <your-database-name>;`

Build the database:
```
psql -d <your-database-name> < schema.sql
```
Launch the app:
```
flask run
```
#### 2) using
After creating a user account you will see this:
![](docs/1.jpg)

Click the button to create a new collection. In this view you can name your collection and provide a list of machines it includes.  
![](docs/2.jpg)  
After this you can navigate to your collection and machines, adding or removing malfunction reports and/or machines as needed.  
![](docs/3.jpg)  
Here Batman has a serious malfunction, Austin Powers has a somewhat serious malfunction, and Cirqus Voltaire has a not serious malfunction. The machines in blue have no reported malfunctions.
![](docs/4.jpg)
Sure enough it is pretty serious.

#### To do:
At the moment there is no way an admin can add other users (as admin or normal user) to their collection. This is an important feature to enable the whole player base to create issues. Only admins should be able to close them though, as well as add/remove machines from the collection.

Could be nice (but not critical) to be able to submit a photo with the issue.

Code is a horrible mess and should be made clearer if I only know how.
