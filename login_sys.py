from tkinter import *
import csv
import re

def main():
    global root
    global uent,pent,uimg,pimg, logoimg, uname, passw,logo, usname, passwd,sub,log, subm

    root.title('signin to RPD_techs')
    try:
        signup_clear()
    except:
        pass

    logo = PhotoImage(file = 'cosm.png')
    logo = logo.subsample(3,3)
    logoimg = Label(root,image=logo)
    logoimg.place(x=210,y=10,in_=root)

    usname = PhotoImage(file = 'userna.png')
    usname = usname.subsample(17, 17)
    uimg = Label(root,image=usname)
    uimg.place(x=40, y=87, in_=root)

    passwd = PhotoImage(file = 'passwd.png')
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

    subm = PhotoImage(file = 'submit.png')
    subm = subm.subsample(3,3)
    sub = Button(root,image = subm,command=search)
    sub.place(x=175,y=180,in_=root)

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

def after_sign_in(name,mail,user):
    global wrpas
    signin_clear()
    y_cor = 50
    lis = ["Welcome "+user,"Your name: "+name,"Your email id: "+mail]
    for data in lis:
        wrpas = Label(root,text=data,foreground="black")
        wrpas.config(font=('',15,"bold"))
        wrpas.place(x=25,y=y_cor,in_=root)
        y_cor+=50
            

def search():
    global wrpas
    data_b = open("Database.rpd","r")
    read_data = csv.reader(data_b)
    ch = 0
    user = uent.get()
    pasd = pent.get()
    for row in read_data:
        name, username, password,email = row
        una = str(user.lower())
        eml = str(username.lower())
        if(una == eml):
            if(pasd == password):
                print("Welcome",name,email)
                after_sign_in(name, email, username)
            else:
                wrpas = Label(root,text='wrong password',foreground='red')
                wrpas.config(font=('Times',10))
                wrpas.place(x=75,y=200,in_=root)
            ch = 1
            break    
    if(ch == 0):
        wrpas = Label(root,text='not found             ',foreground='red')
        wrpas.config(font=('Times',10))
        wrpas.place(x=75,y=200,in_=root)
                
    data_b.close()            

def warn(string,col):
    global wrpas
    wrpas = Label(root,text=string,foreground=col)
    wrpas.config(font=('Times',10))
    wrpas.place(x=75,y=225,in_=root)
        
def taken_check(user,mail_id):
    global ch
    ch = 0
    with open("Database.rpd","r") as db:
        data_read = csv.reader(db)
        for row in data_read:
            n, username, p,email = row
            if(user == username):
                print(user,username)
                ch = 1
            elif(mail_id.lower() == email.lower()):
                ch = 2
    return ch
            
def write_csv(list_data):
    with open("Database.rpd","a") as db:
        data_write = csv.writer(db)
        data_write.writerow(list_data)
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
        #ent_list = [name_ent+','+uname_ent+','+pass_ent+','+mail_ent]
        ent_list = [name_ent,uname_ent,pass_ent,mail_ent]
        print(ent_list)
        
        write_csv(ent_list)
        main()
        warn("sign in was successful!","green")
    
def signup():
    global wrpas, logo, logoimg
    global login_un, login_pa, login_em, login_cp, login_na ,un_ent,na_ent,pa_ent,em_ent,cp_ent, back_but, signup_but
    root.title("login to RPD_tech")
    
    signin_clear()
    
    logo = PhotoImage(file = 'cosm.png')
    logo = logo.subsample(3,3)
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
