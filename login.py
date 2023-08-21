from tkinter import*
from PIL import ImageTk 
from tkinter import messagebox
import sqlite3
import os
import email_pass
import smtplib
import time

class Login_System:
    def __init__(self, root):
        self.root=root
        self.root.title("Login System")
                                        
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#fafafa")

        self.otp=''
#===images====
        #self.phone_image=ImageTk.PhotoImage(file="images/phone.png")
        #self.lbl_Phone_image=Label(self.root,image=self.phone_image,bd=0).place(x=200,y=50)
#===Login_Frame====
        self.employee_id=StringVar()
        self.password=StringVar()

        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        login_frame.place(x=500,y=90, width=350,height=460)

        title=Label(login_frame,text="Login System",font=("Elephant",30,"bold"),bg="white").place(x=0,y=30,relwidth=1)

        lbl_user=Label(login_frame,text="Employee ID",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=100)
        
        txt_username=Entry(login_frame,textvariable=self.employee_id,font=("times new roman",15),bg="#ECECEC").place(x=50,y=140,width=250)

        lbl_pass=Label(login_frame,text="Password",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=200)
        txt_pass=Entry(login_frame,textvariable=self.password,show="*",font=("times new roman",15),bg="#ECECEC").place(x=50,y=240,width=250)

        btn_login=Button(login_frame,text="Login",command=self.login,font=("Arial Rounded MT Bold",15),bg="#00B0F0",cursor="hand2").place(x=50,y=300,width=250,height=35)

        hr=Label(login_frame,bg="lightgray").place(x=50,y=375,width=250,height=2)
        or_=Label(login_frame,text="OR",bg="white",fg="lightgray",font=("times new roman",15,"bold")).place(x=150,y=360)

        btn_forget=Button(login_frame,text="Forget Password?",command=self.forget_window,font=("times new roman",13),bg="white",fg="#00759E",bd=0,activebackground="white").place(x=100,y=390)

        # register_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        # register_frame.place(x=500,y=570, width=350,height=60)

        #lbl_reg=Label(register_frame,text="Subscribe",font=("Times new Roman",13),bg="white").place(x=60,y=15)
       # self.send_email()
    def login(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="" or self.password.get()=="":
                messagebox.showerror('Error',"Provide Employee ID and Password Both",parent=self.root)
            else:   
                cur.execute("select utype from employee where eid=? AND pass=?",(self.employee_id.get(),self.password.get()))
                user=cur.fetchone()
                if user==None:
                    messagebox.showerror('Error',"Invalid Username or Password",parent=self.root)
                else:
                    if user[0]=="Admin":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)    

    def forget_window(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="":
                messagebox.showerror('Error',"Please Provide Employee ID",parent=self.root)
            else:
                cur.execute("select email from employee where eid=?",(self.employee_id.get(),))
                email=cur.fetchone()
                if email==None:
                    messagebox.showerror('Error',"Invalid Email ID",parent=self.root)
                else:
                    self.var_otp=StringVar()
                    self.var_new_pass=StringVar()
                    self.var_conf_pass=StringVar()

                    chk=self.send_email(email[0])
                    if chk=='f':
                        messagebox.showerror('Error',"Connection Error,Try Again",parent=self.root)
                    else:
                        self.forget_win=Toplevel(self.root)
                        self.forget_win.title('RESET PASSWORD')
                        self.forget_win.geometry('400x350+500+100')
                        self.forget_win.focus_force()

                        title=Label(self.forget_win,text="Reset Password",font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white").pack(side=TOP,fill=X)
                        lbl_reset=Label(self.forget_win,text="Enter OTP send on a Registered Email",font=("goudy old style",15,"bold")).place(x=20,y=60)
                        txt_reset=Entry(self.forget_win,textvariable=self.var_otp,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=20,y=100,width=250,height=30)
                    
                        self.btn_reset=Button(self.forget_win,text="Submit",command=self.validate_otp,font=("goudy old style",15,"bold"),bg="lightblue")
                        self.btn_reset.place(x=280,y=100,width=100,height=30)
                   
                        lbl_new_pass=Label(self.forget_win,text="New Password",font=("goudy old style",15,"bold")).place(x=20,y=160)
                        txt_new_pass=Entry(self.forget_win,textvariable=self.var_new_pass,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=20,y=190,width=250,height=30)
                   
                        lbl_conf_pass=Label(self.forget_win,text="Confirm Password",font=("goudy old style",15,"bold")).place(x=20,y=225)
                        txt_conf_pass=Entry(self.forget_win,textvariable=self.var_conf_pass,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=20,y=255,width=250,height=30)
                    
                        self.btn_update=Button(self.forget_win,text="Update",command=self.update_password,state=DISABLED,font=("goudy old style",15,"bold"),bg="lightblue")
                        self.btn_update.place(x=150,y=300,width=100,height=30)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)        

    def update_password(self):
        if self.var_new_pass.get()=="" or self.var_conf_pass.get()=="":
            messagebox.showerror('Error',"Please Enter new Password",parent=self.forget_win)
        elif self.var_new_pass.get()!=self.var_conf_pass.get():
            messagebox.showerror('Error',"Both the password field must be same")
        else:
            con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:   
            cur.execute("Update employee SET pass=? where eid=?",(self.var_new_pass.get(),self.employee_id.get()))
            con.commit()
            messagebox.showinfo('Successful',"Password Updated Successfully",parent=self.forget_win)
            self.forget_win.destroy() 

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)


    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror('Error',"Invalid OTP",parent=self.forget_win)    


    def send_email(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=email_pass.email_
        pass_=email_pass.pass_

        s.login(email_,pass_)

        self.otp=int(time.strftime("%H%S%M"))+int(time.strftime("%S"))

        subj='IMS-Reset Password OTP'
        msg=f'Dear Sir/Madam,\n\nYour OTP for Reset IMS password is {str(self.otp)}\n\n With Regards,\n Team 10'

        msg="Subject:{}\n\n{}".format(subj,msg)
        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return 'f'


root=Tk()
obj=Login_System(root)
root.mainloop()

