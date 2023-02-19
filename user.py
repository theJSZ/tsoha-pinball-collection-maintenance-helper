from db import db

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
