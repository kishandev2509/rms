import sqlite3
from tkinter import messagebox, ttk
from tkinter import *
class categoryClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+230+140")
        self.root.title("Inventory Management System Project")
        self.root.config(bg="white")
        self.root.focus_force()
        self.root.iconbitmap("img/icon.ico")

        #===variables===
        self.variableName = ""
        self.varName = StringVar()

        #===title===
        lblTitle=Label(self.root,text="Manage Product Categories",bd=3,relief=RIDGE,bg="#184a45",fg="white",font=("goudy old style",20)).pack(side=TOP,fill=X,padx=10,pady=20)
        lblName=Label(self.root,text="Enter category name",bg="white",font=("goudy old style",20)).place(x=50,y=100)

        #===Entry Field===
        txtName=Entry(self.root,textvariable=self.varName,bg="lightyellow",font=("goudy old style",20)).place(x=50,y=170,width=300)

        #===button===
        btnAdd=Button(self.root,text="ADD",command=self.add,bg="#4caf50",fg="white",cursor="hand2",font=("goudy old style",12)).place(x=360,y=170,width=150,height=30)
        btnDelete=Button(self.root,text="Delete",command=self.delete,bg="red",fg="white",cursor="hand2",font=("goudy old style",12)).place(x=900,y=170,width=150,height=30)

        #===content===
        #====category Details===
        catFrame=Frame(self.root,bd=3,relief=RIDGE)
        catFrame.place(x=50,y=220,width=1000,height=250)

        scrolly=Scrollbar(catFrame,orient=VERTICAL)
        scrollx=Scrollbar(catFrame,orient=HORIZONTAL)

        self.categoryTable=ttk.Treeview(catFrame,columns=("cid","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.categoryTable.xview)
        scrolly.config(command=self.categoryTable.yview)

        self.categoryTable.heading("cid",text="C ID")
        self.categoryTable.heading("name",text="Name")

        self.categoryTable["show"]="headings"

        self.categoryTable.column("cid",width=20,anchor=CENTER)
        self.categoryTable.column("name",anchor=CENTER)
        self.categoryTable.bind("<ButtonRelease-1>",self.getData)

        self.categoryTable.pack(fill=BOTH,expand=1)

        self.show()

#========================================================================================
    #===show records in table===
    def show(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            cur.execute("Select * from category")
            rows=cur.fetchall()
            self.categoryTable.delete(*self.categoryTable.get_children())
            for row in rows:
                self.categoryTable.insert("",END,values=row)
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)

    #===insert selected row data in text feilds===
    def getData(self,ev):
        f=self.categoryTable.focus()
        content=(self.categoryTable.item(f))
        row=content['values']
        self.variableName = row[1]

    #===add function===
    def add(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            if self.varName.get()=="":
                messagebox.showerror("Error","Category Name must be entered",parent=self.root)
            else:
                cur.execute(f"Select * from category where name='{self.varName.get()}'")
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Category already exists, try different",parent=self.root)
                else:
                    cur.execute(f'Insert into category (name) values("{self.varName.get()}")')
                    con.commit()
                    messagebox.showinfo("Success","Category Added Successfull",parent=self.root)
                    self.show()
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)
        

    #===delete function===
    def delete(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            if self.variableName=="":
                messagebox.showerror("Error","Select a category first",parent=self.root)
            else:
                cur.execute(f"Select * from category where name='{self.variableName}'")
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Category Name",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op:
                        cur.execute(f"Delete from category where name='{self.variableName}'")
                        con.commit()
                        messagebox.showinfo("Success","category deleted Successfull",parent=self.root)
                        # self.varCategoryId.set("")
                        self.variableName = ""
                        self.show()
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)



if __name__=="__main__":
    root=Tk()
    obj=categoryClass(root)
    root.mainloop()