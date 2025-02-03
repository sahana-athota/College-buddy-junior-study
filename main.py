from flask import *
app = Flask(__name__)
app.secret_key = '123'
from db_structure import *
#from theclass import functionsudneed
from datetime import datetime

@app.route('/')
def startpage():
      return render_template("index.html")

@app.route('/rural', methods=["POST", "GET"])
def rural():

    if request.method == 'POST':
        schoolid = request.form['schoolid']
        password = request.form['password']
        f = open('data.txt','w')
        f.write(schoolid)
        f.close()
        session['schoolid'] = schoolid
        session['password'] = password
        from theclass import functionsudneed
        if functionsudneed.isschoolauth(schoolid,password):
            return redirect(url_for("schoolpage"))
        else:
            return "<html><body><h1>Authentication failed invalid credentials</h1></body></html>"


    else:
        return render_template("rural.html")

@app.route('/schoolpage')
def schoolpage():
    f = open('data.txt','r')
    a = f.readline()
    f.close()
    sid = usr_to_id_scho(a)
    details = all_courses(sid)
    f = open('data.txt','r')
    a = f.readline()
    f.close()

    enrolled = my_courses(usr_to_id_scho(a))

    live = "True"
    return render_template("schoolpage.html",details = details, enrolled = enrolled,live = live)

@app.route('/mycourse/<courseid>')
def mycourse(courseid):

    '''
    ideally pass courseid through a function and get necessary details and pass to flask
    '''
    coursedetails = (particular_crs(int(courseid)),)
    return render_template("coursedetails.html",coursedetails = coursedetails)

@app.route('/courseview/<courseid>', methods=["POST", "GET"])
def courseview(courseid):
    if request.method == 'POST':
        cid = int(courseid)
        f = open('data.txt','r')
        a = f.readline()
        f.close()
        t = usr_to_id_scho(a)
        update_courses(cid,t)
        return redirect(url_for("schoolpage"))


    else:
        coursedetails = (particular_crs(int(courseid)),)
        return render_template("courseview.html",coursedetails = coursedetails)




@app.route('/urban')
def urban():
    return render_template("urbanpage.html")

@app.route('/login', methods=["POST", "GET"])
def login():

    if request.method == 'POST':
        tutorid = request.form['tutorid']
        password = request.form['password']
        session['tutorid'] = tutorid
        session['password'] = password
        f = open("data.txt",'w')
        f.write(tutorid)
        f.close()
        if functionsudneed.istutorauth(tutorid,password):
            return redirect(url_for("studentportal"))
        else:
            return "<html><body><h1>Authentication failed invalid credentials</h1></body></html>"
    else:
        return render_template("urbanlogin.html")

@app.route('/studentportal')
def studentportal():
    f = open('data.txt', 'r')
    a = f.readline()
    f.close()
    tid = usr_to_id(a)
    mycourse = crs_of_stu(tid)
    return render_template("studentportal.html",mycourse = mycourse)

@app.route('/createcourse', methods=["POST", "GET"])
def createcourse():
    if request.method == 'POST':
        title = request.form['title']
        descone = request.form['descone']
        descmulti = request.form['descmulti']
        daysweek = request.form['daysweek']
        start = request.form['start']
        durationhrs = request.form['durationhrs']
        date = request.form['date']
        durationmonths = request.form['durationmonths']
        f = open('data.txt', 'r')
        a = f.readline()
        f.close()
        tid = usr_to_id(a)
        insert_courses(tid,title,descone,descmulti,daysweek,start,durationhrs,date,durationmonths)
        return redirect(url_for("studentportal"))

    return render_template("createcourse.html")

@app.route('/register', methods=["POST", "GET"])
def urban_register():
    if request.method == 'POST':
        name = request.form['name']
        tutorusername = request.form['tutorid']
        password = request.form['password']
        bio = request.form['bio']
        tutorid = tutorusername+'1'
        insert_students(tutorid,name,tutorusername,password,bio)
        return redirect(url_for("login"))

    return render_template("urbanregister.html")



if __name__ == '__main__':
   app.run(debug = True)