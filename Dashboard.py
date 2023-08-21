import sqlite3
import time
from tkinter import*
from tkinter import messagebox
from PIL import Image,ImageTk
from Employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
import os

class IMS:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1920x1080+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        #Heading and Logo
        self.icon_title=PhotoImage(file="Images/Icon3.png")
        title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font =("Arial",40,"bold"),bg="#985454",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #Logout button
        btn_logout = Button(self.root,text="Logout",command=self.logout,font=("Arial",15,"bold"),bg="yellow",cursor="hand2").place(x=1300,y=18,height=30,width=150)

        #Date And Time
        self.lbl_clock =Label(self.root,text="Welcome To Inventory Management System\t\t Date : DD-MM-YYYY\t\t Time:HH:MM:SS",font =("Arial",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)


        #left Menubar
        self.MenuLogo= Image.open("Images/LeftMenu.png")
        self.MenuLogo=self.MenuLogo.resize((200,200),Image.ANTIALIAS)
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)
        
        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=110,width=200,height=570)

        lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP,fill=X)

        #Creating All buttons
        self.icon_side= Image.open("Images/Arrow.png")
        self.icon_side=self.icon_side.resize((40,40),Image.ANTIALIAS)
        self.icon_side=ImageTk.PhotoImage(self.icon_side)
        lbl_menu = Label(LeftMenu,text="Menu",font=("Arial",20),bg="#009688").pack(side=TOP,fill=X)

        btn_employee = Button(LeftMenu,text="Employee",command=self.employee,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("Arial",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_supplier = Button(LeftMenu,text="Supplier",command=self.supplier,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("Arial",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_category = Button(LeftMenu,text="Category",command=self.category,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("Arial",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_product = Button(LeftMenu,text="product",command=self.product,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("Arial",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_sales = Button(LeftMenu,text="Sales",command=self.sales,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("Arial",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_exit = Button(LeftMenu,text="Exit",image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("Arial",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        
        
        #Content
        self.lbl_employee=Label(self.root,text="Total Employee \n [0]",bd=5,relief=RIDGE,bg="#0099ff",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_employee.place(x=300,y=120,height=150,width=300)
        
        self.lbl_supplier=Label(self.root,text="Total Supplier \n [0]",bd=5,relief=RIDGE,bg="#ff5722",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_supplier.place(x=650,y=120,height=150,width=300)

        self.lbl_category=Label(self.root,text="Total Category \n [0]",bd=5,relief=RIDGE,bg="#009688",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_category.place(x=1000,y=120,height=150,width=300)

        self.lbl_product=Label(self.root,text="Total Product \n [0]",bd=5,relief=RIDGE,bg="#607d8b",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_product.place(x=300,y=300,height=150,width=300)

        self.lbl_sales=Label(self.root,text="Total Sales\n [0]",bd=5,relief=RIDGE,bg="#ffc107",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_sales.place(x=650,y=300,height=150,width=300)
        
        #Footer
        lbl_footer =Label(self.root,text="This is Developed by Team Py-10",font =("Arial",15),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)
        self.update_content()
#=================================================================================================================
    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)

    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win)
    
    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=categoryClass(self.new_win)

    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=productClass(self.new_win)

    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=salesClass(self.new_win)

    def update_content(self):  # sourcery skip: remove-str-from-fstring
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            product=cur.fetchall()
            self.lbl_product.config(text=f'Total Product \n [{str(len(product))}]')
            
            cur.execute("select * from supplier")
            supplier=cur.fetchall()
            self.lbl_supplier.config(text=f'Total Supplier \n [{str(len(supplier))}]')
            
            cur.execute("select * from category")
            category=cur.fetchall()
            self.lbl_category.config(text=f'Total Category \n [{str(len(category))}]')
            
            cur.execute("select * from employee")
            employee=cur.fetchall()
            self.lbl_employee.config(text=f'Total Employee \n [{str(len(employee))}]')

            bill=len(os.listdir('bill'))
            self.lbl_sales.config(text=f'Total Sales \n[{str(bill)}]')

            time_=time.strftime("%I:%M:%S")
            date_=time.strftime("%d-%m-%Y ")
            self.lbl_clock.config(text=f"Welcome To Inventory Management System\t\t Date : {str(date_)}\t\t Time: {str(time_)}")
            self.lbl_clock.after(200,self.update_content)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)        

    def logout(self):
        self.root.destroy()
        os.system("python login.py")

if __name__=="__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
