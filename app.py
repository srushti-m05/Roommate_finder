from flask import Flask, render_template, request, redirect, session
from database import init_db, get_db
from models.user import User
from datastructures.linked_list import UserList
from datastructures.graph import Graph
from datastructures.priority_queue import PriorityQueue
from services.matcher import compatibility
import random


app = Flask(__name__)
app.secret_key = "secret123"


init_db()


def generate_uid():
    return "RM" + str(random.randint(1000, 9999))


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uid = request.form["uid"]
        pwd = request.form["password"]

        con = get_db()
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM users WHERE uid=? AND password=?",
            (uid, pwd)
        )
        row = cur.fetchone()
        con.close()

        if row:
            session["uid"] = uid
            return redirect("/dashboard")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        d = request.form
        uid = generate_uid()

        con = get_db()
        cur = con.cursor()
        cur.execute("""
        INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            uid,
            d["name"],
            d["age"],
            d["gender"],
            d["city"],
            d["area"],
            d["food"],
            d["sleep"],
            d["smoking"],
            d["drinking"],
            d["cleanliness"],
            d["occupation"],
            d["timing"],
            d["password"]
        ))
        con.commit()
        con.close()

        return f"""
        <h3>Registration  is Successful,Thanks for registering.</h3>
        <p>Your User ID is: <b>{uid}</b></p>
        <a href="/">Go to Login</a>
        """

    return render_template("register.html")

@app.route("/matches")
def matches():
    if "uid" not in session:
        return redirect("/")

    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    con.close()

    users_ll = UserList()
    graph = Graph()
    current_user = None

    for r in rows:
        u = User(r)
        users_ll.add(u)
        graph.add_user(u.uid)
        if u.uid == session["uid"]:
            current_user = u

    if not current_user:
        return redirect("/")

    all_users = users_ll.to_list()

    for i in range(len(all_users)):
        for j in range(i + 1, len(all_users)):
            score = compatibility(all_users[i], all_users[j])
            if score >= 60:
                graph.add_edge(all_users[i].uid, all_users[j].uid, score)

    pq = PriorityQueue()
    for uid, score in graph.get_connections(current_user.uid):
        user = next(u for u in all_users if u.uid == uid)
        pq.push(-score, user)

    results = []
    while not pq.empty():
        score, user = pq.pop()
        results.append((user, score))

    return render_template("matches.html", matches=results)





@app.route("/admin")
def admin():
    if "admin" not in session:
        return redirect("/admin-login")

    con = get_db()
    cur = con.cursor()
    cur.execute(
        "SELECT uid, name, age, gender, city, occupation FROM users"
    )
    users = cur.fetchall()
    con.close()

    return render_template("admin.html", users=users)




@app.route("/admin-logout")
def admin_logout():
    session.pop("admin", None)
    return redirect("/")


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    error = None

    if request.method == "POST":
        password = request.form["password"]

        if password == "admin123":
            session["admin"] = True
            return redirect("/admin")
        else:
            error = "Invalid admin password"

    return render_template("admin-login.html", error=error)

@app.route("/dashboard")
def dashboard():
    if "uid" not in session:
        return redirect("/")

    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE uid=?", (session["uid"],))
    row = cur.fetchone()
    con.close()

    if not row:
        return redirect("/")

    user = User(row)
    return render_template("dashboard.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)
