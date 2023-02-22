from app import app
from db import db
from flask import render_template, session, request, redirect, flash
from werkzeug.security import check_password_hash, generate_password_hash
from user import check_new_password, check_new_username

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/collections")
def collections():
    sql = """SELECT C.id, C.name
             FROM collections C, rights R
             WHERE R.user_id = :user_id
               AND R.collection_id = C.id"""

    if session.get("collection_id",0):
        del session["collection_id"]

    collections_to_show = db.session.execute(
        sql, {"user_id": session["user_id"]}
    ).fetchall()  # [0] = id, [1] = name

    return render_template("collections.html", collections_list=collections_to_show)


@app.route("/collection/<int:collection_id>")
def collection(collection_id):
    # find machines of collection
    sql = """SELECT M.id, M.name, (SELECT COALESCE(MAX(severity), 0) AS max_severity
                                    FROM issues
                                    WHERE machine_id = M.id
                                    AND closed_by IS NULL)
            FROM machines M
            WHERE collection_id = :collection_id
            ORDER BY M.name"""
    machines = db.session.execute(sql, {"collection_id": collection_id}).fetchall()

    sql = "SELECT name FROM collections WHERE id = :collection_id"
    collection_name = db.session.execute(
        sql, {"collection_id": collection_id}
    ).fetchone()[0]

    session["collection_id"] = collection_id

    return render_template(
        "collection.html",
        machines=machines,
        collection_name=collection_name,
        collection_id=collection_id
    )


@app.route("/logout")
def logout():
    del session["username"]
    if session.get("collection_id",0):
        del session["collection_id"]
    return redirect("/")


@app.route("/login", methods=["POST"])
def login():
    # get form contents
    username = request.form["username"]
    password = request.form["password"]

    # check validity
    sql = "SELECT * FROM users WHERE username = :username"
    user = db.session.execute(sql, {"username": username}).fetchone()
    if user:
        stored_pw_hash = user["password"]
    if not user or not check_password_hash(stored_pw_hash, password):
        flash("Invalid username or password")
        return redirect("/")

    session["username"] = username
    sql = "SELECT id FROM users WHERE username = :username"
    user_id = db.session.execute(sql, {"username": username}).fetchone()[0]
    session["user_id"] = user_id
    return redirect("/collections")


@app.route("/register")
def create_user():
    return render_template("register.html")


@app.route("/validate_new_user", methods=["POST"])
def validate_new_user():
    # get form contents
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    password_confirm = request.form["password_confirm"]

    # check username and pw are valid
    username_status = check_new_username(username)
    password_status = check_new_password(password, password_confirm)
    if password_status != "valid" or username_status != "valid":
        return redirect("/register")

    # create password hash and insert new user
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, email, password) VALUES (:username, :email, :password) RETURNING id"
    result = db.session.execute(
        sql, {"username": username, "email": email, "password": hash_value}
    )
    db.session.commit()
    user_id = result.fetchone()[0]

    session["username"] = username
    session["user_id"] = int(user_id)
    return redirect("/")


@app.route("/new_collection")
def new_collection():
    return render_template("new_collection.html")


# @app.route("/add_comment", methods=["POST"])
# def add_comment():
#     comment_content = request.form["comment_content"]
#     issue_id = request.form["issue_id"]
#     user_id = session["user_id"]
#     machine_id = db.session.execute(
#         "SELECT machine_id FROM issues WHERE id = :issue_id", {"issue_id": issue_id}
#     ).fetchone()[0]

#     sql = """INSERT INTO comments (user_id, issue_id, created_at, content)
#             VALUES (:user_id, :issue_id, NOW(), :content)"""
#     db.session.execute(
#         sql, {"user_id": user_id, "issue_id": issue_id, "content": comment_content}
#     )
#     db.session.commit()
#     return redirect(f"/machine_info/{machine_id}")


# @app.route("/comment/<int:issue_id>")
# def comment(issue_id):
#     sql = "SELECT * FROM issues WHERE id = :issue_id"
#     issue = db.session.execute(sql, {"issue_id": issue_id}).fetchone()
#     return render_template("/comment.html", issue=issue)


@app.route("/machine_info/<int:machine_id>")
def machine_info(machine_id):
    sql = "SELECT * FROM machines WHERE id = :machine_id"
    machine = db.session.execute(sql, {"machine_id": machine_id}).fetchone()
    sql = """SELECT I.id, I.content, I.created_at, I.severity, U.username
            FROM issues I, users U
            WHERE machine_id = :machine_id
            AND closed_by IS NULL
            AND U.id = I.user_id"""
    issues = db.session.execute(sql, {"machine_id": machine_id}).fetchall()

    return render_template(
        "machine_info.html", machine=machine, issues=issues, n_issues=len(issues)
    )


@app.route("/new_issue/<int:machine_id>")
def new_issue(machine_id):
    sql = "SELECT * FROM machines WHERE id = :machine_id"
    machine = db.session.execute(sql, {"machine_id": machine_id}).fetchone()
    print(f"machine: {machine}")
    return render_template("new_issue.html", machine=machine)


@app.route("/input_new_issue", methods=["POST"])
def input_new_issue():
    issue_content = request.form["issue_content"]
    machine_id = request.form["machine_id"]
    severity = request.form["severity"]
    sql = """INSERT INTO issues (machine_id, user_id, created_at, content, closed_by, severity)
            VALUES (:machine_id, :user_id, NOW(), :content, NULL, :severity)"""
    db.session.execute(
        sql,
        {
            "machine_id": machine_id,
            "user_id": session["user_id"],
            "content": issue_content,
            "severity": severity,
        },
    )
    db.session.commit()
    # return redirect(f"/machine_info/{machine_id}")
    return redirect(f"/collection/{session['collection_id']}")




@app.route("/edit_collection", methods=["POST", "GET"])
def edit_collection():
    if request.method == "GET":
        # collection_id = request.form["collection_id"]
        return render_template("edit_collection.html")
    if request.method == "POST":
        collection_id = request.form["collection_id"]
        machine_names = request.form["machine_names"].split("\n")
        for machine_name in machine_names:
            if not machine_name:
                continue
            db.session.execute(
                "INSERT INTO machines (name, collection_id) VALUES (:machine_name, :collection_id)",
                {"machine_name": machine_name.strip(), "collection_id": session["collection_id"]},
            )
        db.session.commit()
        return redirect(f"/collection/{session['collection_id']}")


@app.route("/validate_new_collection", methods=["POST"])
def create_new_collection():
    collection_name = request.form["collection_name"]
    machine_names = request.form["machine_names"].split("\n")
    sql = """SELECT C.name
            FROM collections C, rights R
            WHERE R.collection_id = C.id
            AND R.user_id = :user_id"""
    existing_collection_tuples = db.session.execute(
        sql, {"user_id": session["user_id"]}
    ).fetchall()
    existing_collection_names = [t[0].lower() for t in existing_collection_tuples]

    if collection_name.lower() in existing_collection_names:
        flash(f"Collection {collection_name} already in use")
        return redirect("/new_collection")

    collection_id = db.session.execute(
        "INSERT INTO collections (name) VALUES (:collection_name) RETURNING id",
        {"collection_name": collection_name},
    ).fetchone()[0]

    db.session.execute(
        "INSERT INTO rights (user_id, collection_id, is_admin) VALUES (:user_id, :collection_id, true)",
        {"user_id": session["user_id"], "collection_id": collection_id},
    )

    for machine_name in machine_names:
        if not machine_name:
            continue
        db.session.execute(
            "INSERT INTO machines (name, collection_id) VALUES (:machine_name, :collection_id)",
            {"machine_name": machine_name.strip(), "collection_id": collection_id},
        )

    db.session.commit()

    return redirect("/collections")

@app.route("/close_issue", methods=["POST"])
def close_issue():
    issue_id = request.form["issue_id"]
    print(f"***** trying to hide {issue_id} *******")
    user_id = session["user_id"]
    sql = "UPDATE issues SET closed_by = :user_id WHERE id = :issue_id RETURNING machine_id"
    machine_id = db.session.execute(sql, {"user_id": user_id, "issue_id": issue_id}).fetchone()[0]
    db.session.commit()
    return redirect(f"/machine_info/{machine_id}")

@app.route("/delete_machine", methods=["POST"])
def delete_machine():
    machine_id = request.form["machine_id"]
    collection_id = request.form["collection_id"]
    sql = "DELETE FROM machines WHERE id = :machine_id RETURNING name"
    machine_name = db.session.execute(sql, {"machine_id": machine_id}).fetchone()[0]
    db.session.commit()
    flash(f"{machine_name} removed from collection")
    return redirect(f"/collection/{collection_id}")