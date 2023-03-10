from db import db
from flask import flash

def check_new_username(username):
    if username == "":
        flash("Username can not be empty")
        return

    existing_usernames = db.session.execute("SELECT username FROM users").fetchall()

    for tuple in existing_usernames:
        if username == tuple[0]:
            flash(f"Username {username} taken")
            return

    return "valid"


def check_new_password(password, password_confirm):
    status = "valid"

    if len(password) < 8:
        flash("Password must be at least eight characters")
        status = "invalid"

    if password != password_confirm:
        flash("Password did not match password confirm")
        status = "invalid"

    return status


def user_of_collection(user_id, collection_id, name):
    if db.session.execute("SELECT * FROM rights WHERE user_id=:user_id AND collection_id=:collection_id", {"user_id": user_id, "collection_id": collection_id}).fetchone():
        return True
    return False

def username_to_id(name):
    try:
        user_id = db.session.execute("SELECT id FROM users WHERE username=:username", {"username": name}).fetchone()[0]
    except:
        return None
    return user_id