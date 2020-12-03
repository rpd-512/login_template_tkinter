from tkinter import *
import csv
import re
import sqlite3
import config
import os
import hashlib
from time import sleep

dbLoc = "database.db" #location of the database file
conn = sqlite3.connect(dbLoc)
try:
    conn.execute("""
    create table userData(
        usid integer PRIMARY KEY AUTOINCREMENT NOT NULL,
        name TEXT,
        usnm TEXT,
        pswd TEXT,
        mail TEXT
    );
    """)
except:
    pass

def main():
    global root
    global uent,pent,uimg,pimg, logoimg, uname, passw,logo, usname, passwd,sub,log, subm

    root.title('SignIn')
    try:
        signup_clear()
    except:
        pass

    logo = PhotoImage(file = 'images/logo.png')
    logo = logo.subsample(7,7)
    logoimg = Label(root,image=logo)
    logoimg.place(x=210,y=10,in_=root)

    usname = PhotoImage(file = 'images/userna.png')
    usname = usname.subsample(17, 17)
    uimg = Label(root,image=usname)
    uimg.place(x=40, y=87, in_=root)

    passwd = PhotoImage(file = 'images/passwd.png')
    passwd = passwd.subsample(17, 17)
    pimg = Label(root,image=passwd)
    pimg.place(x=40, y=117, in_=root)

    uent = Entry(root,width=25)
    pent = Entry(root,show="*",width=25)


    uname = Label(root,text='username')
    uname.config(font=('Times',15,'bold'))
    passw = Label(root,text='password')
    passw.config(font=('Times',15,'bold'))
    uname.place(x=75,y=90,in_=root)
    passw.place(x=75,y=120,in_=root)

    uent.place(x=175,y=90,in_=root)
    uent.focus_set()
    pent.place(x=175,y=120,in_=root)

    sub = Button(root,text = "submit",command=search,background='black',foreground='white')
    sub.config(font=("",15,"bold"))
    sub.place(x=175,y=185,in_=root)

    login_d = """Don't have an account,
    sign up now!"""

    log = Button(root,text = login_d,command=signup,background='black',foreground='white')
    log.config(font=("",7,"bold"))
    log.place(x=300,y=185,in_=root)

def check_mail(mail_id):
    if(len(re.findall(r"\w+@+\w+\.+\w+",mail_id))==0):
        return False
    return True

def signin_clear():
    global wrpas
    sub.destroy()
    uent.destroy()
    pent.destroy()
    uimg.destroy()
    pimg.destroy()
    logoimg.destroy()
    uname.destroy()
    passw.destroy()
    log.destroy()
    try:
        wrpas.destroy()
    except:
        pass

def signup_clear():
    global wrpas,login_un, login_pa, login_em, login_cp,login_na,na_ent, un_ent,pa_ent,em_ent,cp_ent, back_but, signup_but
    logoimg.destroy()
    login_un.destroy()
    login_em.destroy()
    login_pa.destroy()
    login_cp.destroy()
    login_na.destroy()
    un_ent.destroy()
    em_ent.destroy()
    cp_ent.destroy()
    pa_ent.destroy()
    na_ent.destroy()
    back_but.destroy()
    signup_but.destroy()
    wrpas.destroy()

def after_sign_in(id,name,mail,user):
    global wrpas
    signin_clear()
    warn(" ","green")
    y_cor = 50
    lis = ["Welcome "+user,"Your name: "+name,"Your email id: "+mail]
    for data in lis:
        wrpas = Label(root,text=data,foreground="black")
        wrpas.config(font=('',15,"bold"))
        wrpas.place(x=25,y=y_cor,in_=root)
        y_cor+=50
    print("userid:",id)
            

def search():
    global wrpas
    ch=True
    user = uent.get()#username
    pasd = pent.get()#password
    cursor = conn.execute("select * from userData where usnm = '"+user+"'")
    for i in cursor:
        ch = False
        hash_pswd = (hashlib.md5((pasd+"314159265358979323846264338327").encode())).hexdigest()
        if(hash_pswd == i[3]):
            after_sign_in(i[0],i[1], i[4], i[2])#good sign in
            return 0
        else:
            wrpas = Label(root,text='wrong password',foreground='red')#bad sign in
            wrpas.config(font=('Times',10))#bad sign in
            wrpas.place(x=75,y=200,in_=root)#bad sign in
    if(ch):
        wrpas = Label(root,text='not found             ',foreground='red')
        wrpas.config(font=('Times',10))
        wrpas.place(x=75,y=200,in_=root)
                

def warn(string,col):
    global wrpas
    string += " "*500
    wrpas = Label(root,text=string,foreground=col)
    wrpas.config(font=('Times',10))
    wrpas.place(x=75,y=225,in_=root)
        
def taken_check(user,mail_id):
    ch = 0
    cur_user = conn.execute("select * from userData where usnm = '"+user+"'")
    cur_mail = conn.execute("select * from userData where mail = '"+mail_id+"'")
    for i in cur_user:
        if(str(i[2].lower()) == str(user.lower().replace(" ",""))):
            ch = 1
    for i in cur_mail:
        if(i[4].lower() == mail_id.lower().replace(" ","")):
            ch = 2
    return ch
            
def write_db(list_data):
    hash_pswd = (hashlib.md5((str(list_data[2])+"314159265358979323846264338327").encode())).hexdigest()
    conn.execute("insert into userData (name,usnm,pswd,mail) values ('"+list_data[0]+"','"+list_data[1]+"','"+hash_pswd+"','"+list_data[3]+"');")
    conn.commit()
def login():
    uname_ent = un_ent.get()
    mail_ent = em_ent.get()
    pass_ent = pa_ent.get()
    conp_ent = cp_ent.get()
    name_ent = na_ent.get()
    if not check_mail(mail_ent) or " " in mail_ent:
        warn("invalid mail id             ","red")
    
    elif (taken_check(uname_ent,mail_ent)==1):
        warn("username already taken    ","red")
    
    elif (taken_check(uname_ent,mail_ent)==2):
        warn("Email id already used once","red")
                
    elif(len(pass_ent)<8):
        warn("Enter a strong password!   ","red")
    elif(uname_ent == ""):
        warn("please give us a username! ","red")
    elif(pass_ent != conp_ent):
        warn("password doesn't matches!  ","red")
    elif(name_ent == ""):
        warn("please enter a name        ","red")
    else:
        warn(uname_ent+" sign up successful","green")
        ent_list = [name_ent,uname_ent,pass_ent,mail_ent]
        print(ent_list)
        
        write_db(ent_list)
        main()
        warn("sign in was successful!","green")
    
def signup():
    global wrpas, logo, logoimg
    global login_un, login_pa, login_em, login_cp, login_na ,un_ent,na_ent,pa_ent,em_ent,cp_ent, back_but, signup_but
    root.title("Sign Up")
    warn(" ","green")
    signin_clear()
    
    logo = PhotoImage(file = 'images/logo.png')
    logo = logo.subsample(7,7)
    logoimg = Label(root,image=logo)
    logoimg.place(x=210,y=10,in_=root)

    login_un = Label(root,text='  Enter username*')
    login_em = Label(root,text='  Enter email ID*')
    login_pa = Label(root,text='  Enter password*')
    login_cp = Label(root,text='Confirm password*')
    login_na = Label(root,text='Enter Your Name*')
    
    ts = 15
    fon = "Times"
    login_un.config(font=(fon,ts,"bold"))
    login_na.config(font=(fon,ts,"bold"))
    login_em.config(font=(fon,ts,"bold"))
    login_pa.config(font=(fon,ts,"bold"))
    login_cp.config(font=(fon,ts,"bold"))
    
    login_un.place(x=70,y=70,in_=root)
    login_na.place(x=55,y=100,in_=root)
    login_em.place(x=75,y=130,in_=root)
    login_pa.place(x=70,y=160,in_=root)
    login_cp.place(x=55,y=190,in_=root)
    
    un_ent = Entry(root,width=25)
    un_ent.place(x=230,y=72,in_=root)
    
    na_ent = Entry(root,width=25)
    na_ent.place(x=230,y=102,in_=root)
    
    em_ent = Entry(root,width=25)
    em_ent.place(x=230,y=132,in_=root)

    pa_ent = Entry(root,show="*",width=25)
    pa_ent.place(x=230,y=162,in_=root)
    
    cp_ent = Entry(root,show="*",width=25)
    cp_ent.place(x=230,y=192,in_=root)

    back_but = Button(root,text='<Back<',command=main,background='black', foreground='white')
    back_but.config(font=("",12,"bold"))
    back_but.place(x=75,y=10,in_=root)

    signup_but = Button(root,text = '>Sign In>', command=login, background='black', foreground='white')
    signup_but.config(font=("",12,"bold"))
    signup_but.place(x=325,y=10,in_=root)
        
root = Tk()
root.geometry('500x250')

main()


root.mainloop()
