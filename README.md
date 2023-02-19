# Pinball collection maintenance helper
###### Python / Flask / PostgreSQL project for the Spring 2023 course "Tietokantasovellus", University of Helsinki

### What and why:
In the pinball community it is not unusual to see collections of [several dozen machines](http://www.flipperikellari.fi/flipperit/). Pinball machines have a lot of ways to malfunction and especially with a large collection that sees a lot of players, some kind of system for keeping track of these is very helpful. This app aims to make it easy
* for a player (who is not necessarily the owner of the machine) to report a malfunction
* for the owner (or some other designated person) to see the reported malfunctions

The finished app should have the following features:
TO DO:
* A photo can be included in the report
* An admin can invite other people to become normal users of a collection

DONE:
* All users log in with a username and password DONE
* A user can create a new collection which makes them an admin with regard to that collection DONE
* An admin can edit the collection afterwards DONE
* Any user can report a malfunction. The report always concerns a certain machine and must include a written description of what is wrong DONE
* The malfunction is given a severity rating from 1 (not severe, e.g. a light that is not working) to 3 (very severe, e.g. an important feature of the game is impossible to achieve because a mechanical switch not working) DONE
* An admin can mark a malfunction as fixed (i.e. delete the entry) DONE
