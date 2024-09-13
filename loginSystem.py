from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_mysqldb import MySQL

class PetAdoptionSystem:
    def __init__(self, name):
        self.web = Flask(name)
        self.web.secret_key = "ovuvwevwevwe/onyetenyevwe/ugwemuhwem/osas"
        self.web.config['MYSQL_HOST'] = 'localhost'
        self.web.config['MYSQL_USER'] = 'root'
        self.web.config['MYSQL_PASSWORD'] = ''
        self.web.config['MYSQL_DB'] = 'accounts_db'
        self.mysql = MySQL(self.web)
    
    def setup_route(self):
        @self.web.route("/")
        def home():
                return render_template("home.html")
            
        @self.web.route("/aboutus")
        def aboutus():
                return render_template("aboutus.html")
        
        @self.web.route("/howtoadopt")
        def howtoadopt():
            if "user" in session:
                return render_template("howtoadopt.html")
            else:
                flash("Please register or login to access this feature.")
                return redirect("/signin")
        
        @self.web.route("/adopt")
        def adopt():
            if "user" in session:
                return render_template("adopt.html")
            else:
                flash("Please register or login to access this feature.")
                return redirect("/signin")
            
        @self.web.route("/donate")
        def donate():
            if "user" in session:
                return render_template("donate.html")
            else:
                flash("Please register or login to access this feature.")
                return redirect("/signin")
            
        @self.web.route("/contactus")
        def contactus():
                return render_template("contact.html")
        
        @self.web.route("/signin", methods=["GET", "POST"])
        def signin():
            return render_template("sign_in.html")
            
        @self.web.route("/signin_process", methods=["GET", "POST"])
        def signin_process():
            if request.method == "POST":
                acc_name = request.form["fullname"]
                acc_username = request.form["username"]
                acc_password = request.form["password"]
                acc_email = request.form["email"]
                contact_no = request.form["contact_no"]
                address = request.form["address"]
                occupation = request.form["occupation"]
                civil_status = request.form["civil_status"]
                nationality = request.form["nationality"]
                cursor = self.mysql.connection.cursor()
                cursor.execute("SELECT * FROM account WHERE username = %s OR email=%s", (acc_username,acc_email))
                acc_exist = cursor.fetchone()
                if acc_exist:
                    flash("The username or email already in use. Please choose a different one!")
                    return redirect("/signin")  
                  
                cursor.execute("INSERT INTO account (fullname, username, password, email, contact_no, address, occupation, civil_status, nationality) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (acc_name, acc_username,  acc_password, acc_email, contact_no, address, occupation, civil_status, nationality))
                self.mysql.connection.commit()
                cursor.close()
                session["user"] = acc_name
                flash("Registration successful! Welcome!")
                return redirect("/")
            else:
                return render_template("sign_in.html")
            
        @self.web.route("/login")
        def login():
            return render_template("/login.html")
        
        @self.web.route("/login_process", methods=["POST", "GET"])
        def login_process():
            if request.method == "POST":
                user_textbox = request.form["namefield"]
                pass_textbox = request.form["passfield"]
                cursor = self.mysql.connection.cursor()
                cursor.execute("SELECT * FROM `account` WHERE username=%s OR email=%s", (user_textbox, user_textbox))
                account_found = cursor.fetchone()
                if account_found:
                    passwords = account_found[3]
                    if passwords == pass_textbox:
                        session["user"] = account_found[2]
                        flash("Successfully logged in!")
                        return redirect("/")
                    else:
                        flash("Incorrect password. Please try again.")
                        return redirect("/login")     
                else:
                    flash("Username or email does not exist. Please try again.")
                    return redirect("/login")
            
        @self.web.route("/logout")
        def logout():
            session.pop("user", None)
            flash("Logged out successfully!")
            return redirect("/login")
        
        @self.web.route("/display")
        def display():
            if "user" in session:
                cursor = self.mysql.connection.cursor()
                cursor.execute("SELECT * FROM account ORDER BY fullname")
                account_list = cursor.fetchall()
                cursor.close()
                return render_template("displaymem.html", user_account=account_list)
            else:
                flash("Please register or login to access this feature.")
                return redirect("/signin")

        
        @self.web.route("/update1")
        def update1():

                    cursor = self.mysql.connection.cursor()
                    cursor.execute(f"SELECT `id`, `fullname`, `username`, `password`, `email`, `contact_no`, `address`, `occupation`, `civil_status`, `nationality` FROM `account` WHERE `id` = {session['id']} ")
                    account_list = cursor.fetchall()
                    cursor.close()
                    id = account_list[0][0]
                    fullname = account_list[0][1]
                    username = account_list[0][2]
                    password = account_list[0][3]
                    email = account_list[0][4]
                    contact_no = account_list[0][5]
                    address = account_list[0][6]
                    occupation = account_list[0][7]
                    civil_status = account_list[0][8]
                    nationality = account_list[0][9]

                    return render_template("update.html", id=id,fullname=fullname,username=username,
                                           password=password,email=email,contact_no=contact_no,address=address,occupation=occupation
                                           ,civil_status=civil_status,nationality=nationality)
            
            
        
        @self.web.route("/update", methods=["GET", "POST"])
        def update():
            if request.method == "POST":
                namez = request.form["fullname"]
                username = request.form["username"]
                Id = request.form["id"]
                emailz = request.form["email"]
                new_pass = request.form["password"]
                number = request.form["contact_no"]
                address = request.form["address"]
                occupation = request.form["occupation"]
                status = request.form["civil_status"]
                nationality = request.form["nationality"]
                Action = request.form["action"]

                session['id'] = Id

                if Action == "updates":

                    return render_template("update.html", namez=namez,username = username, new_Id=Id, emailz=emailz, new_password = new_pass, number=number, address=address, occupation=occupation, status=status,nationality=nationality)

                elif Action == "deletes":
                    cursor = self.mysql.connection.cursor()
                    cursor.execute("DELETE FROM account WHERE id=%s", (Id,))
                    self.mysql.connection.commit()
                    cursor.close()
                    
                    flash("Account removed successfully!")
                    return redirect("/display")
                
        @self.web.route("/update_process", methods=["GET", "POST"])
        def update_process():
            try:
                
                if request.method == "POST":
                    new_name = request.form["new_fullname"]
                    username = request.form["new_username"]
                    n_id = request.form["id"]
                    emailz = request.form["email"]
                    number = request.form["number"]
                    address = request.form["new_address"]
                    occupation = request.form["new_occupation"]
                    status = request.form["new_status"]
                    nationality = request.form["new_nationality"]
     
                    cursor = self.mysql.connection.cursor()
                    cursor.execute("UPDATE account set `fullname` = %s, `username` = %s, `email` = %s, `contact_no` = %s, `address` = %s, `occupation` = %s, `civil_status` = %s, `nationality` = %s WHERE `id` = %s", (new_name, username, emailz, number, address, occupation, status, nationality, n_id))
                    self.mysql.connection.commit()
                    cursor.close()
                    
                    flash("Profile updated successfully!")
                    return redirect("/display")
            except:
                flash("user name or gmail is already used!")
                return redirect("/update1")
    def run(self):
        self.web.run(debug=True)
x = PetAdoptionSystem(__name__)
x.setup_route()
x.run()
