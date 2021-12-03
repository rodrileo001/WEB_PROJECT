from flask import Flask, render_template, request,  flash, redirect, url_for, session, json, jsonify
from flask_mysqldb import MySQL
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta  # Used to set session time, perm



# Create Flask APP
def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'kfdsjahfkdjsh dkjsahfksld'

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'KodaBlue1!'
    app.config['MYSQL_DB'] = 'task'
    # converts from string to dictionary
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    # set session life time
    app.permanent_session_lifetime = timedelta(minutes=15)

    return app


# Instance of Flask APP
app = create_app()

# Instance of MySQL DB
mysql = MySQL(app)


# Create MySQL DB in MySQL server


# ------ ROUTES
#   Index
@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')


#   Login

@app.route('/login', methods=['GET', 'POST'])
def login():
    # data = request.form
    # print(data)
    if request.method == 'POST':
        # Open Connection
        cur = mysql.connection.cursor()

        # Get data input in form
        email = request.form.get('email')
        password = request.form.get('password')
        # Get saved data in DB to match with
        select_stmt = """SELECT email, password FROM user WHERE email = %(email)s AND password = %(password)s """
        cur.execute(select_stmt, {'email': email, 'password': password})
        user = cur.fetchall()

        if user:
            if user[0]['password'] == password:

                # Define THIS session as permanent defined above
                session.permanent = True
                session['user'] = user
                return redirect(url_for('home'))
            else:
                flash("Incorrect password, try again.", category='error')
        else:
            flash("User Not Found.", category='error')
            return render_template('login.html')

        # Close the db connection
        cur.close()

    if request.method == 'GET':
        if "user" in session:
            return redirect(url_for('home'))

    return render_template('login.html')


#   Sign Up

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':

        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        role = request.form.get('role')
        # print(role)

        password_hash = generate_password_hash(password1, method='sha256')
        user_data = (email, password1, first_name, role)

        # Open Connection
        cur = mysql.connection.cursor()
        select_stmt = """SELECT email FROM user WHERE email = %(email)s """
        cur.execute(select_stmt, {'email': email})
        user = cur.fetchall()
        # Close the cursor connection

        if user:
            flash("User already exists", category='error')
        elif len(email) <= 4:
            flash("Email must be greater than 4 characters.", category='error')
        elif len(first_name) <= 2:
            flash("First name must be greater than 2 characters.", category='error')
        elif role == '':
            flash("Please select a user role.", category='error')
        elif password1 != password2:
            flash("Passwords don\'t match", category='error')
        elif len(password1) < 7:
            flash("Password must be at least 7 characters.", category='error')
        else:
            # add user to DB
            cur.execute('''INSERT INTO user VALUES (%s, %s, %s, %s)''', user_data)
            mysql.connection.commit()
            cur.close()
            flash("Account created!", category='success')
            return redirect(url_for('login'))

    return render_template('sign_up.html')


#   Logout

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('login'))



#   Home

@app.route('/home', methods=['GET', "POST"])
def home():
    if "user" in session:
        if request.method == 'GET':
            # Open Connection
            cur = mysql.connection.cursor()

            # snapshot user object
            user = session['user']
            # print(session)
            # print(user)
            # parse user name from user object
            user_name = user[0]['email']
            # print(user_name)

            # get user role from DB
            select_role = """SELECT role FROM user WHERE email = %(user_name)s """
            cur.execute(select_role, {'user_name': user_name})
            role_obj = cur.fetchall()
            user_role = role_obj[0]['role']
            # print(user_role)

            # get firstname of user from user db
            select_first_name = """SELECT first_name FROM user WHERE email = %(user_name)s """
            cur.execute(select_first_name, {'user_name': user_name})
            first_name_obj = cur.fetchall()
            first_name = first_name_obj[0]['first_name']
            # print(first_name)

            if user_role == 'User':
                # get list of open tasks for user
                select_open_task_list = """SELECT task_num, task, status, description FROM task WHERE assigned_to = %(first_name)s AND status != 'Closed' """
                cur.execute(select_open_task_list, {'first_name': first_name})
                open_task_list = cur.fetchall()
                # print(task_list)

                # get list of closed tasks for user
                select_closed_task_list = """SELECT task_num, task, status, description FROM task WHERE assigned_to = %(first_name)s AND status = 'Closed' """
                cur.execute(select_closed_task_list, {'first_name': first_name})
                closed_task_list = cur.fetchall()
                # print(task_list)

                return render_template('home.html', first_name=first_name, open_task_list=open_task_list, closed_task_list=closed_task_list)

            if user_role == "Boss":
                return redirect(url_for('boss'))

    return render_template("login.html")


#   Task Page

@app.route('/task', methods=['GET', 'POST'])
def task():
    if "user" in session:
        #     if request.method == 'GET':
        # Open Connection
        cur = mysql.connection.cursor()

        # snapshot user object
        user = session['user']
        # print(user)
        # parse user name from user object
        user_name = user[0]['email']
        # print(user_name)

        # get role of user from user db
        select_role = """SELECT role FROM user WHERE email = %(user_name)s """
        cur.execute(select_role, {'user_name': user_name})
        role_obj = cur.fetchall()
        role = role_obj[0]['role']
        # print(role)

        # get firstname of user from user db
        select_first_name = """SELECT first_name FROM user WHERE email = %(user_name)s """
        cur.execute(select_first_name, {'user_name': user_name})
        first_name_obj = cur.fetchall()
        first_name = first_name_obj[0]['first_name']
        # print(first_name)

        # Get Task Number from form body
        # task_number = request.form.get('taskNum')
        task_number = request.args['taskNum']
        print(task_number)
        # print(task_number)

        # get task detail of task from task table
        select_task = """SELECT status, priority, start_date, assigned_to, target_date, description, task FROM task WHERE task_num = %(tempTaskNum)s """
        cur.execute(select_task, {'tempTaskNum': task_number})
        task_detail = cur.fetchall()
        # print(task_detail)

        # Get Comments associated to task selected
        select_comments_query = """SELECT comment, assigned_to FROM comments WHERE task_num = %(task_number)s """
        cur.execute(select_comments_query, {'task_number': task_number})
        comment_list = cur.fetchall()
        # print(comment_list)

        # Get List of users
        select_user_list = """SELECT first_name FROM user """
        cur.execute(select_user_list)
        user_list = cur.fetchall()
        # print(user_list)

        cur.close()

        task_status = task_detail[0]['status']
        task_priority = task_detail[0]['priority']
        task_start_date = task_detail[0]['start_date']
        task_assigned_to = task_detail[0]['assigned_to']
        task_target_date = task_detail[0]['target_date']
        task_description = task_detail[0]['description']
        task_label = task_detail[0]['task']
        # print(task_status)
        # return redirect(url_for('task'))

        return render_template("task.html", task_status=task_status,
                               task_priority=task_priority,
                               task_start_date=task_start_date,
                               task_assigned_to=task_assigned_to,
                               task_target_date=task_target_date,
                               task_description=task_description,
                               comment_list=comment_list,
                               task_label=task_label,
                               task_number=task_number,
                               user_list=user_list)
    return render_template("login.html")


#   Add Comment

@app.route('/add_comment', methods=['GET', "POST"])
def addComment():
    if "user" in session:
        if request.method == 'POST':
            comment_data = request.form
            # print(comment_data.get('newCommentText'))
            # print(comment_data.get('task_number'))
            comment = comment_data.get('newCommentText')
            task_number = comment_data.get('task_number')

            # snapshot user object
            user = session['user']
            # print(user)
            # parse user name from user object
            user_name = user[0]['email']
            # print(user_name)

            # Open Connection
            cur = mysql.connection.cursor()

            # get firstname of user from user db
            select_first_name = """SELECT first_name FROM user WHERE email = %(user_name)s """
            cur.execute(select_first_name, {'user_name': user_name})
            first_name_obj = cur.fetchall()
            first_name = first_name_obj[0]['first_name']
            # print(first_name)

            # Insert comment with user first name and task number into comments table
            search_data = (first_name, comment, task_number)
            cur.execute('''INSERT INTO comments VALUES (%s, %s, %s)''', search_data)
            mysql.connection.commit()
            # Close the cursor connection
            cur.close()

            return redirect(url_for('task', taskNum=task_number))

    # return redirect(url_for('task'))

#   Remove Comment

@app.route('/remove_comment', methods=['GET', "POST"])
def removeComment():
    if "user" in session:
        if request.method == 'POST':

            # snapshot user object
            user = session['user']
            # print(user)
            # parse user name from user object
            user_name = user[0]['email']
            # print(user_name)

            # Open Connection
            cur = mysql.connection.cursor()

            # get firstname of user from user db
            select_first_name = """SELECT first_name FROM user WHERE email = %(user_name)s """
            cur.execute(select_first_name, {'user_name': user_name})
            first_name_obj = cur.fetchall()
            first_name = first_name_obj[0]['first_name']
            # print(first_name)

            # Get Comment text and Task number to remove from comments table
            comment_text = request.form.get("commentText")
            # print(comment_text)
            task_num = request.form.get('commentTaskNum')
            # print(task_num)

            # Remove comment from comments table assoicated to task number
            remove_comment_query = """DELETE FROM comments  WHERE assigned_to = %(first_name)s AND comment = %(comment)s AND task_num = %(task_num)s """
            cur.execute(remove_comment_query, {'first_name': first_name, "comment": comment_text, "task_num": task_num})
            mysql.connection.commit()
            cur.close()

            return redirect(url_for('task', taskNum=task_num))


#   Create New Task

@app.route('/new_task', methods=['GET', "POST"])
def newTask():
    if "user" in session:

        if request.method == 'POST':
            # temp = request.form
            # print(temp)

            # Open Connection
            cur = mysql.connection.cursor()


            # Verify input for Titel, Description, Start Date, Status, and Priority
            if request.form.get("task_label") == '':
                flash("Please enter a Title", category='error')
            elif request.form.get("task_desc") == '':
                flash("Please enter a Description", category='error')
            elif request.form.get("task_start") == '':
                flash("Please enter a Start Date", category='error')
            elif request.form.get("task_status") == '':
                flash("Please enter a Status", category='error')
            elif request.form.get("task_priority") == '':
                flash("Please enter a Priority", category='error')
            else:
                task_label = request.form.get("task_label")
                task_desc = request.form.get("task_desc")
                task_start = request.form.get("task_start")
                task_status = request.form.get("task_status")
                task_target = request.form.get("task_target")
                task_priority = request.form.get("task_priority")
                task_assigned = request.form.get("task_assigned")
                first_name = request.form.get("user_assigned")


                # Check box on task screen, will assign to current user creating the task when checked
                if task_assigned == 'on':
                    # snapshot user object
                    user = session['user']
                    # print(user)

                    # parse user name from user object
                    user_name = user[0]['email']
                    # print(user_name)
                    # get firstname of user from user db
                    select_first_name = """SELECT first_name FROM user WHERE email = %(user_name)s """
                    cur.execute(select_first_name, {'user_name': user_name})
                    first_name_obj = cur.fetchall()
                    first_name = first_name_obj[0]['first_name']
                    # print(first_name)


                # Get Max task number, add one to it for next added task
                select_highest_task_num = """SELECT MAX(DISTINCT task_num) as maxNum FROM task"""
                cur.execute(select_highest_task_num)
                max_task_obj = cur.fetchall()
                max_task = max_task_obj[0]['maxNum']
                # print(max_task)

                # Set Next incremental Task Number
                task_num = max_task + 1

                task_data = (task_num, task_label, task_status, task_priority, task_start, task_target, first_name, task_desc)
                cur.execute('''INSERT INTO task VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', task_data)
                mysql.connection.commit()

                # Close the cursor connection
                cur.close()

                return redirect(url_for('home'))

    # Open Connection
    cur = mysql.connection.cursor()

    # Get List of users
    select_user_list_new_task = """SELECT first_name FROM user """
    cur.execute(select_user_list_new_task)
    user_list_new_task = cur.fetchall()
    # print(user_list)
    cur.close()

    return render_template("new_task.html", user_list_new_task=user_list_new_task)


#   Boss Page

@app.route('/boss', methods=['GET', "POST"])
def boss():
    if "user" in session:
        if request.method == 'GET':
            # Open Connection
            cur = mysql.connection.cursor()

            # snapshot user object
            user = session['user']
            # print(user)
            # parse user name from user object
            user_name = user[0]['email']
            # print(user_name)
            # get firstname of user from user db
            select_first_name = """SELECT first_name FROM user WHERE email = %(user_name)s """
            cur.execute(select_first_name, {'user_name': user_name})
            first_name_obj = cur.fetchall()
            first_name = first_name_obj[0]['first_name']
            # print(first_name)

            # Get number of tasks per user
            select_user_count_query = """SELECT assigned_to, count(assigned_to) as count FROM task 
                WHERE assigned_to != '' AND status != 'Closed' GROUP BY assigned_to ORDER BY count(assigned_to) desc """
            cur.execute(select_user_count_query)
            user_count = cur.fetchall()
            # print(user_count)

            # Get number of unassigned Tasks
            select_unassigned_count_query = """SELECT assigned_to, count(assigned_to) as count FROM task 
                            WHERE assigned_to = '' GROUP BY assigned_to ORDER BY count(assigned_to) desc """
            cur.execute(select_unassigned_count_query)
            unassigned_count = cur.fetchall()
            # print(user_count)

            # Get number of task per each Priority
            select_priority_count_query = """SELECT priority, count(priority) as count FROM task WHERE status NOT IN ("Closed", "")
                                        GROUP BY priority ORDER BY count(priority) desc """
            cur.execute(select_priority_count_query)
            priority_count = cur.fetchall()
            # print(priority_count)

            # get list of open assigned tasks from task db
            user_assigned_task_list = """SELECT task_num, task, status, description, assigned_to FROM task WHERE assigned_to != '' AND status != 'Closed'  """
            cur.execute(user_assigned_task_list, {'first_name': first_name})
            task_list = cur.fetchall()
            # print(task_list)

            # get task list of open unassigned tasks from task db
            user_not_assigned_task_list = """SELECT task_num, task, status, description, assigned_to FROM task WHERE assigned_to = '' AND status != 'Closed'  """
            cur.execute(user_not_assigned_task_list, {'first_name': first_name})
            unassigned_task_list = cur.fetchall()
            # print(unassigned_task_list)

            # get task list of closed tasks from task db
            user_closed_task_list = """SELECT task_num, task, status, description, assigned_to FROM task WHERE status = 'Closed'  """
            cur.execute(user_closed_task_list, {'first_name': first_name})
            closed_task_list = cur.fetchall()
            # print(unassigned_task_list)

            cur.close()

            return render_template('boss.html', first_name=first_name,
                                   task_list=task_list,
                                   unassigned_task_list=unassigned_task_list,
                                   user_count=user_count,
                                   unassigned_count=unassigned_count,
                                   priority_count=priority_count,
                                   closed_task_list=closed_task_list)

    return render_template("login.html")


#   Update Task

@app.route('/update_task', methods=['GET', "POST"])
def updateTask():
    if "user" in session:
        if request.method == 'POST':
            # temp = request.form
            # print(temp)

            task_new_target = request.form.get("target_change")
            task_new_status = request.form.get("status_change")
            task_new_priority = request.form.get("priority_change")
            task_new_assigned = request.form.get("user_change")
            task_num = request.form.get("updateTaskNum")

            # Open Connection
            cur = mysql.connection.cursor()

            # Update task table with new details
            update_statement = """  UPDATE task SET target_date = %s, status = %s, priority  = %s, assigned_to = %s WHERE task_num = %s """
            values = (task_new_target, task_new_status, task_new_priority, task_new_assigned, task_num)
            cur.execute(update_statement, values)
            mysql.connection.commit()

            cur.close()
            # return '200'
            return redirect(url_for('home'))

    return render_template("task.html")




if __name__ == '__main__':
    app.run(debug=True)
