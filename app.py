from flask import Flask, url_for, request, session, g
from flask.templating import render_template
from werkzeug.utils import redirect
from database import get_database
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.teardown_appcontext
def close_database(error):
    if hasattr(g, 'crudapplication_db'):
        g.crudapplication_db.close()

def get_current_user():
    user = None
    if 'user' in session:
        user = session['user']
        db = get_database()
        user_cur = db.execute('select * from users where name = ?', [user])
        user = user_cur.fetchone()
    return user

@app.route('/')
@app.route('/home')
def index():
    user = get_current_user()
    return render_template('home.html', user = user)


@app.route('/login', methods = ["POST", "GET"])
def login():
    user = get_current_user()
    error = None
    db = get_database()
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user_cursor = db.execute('select * from users where name = ?', [name])
        user = user_cursor.fetchone()
        if user:
            if check_password_hash(user['password'], password):
                session['user'] = user['name']
                return redirect(url_for('dashboard'))
            else:
                error = "Username or Password did not match, Try again."
        else:
            error = 'Username or password did not match, Try again.'
    return render_template('login.html', loginerror = error, user = user)


@app.route('/register', methods=["POST", "GET"])
def register():
    user = get_current_user()
    db = get_database()
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        dbuser_cur = db.execute('select * from users where name = ?', [name])
        existing_username = dbuser_cur.fetchone()
        if existing_username:
            return render_template('register.html', registererror = 'Username already taken , try different username.')
        db.execute('insert into users ( name, password) values (?, ?)',[name, hashed_password])
        db.commit()
        return redirect(url_for('login'))
    return render_template('register.html', user = user)


@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    db = get_database()
    emp_cur = db.execute('select * from emp')
    allemp = emp_cur.fetchall()
    return render_template('dashboard.html', user = user, allemp = allemp)


@app.route('/addnewemployee', methods = ["POST", "GET"])
def addnewemployee():
    user = get_current_user()
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        db = get_database()
        db.execute('insert into emp (name, email, phone ,address) values (?,?,?,?)', [name, email, phone, address])
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('addnewemployee.html', user = user)


@app.route('/singleemployee/<int:empid>')
def singleemployee(empid):
    user = get_current_user()
    db = get_database()
    emp_cur = db.execute('select * from emp where empid = ?', [empid])
    single_emp = emp_cur.fetchone()
    return render_template('singleemployee.html', user = user, single_emp = single_emp)


@app.route('/fetchone/<int:empid>')
def fetchone(empid):
    user = get_current_user()
    db = get_database()
    emp_cur = db.execute('select * from emp where empid = ?', [empid])
    single_emp = emp_cur.fetchone()
    return render_template('updateemployee.html', user = user, single_emp = single_emp)


@app.route('/updateemployee' , methods = ["POST", "GET"])
def updateemployee():
    user = get_current_user()
    if request.method == 'POST':
        empid = request.form['empid']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        db = get_database()
        db.execute('update emp set name = ?, email =? , phone = ? , address = ? where empid = ?', [name, email, phone, address, empid])
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('updateemployee.html', user = user)


@app.route('/deleteemp/<int:empid>', methods = ["GET", "POST"])
def deleteemp(empid):
    user = get_current_user()
    if request.method == 'GET':
        db = get_database()
        db.execute('delete from emp where empid = ?', [empid])
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html', user = user)


@app.route('/addnewtestcase', methods = ["POST", "GET"])
def addnewtestcase():
    user = get_current_user()
    if request.method == "POST":
        testcasename = request.form['testcasename']
        requirementnumber = request.form['requirementnumber']
        modulename = request.form['modulename']
        buildnumber = request.form['buildnumber']
        precondition = request.form['precondition']
        testdata = request.form['testdata']
        postcondition = request.form['postcondition']
        severity = request.form['severity']
        testcasetype = request.form['testcasetype']
        briefdescription = request.form['briefdescription']
        textcaseexecutionhours = request.form['textcaseexecutionhours']
        stepnumber1 = request.form['stepnumber1']
        action1 = request.form['action1']
        testdata1 = request.form['testdata1']
        expectedresult1 = request.form['expectedresult1']
        actualresult1 = request.form['actualresult1']
        status1 = request.form['status1']
        remark1 = request.form['remark1']
        stepnumber2 = request.form['stepnumber2']
        action2 = request.form['action2']
        testdata2 = request.form['testdata2']
        expectedresult2 = request.form['expectedresult2']
        actualresult2 = request.form['actualresult2']
        status2 = request.form['status2']
        remark2 = request.form['remark2']
        stepnumber3 = request.form['stepnumber3']
        action3 = request.form['action3']
        testdata3 = request.form['testdata3']
        expectedresult3 = request.form['expectedresult3']
        actualresult3 = request.form['actualresult3']
        status3 = request.form['status3']
        remark3 = request.form['remark3']
        stepnumber4 = request.form['stepnumber4']
        action4 = request.form['action4']
        testdata4 = request.form['testdata4']
        expectedresult4 = request.form['expectedresult4']
        actualresult4 = request.form['actualresult4']
        status4 = request.form['status4']
        remark4 = request.form['remark4']
        stepnumber5 = request.form['stepnumber5']
        action5 = request.form['action5']
        testdata5 = request.form['testdata5']
        expectedresult5 = request.form['expectedresult5']
        actualresult5 = request.form['actualresult5']
        status5 = request.form['status5']
        remark5 = request.form['remark5']
        stepnumber6 = request.form['stepnumber6']
        action6 = request.form['action6']
        testdata6 = request.form['testdata6']
        expectedresult6 = request.form['expectedresult6']
        actualresult6 = request.form['actualresult6']
        status6 = request.form['status6']
        remark6 = request.form['remark6']
        authorname = request.form['authorname']
        reviewedby = request.form['reviewedby']
        approvedby = request.form['approvedby']
        approvaldate = request.form['approvaldate']
        db = get_database()
        db.execute('insert into testcase (testcasename, requirementnumber,modulename, buildnumber, precondition, testdata, postcondition, severity, testcasetype, briefdescription,textcaseexecutionhours,stepnumber1, action1, testdata1, expectedresult1, actualresult1, status1, remark1,stepnumber2, action2, testdata2, expectedresult2, actualresult2, status2, remark2,stepnumber3, action3, testdata3, expectedresult3, actualresult3, status3, remark3,stepnumber4, action4, testdata4, expectedresult4, actualresult4, status4, remark4,  authorname, reviewedby, approvedby, approvaldate ) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', [testcasename, requirementnumber,modulename, buildnumber, precondition, testdata, postcondition, severity, testcasetype, briefdescription,textcaseexecutionhours, stepnumber1, action1, testdata1, expectedresult1, actualresult1, status1, remark1,stepnumber2, action2, testdata2, expectedresult2, actualresult2, status2, remark2, stepnumber3, action3, testdata3, expectedresult3, actualresult3, status3, remark3, stepnumber4, action4, testdata4, expectedresult4, actualresult4, status4, remark4,stepnumber4, action4, testdata4, expectedresult4, actualresult4, status4, remark4, status4, remark4,stepnumber5, action5, testdata5, expectedresult5, actualresult5, status5, remark5,status4, remark4,stepnumber6, action6, testdata6, expectedresult6, actualresult6, status6, remark6, authorname, reviewedby, approvedby, approvaldate ])
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('addnewtestcase.html', user = user)


@app.route("/dropdown")
def dropdown():
    user = get_current_user()
    return render_template("dropdown.html")


@app.route("/alerts")
def alerts():
    user = get_current_user()
    return render_template("alerts.html")


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug = True)