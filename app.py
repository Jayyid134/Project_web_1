from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="user_db"
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def index():
    cursor.execute("SELECT * FROM users")  # Fetch all users
    users = cursor.fetchall()  # Store in 'users'
    return render_template('index.html', users=users)  # Pass to HTML

@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']

    cursor.execute("INSERT INTO users (name, email, age) VALUES (%s, %s, %s)", (name, email, age))
    db.commit()
    return redirect('/')


@app.route('/edit/<int:id>', methods=['GET', 'PUT'])
def edit_user(id):
    # Fetch user data from the database
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()

    if request.method == 'PUT':
        # Get updated form data
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']

        # Update the database with new values
        cursor.execute("UPDATE users SET name=%s, email=%s, age=%s WHERE id=%s", (name, email, age, id))
        db.commit()

        return redirect('/')  # Redirect back to homepage

    return render_template('edit.html', user=user)  # Render edit form


@app.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    cursor.execute("DELETE FROM users WHERE id=%s", (id,))
    db.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)