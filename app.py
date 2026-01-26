from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import json
import secrets
import csv
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "change-this-" + secrets.token_hex(16)

DB_NAME = "app.db"

# Pre-defined grocery items by category
GROCERY_CATALOG = {
    "Vegetables": [
        "Tomato",
        "Potato",
        "Onion",
        "Carrot",
        "Cucumber",
        "Cabbage",
        "Spinach",
        "Broccoli",
        "Bell Pepper",
        "Garlic",
        "Ginger",
        "Lettuce",
        "Peas",
        "Corn",
    ],
    "Fruits": [
        "Apple",
        "Banana",
        "Orange",
        "Mango",
        "Grape",
        "Watermelon",
        "Papaya",
        "Pineapple",
        "Strawberry",
        "Lemon",
        "Lime",
        "Kiwi",
        "Guava",
        "Pomegranate",
    ],
    "Grains & Cereals": [
        "Rice",
        "Wheat Flour",
        "Sugar",
        "Salt",
        "Maida",
        "Oats",
        "Bread",
        "Pasta",
        "Semolina",
    ],
    "Spices": [
        "Turmeric",
        "Chili Powder",
        "Cumin",
        "Coriander",
        "Mustard Seeds",
        "Fenugreek",
        "Cardamom",
        "Cloves",
        "Cinnamon",
        "Black Pepper",
        "Asafoetida",
    ],
    "Dairy & Eggs": [
        "Milk",
        "Yogurt",
        "Cheese",
        "Butter",
        "Ghee",
        "Eggs",
        "Paneer",
        "Cream",
    ],
    "Meat & Fish": ["Chicken", "Mutton", "Fish", "Shrimp", "Ground Meat", "Sausage"],
    "Snacks & Dry Items": [
        "Nuts (Mixed)",
        "Almonds",
        "Cashews",
        "Peanuts",
        "Cookies",
        "Biscuits",
        "Popcorn",
    ],
    "Beverages": ["Tea", "Coffee", "Juice", "Water Bottles", "Soft Drinks"],
    "Oils & Condiments": [
        "Cooking Oil",
        "Ghee",
        "Soy Sauce",
        "Tomato Sauce",
        "Mustard",
        "Vinegar",
    ],
    "Others": ["Baking Powder", "Yeast", "Honey", "Jam", "Peanut Butter"],
}


def db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = db()

    # Create users table
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """
    )

    # Create grocery_lists table
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS grocery_lists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            list_type TEXT NOT NULL,
            title TEXT NOT NULL,
            items_json TEXT NOT NULL,
            status TEXT NOT NULL,
            receiver_id INTEGER,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """
    )

    # Migrate existing database
    try:
        conn.execute("ALTER TABLE grocery_lists ADD COLUMN receiver_id INTEGER")
        conn.commit()
    except sqlite3.OperationalError:
        pass

    conn.close()


init_db()


def init_feedback_csv():
    """Initialize CSV file for feedback if it doesn't exist"""
    feedback_dir = "feedback_data"
    os.makedirs(feedback_dir, exist_ok=True)

    feedback_file = os.path.join(feedback_dir, "feedback.csv")

    if not os.path.exists(feedback_file):
        with open(feedback_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "ID",
                    "Email",
                    "Rating",
                    "Improvements",
                    "Type",
                    "Message",
                    "User ID",
                    "Submitted At",
                ]
            )

    return feedback_file


def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    conn = db()
    user = conn.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    conn.close()
    return user


def get_payload():
    return request.get_json(silent=True) or request.form


@app.get("/")
def index():
    return redirect(
        url_for("home_page") if session.get("user_id") else url_for("login_page")
    )


@app.get("/home")
@app.get("/home.html")
def home_page():
    user = current_user()
    if not user:
        return redirect(url_for("login_page"))
    return render_template("home.html", username=user["username"])


@app.get("/feedback")
@app.get("/feedback.html")
def feedback_page():
    return render_template("feedback.html")


@app.get("/login")
@app.get("/login.html")
def login_page():
    return render_template("login.html")


@app.get("/signup")
@app.get("/signup.html")
def signup_page():
    return render_template("signup.html")


@app.get("/forgot")
@app.get("/forgot.html")
def forgot_page():
    return render_template("forgot.html")


@app.post("/api/signup")
def api_signup():
    p = get_payload()
    username = (p.get("username") or p.get("newUsername") or "").strip()
    email = (p.get("email") or p.get("newEmail") or "").strip()
    password = p.get("password") or p.get("newPassword") or ""
    confirm = p.get("confirm") or p.get("confirmPassword") or ""

    if not username or not email or not password:
        return jsonify(ok=False, message="Please fill all fields."), 400
    if len(password) < 6:
        return jsonify(ok=False, message="Password must be at least 6 characters."), 400
    if password != confirm:
        return jsonify(ok=False, message="Passwords do not match."), 400
    if "@" not in email:
        return jsonify(ok=False, message="Please enter a valid email."), 400

    conn = db()
    try:
        conn.execute(
            "INSERT INTO users(username,email,password_hash,created_at) VALUES(?,?,?,?)",
            (
                username,
                email,
                generate_password_hash(password),
                datetime.utcnow().isoformat(),
            ),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify(ok=False, message="Username or email already exists."), 409
    conn.close()
    return jsonify(ok=True, message="Account created.")


@app.post("/api/login")
def api_login():
    p = get_payload()
    username = (p.get("username") or "").strip()
    password = p.get("password") or ""

    if not username or not password:
        return jsonify(ok=False, message="Please enter username and password."), 400

    conn = db()
    user = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
    conn.close()

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify(ok=False, message="Invalid username or password."), 401

    session["user_id"] = user["id"]
    session["username"] = user["username"]
    return jsonify(ok=True, username=user["username"])


@app.post("/api/logout")
def api_logout():
    session.clear()
    return jsonify(ok=True)


@app.post("/api/forgot/request")
def api_forgot_request():
    p = get_payload()
    email = (p.get("email") or "").strip()
    if not email:
        return jsonify(ok=False, message="Enter your email."), 400

    conn = db()
    user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    conn.close()
    if not user:
        return jsonify(ok=False, message="No account found with this email."), 404

    code = f"{secrets.randbelow(1000000):06d}"
    session["reset_user_id"] = user["id"]
    session["reset_code"] = code
    session["reset_expires"] = (datetime.utcnow() + timedelta(minutes=10)).isoformat()

    return jsonify(ok=True, message="Reset code generated.", code=code)


@app.post("/api/forgot/verify")
def api_forgot_verify():
    p = get_payload()
    code = (p.get("code") or "").strip()

    if not code:
        return jsonify(ok=False, message="Enter the code."), 400

    saved = session.get("reset_code")
    expires = session.get("reset_expires")
    if not saved or not expires:
        return jsonify(ok=False, message="Please request a new code."), 400
    if datetime.utcnow() > datetime.fromisoformat(expires):
        return jsonify(ok=False, message="Code expired. Request again."), 400
    if code != saved:
        return jsonify(ok=False, message="Wrong code."), 401

    session["reset_verified"] = True
    return jsonify(ok=True)


@app.post("/api/forgot/reset")
def api_forgot_reset():
    p = get_payload()
    new_password = p.get("newPassword") or ""
    confirm = p.get("confirmNewPass") or ""

    if not session.get("reset_verified") or not session.get("reset_user_id"):
        return jsonify(ok=False, message="Verify code first."), 400
    if len(new_password) < 6:
        return jsonify(ok=False, message="Password must be at least 6 characters."), 400
    if new_password != confirm:
        return jsonify(ok=False, message="Passwords do not match."), 400

    uid = session["reset_user_id"]
    conn = db()
    conn.execute(
        "UPDATE users SET password_hash=? WHERE id=?",
        (generate_password_hash(new_password), uid),
    )
    conn.commit()
    conn.close()

    session.pop("reset_user_id", None)
    session.pop("reset_code", None)
    session.pop("reset_expires", None)
    session.pop("reset_verified", None)

    return jsonify(ok=True, message="Password updated.")


@app.get("/api/users")
def api_get_users():
    """Get all registered users except current user"""
    user = current_user()
    if not user:
        return jsonify(ok=False, message="Not logged in."), 401

    conn = db()
    users = conn.execute(
        "SELECT id, username FROM users WHERE id != ?", (user["id"],)
    ).fetchall()
    conn.close()

    return jsonify(
        ok=True, users=[{"id": u["id"], "username": u["username"]} for u in users]
    )


@app.get("/api/catalog")
def api_get_catalog():
    """Return the pre-defined grocery items catalog"""
    return jsonify(ok=True, catalog=GROCERY_CATALOG)


@app.get("/api/groceries/<list_type>")
def api_get_lists(list_type):
    user = current_user()
    if not user:
        return jsonify(ok=False, message="Not logged in."), 401
    if list_type not in ("sent", "received", "drafts"):
        return jsonify(ok=False, message="Invalid list type."), 400

    conn = db()
    rows = conn.execute(
        "SELECT * FROM grocery_lists WHERE user_id=? AND list_type=? ORDER BY id DESC",
        (user["id"], list_type),
    ).fetchall()
    conn.close()

    data = []
    for r in rows:
        data.append(
            {
                "id": r["id"],
                "title": r["title"],
                "status": r["status"],
                "items": json.loads(r["items_json"]) if r["items_json"] else [],
            }
        )
    return jsonify(ok=True, lists=data)


@app.get("/api/groceries/<int:list_id>")
def api_get_list_detail(list_id):
    """Get a single grocery list with full details"""
    user = current_user()
    if not user:
        return jsonify(ok=False, message="Not logged in."), 401

    conn = db()
    row = conn.execute("SELECT * FROM grocery_lists WHERE id=?", (list_id,)).fetchone()
    conn.close()

    if not row:
        return jsonify(ok=False, message="List not found."), 404

    if row["user_id"] != user["id"] and row["list_type"] != "received":
        return jsonify(ok=False, message="Unauthorized."), 403

    return jsonify(
        ok=True,
        list={
            "id": row["id"],
            "title": row["title"],
            "items": json.loads(row["items_json"]),
            "status": row["status"],
            "list_type": row["list_type"],
            "receiver_id": row["receiver_id"],
        },
    )


@app.post("/api/groceries")
def api_create_list():
    user = current_user()
    if not user:
        return jsonify(ok=False, message="Not logged in."), 401

    p = request.get_json(silent=True) or {}
    list_type = p.get("list_type", "drafts")
    title = (p.get("title") or "").strip()
    items = p.get("items") or []
    status = p.get("status", "Pending")

    if list_type not in ("sent", "received", "drafts"):
        return jsonify(ok=False, message="Invalid list type."), 400
    if not title:
        return jsonify(ok=False, message="Title required."), 400
    if not isinstance(items, list):
        return jsonify(ok=False, message="Items must be a list."), 400

    conn = db()
    conn.execute(
        "INSERT INTO grocery_lists(user_id,list_type,title,items_json,status,created_at) VALUES(?,?,?,?,?,?)",
        (
            user["id"],
            list_type,
            title,
            json.dumps(items),
            status,
            datetime.utcnow().isoformat(),
        ),
    )
    conn.commit()
    conn.close()
    return jsonify(ok=True)


@app.delete("/api/groceries/<int:list_id>")
def api_delete_list(list_id):
    """Delete a draft list"""
    user = current_user()
    if not user:
        return jsonify(ok=False, message="Not logged in."), 401

    conn = db()
    row = conn.execute(
        "SELECT * FROM grocery_lists WHERE id=? AND user_id=?", (list_id, user["id"])
    ).fetchone()

    if not row:
        conn.close()
        return jsonify(ok=False, message="List not found."), 404

    if row["list_type"] != "drafts":
        conn.close()
        return jsonify(ok=False, message="Can only delete draft lists."), 403

    conn.execute("DELETE FROM grocery_lists WHERE id=?", (list_id,))
    conn.commit()
    conn.close()

    return jsonify(ok=True, message="List deleted.")


@app.post("/api/groceries/send/<int:list_id>")
def api_send_list(list_id):
    """Send a draft list to receiver"""
    user = current_user()
    if not user:
        return jsonify(ok=False, message="Not logged in."), 401

    data = request.get_json(silent=True) or {}
    receiver_id = data.get("receiver_id")

    if not receiver_id:
        return jsonify(ok=False, message="Receiver required."), 400

    conn = db()

    row = conn.execute(
        "SELECT * FROM grocery_lists WHERE id=? AND user_id=?", (list_id, user["id"])
    ).fetchone()

    if not row:
        conn.close()
        return jsonify(ok=False, message="List not found."), 404

    sender_user = conn.execute(
        "SELECT username FROM users WHERE id=?", (user["id"],)
    ).fetchone()
    receiver_user = conn.execute(
        "SELECT username FROM users WHERE id=?", (receiver_id,)
    ).fetchone()

    if not receiver_user:
        conn.close()
        return jsonify(ok=False, message="Receiver not found."), 404

    title = row["title"]
    if " from " not in title.lower():
        title = f"{row['title']} (from {sender_user['username']})"

    conn.execute(
        """INSERT INTO grocery_lists 
           (user_id, list_type, title, items_json, status, created_at) 
           VALUES (?, ?, ?, ?, ?, ?)""",
        (
            receiver_id,
            "received",
            title,
            row["items_json"],
            "Pending",
            datetime.utcnow().isoformat(),
        ),
    )
    conn.commit()

    conn.execute(
        "UPDATE grocery_lists SET list_type=?, receiver_id=? WHERE id=?",
        ("sent", receiver_id, list_id),
    )
    conn.commit()
    conn.close()

    return jsonify(ok=True, message="List sent successfully!")


@app.post("/api/groceries/mark-done/<int:list_id>")
def api_mark_done(list_id):
    """Receiver marks list as done with checked items and prices"""
    user = current_user()
    if not user:
        return jsonify(ok=False, message="Not logged in."), 401

    data = request.get_json(silent=True) or {}
    checked_items = data.get("checked_items") or []

    conn = db()
    row = conn.execute(
        "SELECT * FROM grocery_lists WHERE id=? AND user_id=? AND list_type=?",
        (list_id, user["id"], "received"),
    ).fetchone()

    if not row:
        conn.close()
        return jsonify(ok=False, message="List not found or not authorized."), 404

    conn.execute("UPDATE grocery_lists SET status=? WHERE id=?", ("Done", list_id))
    conn.commit()

    items_data = json.loads(row["items_json"])
    for item in items_data:
        for checked in checked_items:
            if checked["name"].lower() == item["name"].lower():
                item["price"] = checked.get("price", 0)
                item["checked"] = checked.get("checked", False)
                break
        if "checked" not in item:
            item["checked"] = False

    conn.execute(
        "UPDATE grocery_lists SET items_json=? WHERE id=?",
        (json.dumps(items_data), list_id),
    )
    conn.commit()

    csv_dir = "groceries_data"
    os.makedirs(csv_dir, exist_ok=True)

    csv_filename = f"{csv_dir}/list_{list_id}_{user['username']}.csv"
    with open(csv_filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["Item Name", "Quantity", "Unit", "Price", "Status", "Receiver", "Date"]
        )

        for item in items_data:
            status = "Collected" if item.get("checked") else "Not Available"
            price = item.get("price", "")
            writer.writerow(
                [
                    item["name"],
                    item["qty"],
                    item["unit"],
                    price,
                    status,
                    user["username"],
                    datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                ]
            )

    conn.close()

    return jsonify(ok=True, message="List marked as done! CSV saved.")


@app.route("/api/feedback", methods=["POST"])
def submit_feedback():
    """Handle feedback submissions - SAVE TO CSV"""
    try:
        data = request.json

        # Validate required fields
        if not data.get("email"):
            return jsonify(ok=False, message="Email is required"), 400
        if not data.get("rating"):
            return jsonify(ok=False, message="Rating is required"), 400
        if not data.get("type"):
            return jsonify(ok=False, message="Feedback type is required"), 400
        if not data.get("message"):
            return jsonify(ok=False, message="Message is required"), 400

        # Initialize CSV file
        feedback_file = init_feedback_csv()

        # Get user ID if logged in
        user_id = session.get("user_id") or ""

        # Convert improvements list to JSON string
        improvements_str = json.dumps(data.get("improvements", []))

        # Get next ID
        next_id = 1
        try:
            with open(feedback_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                if len(lines) > 1:
                    next_id = int(lines[-1].split(",")[0]) + 1
        except:
            next_id = 1

        # Append to CSV file
        with open(feedback_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    next_id,
                    data.get("email"),
                    data.get("rating"),
                    improvements_str,
                    data.get("type"),
                    data.get("message"),
                    user_id,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ]
            )

        return (
            jsonify(
                ok=True,
                message="Thank you for your feedback! 💬 We appreciate your input and will use it to improve the app. Your feedback has been saved successfully! ✅",
            ),
            200,
        )

    except Exception as e:
        print(f"Feedback error: {e}")
        return jsonify(ok=False, message=f"Failed to save feedback"), 500


if __name__ == "__main__":
    app.run(debug=True)
