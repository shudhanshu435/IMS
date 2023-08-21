from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import os

class salesClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        #Variable Declaration
        self.var_invoice=StringVar()
        self.bill_list=[]
        #Title
        lbl_title=Label(self.root,text=" View Customer Bills ",font=("goudy old style",30),bg="#184a45",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)
        
        lbl_invoice=Label(self.root,text="Invoice No.",font=("goudy old styke",15),bg="white").place(x=50,y=100)
        txt_invoice=Entry(self.root,textvariable=self.var_invoice,font=("goudy old styke",15),bg="lightyellow").place(x=160,y=102,width=180,height=28 )

        btn_search=Button(self.root,text="Search",command=self.search,font=("goudy old style",15,"bold"),bg="#2196f3",fg="white",cursor="hand2").place(x=360,y=101,width=120,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15,"bold"),bg="lightgray",cursor="hand2").place(x=490,y=101,width=120,height=28)

        #Bill List
        sales_frame=Frame(self.root,bd=3,relief=RIDGE)
        sales_frame.place(x=50,y=140,width=200,height=330)

        scrolly=Scrollbar(sales_frame,orient=VERTICAL)
        self.sales_List=Listbox(sales_frame,font=("goudy old style",15),bg="white",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.sales_List.yview)
        self.sales_List.pack(fill=BOTH,expand=1)
        self.sales_List.bind("<ButtonRelease-1>",self.get_data)
        #Bill Area 
        bill_frame=Frame(self.root,bd=3,relief=RIDGE)
        bill_frame.place(x=280,y=140,width=410,height=330)

        lbl_title2=Label(bill_frame,text="Customer Bills",font=("goudy old style",20),bg="orange").pack(side=TOP,fill=X)
        

        scrolly2=Scrollbar(bill_frame,orient=VERTICAL)
        self.bill_area=Text(bill_frame,bg="lightyellow",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH,expand=1)

#==========================Images========================================================
        self.bill_photo= Image.open("Images/counter.jpg")
        self.bill_photo=self.bill_photo.resize((400,300),Image.ANTIALIAS)
        self.bill_photo=ImageTk.PhotoImage(self.bill_photo)

        lbl_image=Label(self.root,image=self.bill_photo,bd=0)
        lbl_image.place(x=700,y=150)
        self.show()

#===========================Defining Functions========================================

    def show(self):
        self.bill_list[:]
        self.sales_List.delete(0,END)
        for i in os.listdir('bill'):
            if i.split('.')[-1]=='txt':
                self.sales_List.insert(END,i)
                self.bill_list.append(i.split('.')[0])

#========================Read the data of selected files=============================

    def get_data(self,ev):
        index_=self.sales_List.curselection()
        file_name=self.sales_List.get(index_) 
        print(file_name) 
        self.bill_area.delete('1.0',END) 
        fp=open(f'bill/{file_name}','r')
        for i in fp:
            self.bill_area.insert(END,i)
        fp.close()    

#====================================================================================

    def search(self):
        if self.var_invoice.get()=="":
            messagebox.showerror("Error","Invoice Number should be required",parent=self.root)
        else:
            if self.var_invoice.get() in self.bill_list:
                fp=open(f'bill/{self.var_invoice.get()}.txt','r')
                self.bill_area.delete('1.0',END)
                for i in fp:
                    self.bill_area.insert(END,i)
                fp.close()
            else:
                messagebox.showerror("Error","Invalid Invoice Number",parent=self.root)

#===========================================================================================
    def clear(self):
        self.show()
        self.bill_area.delete('1.0',END)
        self.var_invoice.set("")



if __name__=="__main__":
    root = Tk()
    obj = salesClass(root)
    root.mainloop()