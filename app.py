from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL
import os
import string
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from helpers import login_required, validate_password


# Configure application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '\\static\\img\\uploads'  # Carpeta donde se guardarán las fotos de perfil


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///contacts.db")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        #Select user_id
        user_id = session["user_id"]
        #Extract contacts from database
        contacts_data = db.execute("SELECT * FROM contacts WHERE user_id = ?", user_id)
        # Convert the result into a list of dictionaries
        contacts = []
        for contact in contacts_data:
            contact_dict = {
                "id": contact["id"],
                "name": contact["name"],
                "lastname": contact["lastname"],
                "phonenumber": contact["phonenumber"],
                "email": contact ["email"],
                "address": contact["address"],
                "birthday": contact["birthday"],
            }
            contacts.append(contact_dict)
        
        return render_template("index.html", contacts = contacts)




@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    
    # Forget any user_id
    session.clear()
    
    # Username and password
    username = request.form.get("username")
    password = request.form.get("password")
    # Via POST
    if request.method == "POST":
        # Ensure user enter username
        if not username:
            return render_template("error.html")
        # Ensure user enter password
        elif not password:
            return render_template("error.html")
    
        # List of users
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
    
        # Ensure user exist and password is correct
        if len(rows) != 1 or not check_password_hash(
                rows[0]["password_hash"], password):
            return render_template("error.html")
        else:
            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]
            
            # Redirect user to index
            flash("Login successful!!", "success")
            return redirect("/")
            
    
    # Via GET
    else:
        return render_template("login.html")

    
@app.route("/signup", methods=["GET", "POST"])   
def signup():
    """Register user"""
    # Via POST
    if request.method == "POST":
        # List of users
        users = db.execute("SELECT username FROM users")  
        usernames = [user["username"] for user in users]
        
        # Forms
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
    
        # Error handling
        if not username or not password or not confirmation:
            return render_template("error.html")
        # Check if username already exists
        elif username in usernames:
            return render_template("error.html")
        # Check valid password
        elif validate_password(password) == False:
            return render_template("error.html")
        # Check if password == confirmation
        elif password != confirmation:
            return render_template("error.html")
         
        #Upload Photo
        # Carga de la foto de perfil
        uploaded_file = request.files['input-file']
        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            if filename:
                upload_folder = app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                # Guarda la foto de perfil en la carpeta 'uploads' con el nombre de usuario como nombre de archivo
                uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], username + "_" + filename))
                # Almacena la ruta del archivo en la base de datos (por ejemplo, SQLite)
                photo_src = os.path.join(app.config['UPLOAD_FOLDER'], username + "_profile-pic")
                # Guarda photo_src en la base de datos aquí
        
        
        # Log the user in
        password_hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, password_hash, photo_src) VALUES (?, ?, ?)", username, password_hash, photo_src)
        user = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = user[0]["id"]
    
        return redirect("/")
        
    # Via GET
    else:
        return render_template("signup.html")
    

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


@app.route("/favorites", methods=["GET", "POST"])
@login_required
def favorites():
    # Via GET
    if request.method == "GET":
        #Select user_id
        user_id = session["user_id"]
        #Extract contacts from database
        contacts_data = db.execute("SELECT * FROM contacts WHERE user_id = ? AND favorite = 1", user_id)
        # Convert the result into a list of dictionaries
        contacts = []
        for contact in contacts_data:
            contact_dict = {
                "id": contact["id"],
                "name": contact["name"],
                "lastname": contact["lastname"],
                "phonenumber": contact["phonenumber"],
                "email": contact ["email"],
                "address": contact["address"],
                "birthday": contact["birthday"],
            }
            contacts.append(contact_dict)
        
        return render_template("favorites.html", contacts = contacts)
    
    # Via POST
    else:
        # Get data from contact
        contact_id = request.form.get("contact_id")
        
        # Check if is already favorite
        is_favorite = db.execute("SELECT favorite FROM contacts WHERE id = ?", contact_id)[0]["favorite"]
        
        if is_favorite == 0:
            db.execute("UPDATE contacts SET favorite = ? WHERE id = ?", 1, contact_id)
        else:
            db.execute("UPDATE contacts SET favorite = ? WHERE id = ?", 0, contact_id)
        
        return redirect("/")
    
@app.route("/new_contact", methods=["GET", "POST"])
@login_required
def new_contact():
    # Via GET
    if request.method == "GET":
        return render_template("new_contact.html")
    else:
        # User id
        user_id = session["user_id"]
        
        # Contact form data
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        phonenumber = request.form.get("phonenumber")
        email = request.form.get("email")
        address = request.form.get("address")
        birthday = request.form.get("birthday")
        
        # Save in database
        db.execute("INSERT INTO contacts (user_id, name, lastname, phonenumber, email, address, birthday) VALUES (?, ?, ?, ?, ?, ?, ?)", user_id, name, lastname, phonenumber, email, address, birthday)
               
        return redirect("/")
    

@app.route("/edit_contact", methods=["GET", "POST"])
@login_required
def edit_contact():
    # Via GET
    if request.method == "GET":
        # Get data from this contact
        contact_id = request.args.get("contact_id")
        
        #Extract contact's data from database
        contacts_data = db.execute("SELECT * FROM contacts WHERE id = ?", contact_id)
        # Convert the result into a list of dictionaries
        contacts = []
        for contact in contacts_data:
            contact_dict = {
                "id": contact["id"],
                "name": contact["name"],
                "lastname": contact["lastname"],
                "phonenumber": contact["phonenumber"],
                "email": contact ["email"],
                "address": contact["address"],
                "birthday": contact["birthday"],
            }
            contacts.append(contact_dict)
        
        return render_template("edit_contact.html", contact_id = contacts[0]['id'], contact_name = contacts[0]['name'], contact_lastname = contacts[0]['lastname'],
                               contact_phonenumber = contacts[0]['phonenumber'], contact_email = contacts[0]['email'],
                               contact_address = contacts[0]['address'], contact_birthday = contacts[0]['birthday'])
    
    # Via POST    
    else:
        # Get id from this contact
        contact_id = request.form.get("contact_id")
        
        #Get new data
        name = request.form.get("name")  
        lastname = request.form.get("lastname")
        phonenumber = request.form.get("phonenumber")
        email = request.form.get("email")
        address = request.form.get("address")
        birthday = request.form.get("birthday")  
        
        # Update database
        db.execute("UPDATE contacts SET name = ?, lastname = ?, phonenumber = ?, email = ?, address = ?, birthday = ? WHERE id = ?", 
                   name, lastname, phonenumber, email, address, birthday, contact_id)   
        
        return redirect("/") 
    
    
    
@app.route("/delete_contact", methods=["POST"])
@login_required
def delete_contact():
    #Via POST
    if request.method == "POST":
        # Get data from contact
        contact_id = request.form.get("contact_id")
        # Delete contact
        db.execute("DELETE FROM contacts WHERE id = ?", contact_id)
        
        return redirect("/")