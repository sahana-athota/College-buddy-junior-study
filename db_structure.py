import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Leia23076",
  autocommit=True
)

cur=mydb.cursor()

def initialization(): #to create all tables
    cur.execute("create database nps;")
    cur.execute("use nps;")
    cur.execute("create table stu_info(id varchar(225) primary key,name varchar(225) not null, username varchar(225) not null,pwd varchar(225) not null,bio longtext not null);")
    cur.execute("create table courses_info(c_id int AUTO_INCREMENT primary key, stu_id varchar(225) , stu_name varchar(225) not null,c_title varchar(100) not null,c_brief varchar(300) not null, c_Desc longtext not null , status int default 0,scho_id_enrolled varchar(225), days_of_class varchar(100), str_time_of_class varchar(225),link longtext,duration_class int,str_date date,duration_course int, FOREIGN KEY (stu_id) REFERENCES stu_info(id));")
    cur.execute("create table sms(sms_id int AUTO_INCREMENT primary key, stu_id varchar(500) , scho_id int, from_number varchar(10), c_id int, status int default 0);")
    cur.execute("create table scho_info(id varchar(225)  primary key,name varchar(225) not null,username varchar(225) not null,pwd varchar(225) not null, number varchar(10) not null);")

def usr_to_id(username): #finding id with username
    cur.execute("use nps;")
    cur.execute(f"select id from stu_info where username='{username}';")
    o=cur.fetchall()
    o=o[0][0]
    return o

def id_to_name(id): #finding name with id
    cur.execute("use nps;")
    cur.execute(f"select name from stu_info where id='{id}';")
    o=cur.fetchall()
    o=o[0][0]
    return o

def usr_to_id_scho(username): #finding id with username
    cur.execute("use nps;")
    cur.execute(f"select id from scho_info where username='{username}';")
    o=cur.fetchall()
    o=o[0][0]
    return o


def all_stu(): #list of all students and their info
    cur.execute("use nps;")
    cur.execute("select id,name,username,pwd from stu_info;")
    o=cur.fetchall()
    return o #[(1,'abc','123','pwd'),]

def all_scho(): #list of all schools and their info
    cur.execute("use nps;")
    cur.execute("select id,name,username,pwd from scho_info;")
    o=cur.fetchall()
    return o #[(1,'abc','123','pwd'),]


def crs_of_stu(id): #list of courses taken by a particular student(tutor)
    cur.execute("use nps;")
    cur.execute(f"select c_title,c_brief,c_desc,days_of_class,str_time_of_class from courses_info where stu_id='{id}';")
    o=cur.fetchall()
    a=[]
    if o==None:
        return a
    return o


def all_courses(scho_id): #list of all courses and their info
    cur.execute("use nps;")
    cur.execute(f"select stu_name,c_title,c_id,c_brief,str_date from courses_info where scho_id_enrolled !='{scho_id}';")
    o=cur.fetchall()
    return o

def active_courses():#all ongoing classes
    cur.execute("use nps;")
    cur.execute("select c_id,stu_id,c_title,scho_id_enrolled from courses_info where status=1;")
    o=cur.fetchall()
    a=[]
    for i in o:
        cur.execute(f"select number from scho_info where id='{i[3]}';")
        b=cur.fetchall()
        a.append([i[0],i[1],i[2],b[0][0]])
    return a

def insert_students(sid,name,username,pwd,bio): #registering students
    cur.execute("use nps;")
    cur.execute(f"insert into stu_info values('{sid}','{name}','{username}','{pwd}','{bio}');")


def insert_courses(sid,c_title,c_brief,c_desc,days,str_time,dur_class,str_date,dur_course,link='abc'): #registering courses
    cur.execute("use nps;")
    name=id_to_name(sid)
    cur.execute(f"insert into courses_info values(NULL,'{sid}','{name}','{c_title}','{c_brief}','{c_desc}',0,NULL,'{days}','{str_time}','{link}',{dur_class},'{str_date}',{dur_course});")

def update_courses(cid,scho_id): #making courses active
    cur.execute("use nps;")
    cur.execute(f"update courses_info set scho_id_enrolled='{scho_id}',status=1 where c_id={cid};")


def insert_req(stu_id,scho_id,no,cid,status=0): #inserting into sms table
    cur.execute("use nps;")
    cur.execute(f"insert into sms values(NULL,'{stu_id}','{scho_id}','{no}',{cid},{status});")

def stu_req(stu_id): #requests recieved by a particular student
    cur.execute("use nps;")
    cur.execute(f"select from_number,c_id from sms where stu_id='{stu_id}';")
    o=cur.fetchall()
    b=[]
    if o==None:
        return b
    a=[]
    for i in o:
        cur.execute(f"select name from scho_info where number='{i[0]}';")
        b=cur.fetchall()
        cur.execute(f"select c_title from courses_info where c_id={i[1]}")
        c=cur.fetchall()
        a.append([c[0][0],b[0][0],i[0]])
    return a


def my_courses(sid): #all courses enrolled by a particular school
    cur.execute("use nps;")
    cur.execute(f"select stu_name,c_title,c_id,c_brief,str_date from courses_info where scho_id_enrolled='{sid}';")
    o=cur.fetchall()
    a=[]
    if o==None:
        return a
    for i in o:
        a.append(i[0])
    return o

def my_courses_stu(sid): 
    cur.execute("use nps;")
    cur.execute(f"select stu_name,c_title,c_id,c_brief,str_date from courses_info where scho_id_enrolled='{sid}';")
    o=cur.fetchall()
    a=[]
    if o==None:
        return a
    for i in o:
        a.append(i[0])
    return a


def time_set(cid): #time information for checking schedule
    cur.execute("use nps;")
    cur.execute(f"select days_of_class,str_time_of_class,str_date date,duration_course from courses_info where c_id={cid};")
    o=cur.fetchall()
    o=o[0]
    a=[[o[2],o[3]],[o[0],o[1]]]
    return a

def dis_time(cid): #duration of course
    a=time_set(cid)
    a=a[0]
    st=str(a[0])
    year=int(st[:4])
    month=0
    if int(st[5:7])+a[1]>12:
        month=0+(a[1]-(12-int(st[5:7])))
        year+=1
    else:
        month=int(st[5:7])+a[1]
    d=str(year)+'-'+str(month)+st[-3:]
    return st+' to '+d

def particular_crs(cid): #detailed desc of a course
    cur.execute("use nps;")
    cur.execute(f"select stu_name,c_brief,c_id,c_title,c_desc,str_date from courses_info where c_id={cid};")
    o=cur.fetchall()
    o=list(o[0]) 
    o=o[:-1]+[dis_time(cid)]
    return o

def acc_req(stu_id,scho_id,no,cid):
    cur.execute("use nps;")
    cur.execute(f"delete from sms where c_id={cid} and scho_id='{scho_id}'; ")
    cur.execute(f"update courses_info set scho_id_enrolled='{scho_id}',status=1 where c_id={cid};")


