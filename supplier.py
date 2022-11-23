import sqlite3
from tkinter import messagebox, ttk
from tkinter import *
class supplierClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+230+140")
        self.root.title("Shop Management System Project")
        self.root.config(bg="white")
        self.root.focus_force()
        self.root.iconbitmap("img/icon.ico")

        #===variables===
        self.varSupInvoice=StringVar()
        self.varName=StringVar()
        self.varContact=StringVar()


        self.varSearchBy=StringVar()
        self.varSearchTxt=StringVar()
  
        #===search frame===
        searchFrame=LabelFrame(self.root,text="Search Supplier",bd=2,relief=RIDGE,font=("goudy old style",9,"bold"),bg="white")
        searchFrame.place(x=670,y=55,width=410,height=60)

        #===otions===
        cmbSearch=ttk.Combobox(searchFrame,textvariable=self.varSearchBy,values=("Invoice","Name","Contact"),state="readonly",justify=CENTER,font=("goudy old style",11))
        cmbSearch.place(x=5,y=7,width=100)
        cmbSearch.current(0)

        txtSearch=Entry(searchFrame,textvariable=self.varSearchTxt,font=("goudy old style",15),bg="lightyellow").place(x=110,y=5,width=210)

        
        btnSearch=Button(searchFrame,text="Search",command=self.search,bg="#4caf50",fg="white",cursor="hand2",font=("goudy old style",12)).place(x=330,y=3,width=70,height=30)



        #===title===
        title=Label(self.root,text="Supplier Details",bg="#0f4d7d",fg="white",font=("goudy old style",20)).place(x=50,y=10,width=1000,height=40)

        #===content===
        #===row1===
        lblSupplierInvoice=Label(self.root,text="Invoice No.",bg="white",font=("goudy old style",15)).place(x=50,y=80)
        txtSupplierInvoice=Entry(self.root,textvariable=self.varSupInvoice,bg="lightyellow",font=("goudy old style",15)).place(x=180,y=80,width=180)

        #===row2===
        lblName=Label(self.root,text="Name",bg="white",font=("goudy old style",15)).place(x=50,y=120)
        txtName=Entry(self.root,textvariable=self.varName,bg="lightyellow",font=("goudy old style",15)).place(x=180,y=120,width=180)

        #===row3===
        lblContact=Label(self.root,text="Contact",bg="white",font=("goudy old style",15)).place(x=50,y=160)
        txtContact=Entry(self.root,textvariable=self.varContact,bg="lightyellow",font=("goudy old style",15)).place(x=180,y=160,width=180)
        #===row4===
        lblDesc=Label(self.root,text="Description",bg="white",font=("goudy old style",15)).place(x=50,y=200)
        self.txtDesc=Text(self.root,bg="lightyellow",font=("goudy old style",15))
        self.txtDesc.place(x=180,y=200,width=470,height=200)

 
        #===buttons===
        btnAdd=Button(self.root,text="Add",command=self.add,bg="#2196f3",fg="white",cursor="hand2",font=("goudy old style",20)).place(x=180,y=425,width=110,height=35)
        
        btnUpdate=Button(self.root,text="Update",command=self.update,bg="#4caf50",fg="white",cursor="hand2",font=("goudy old style",20)).place(x=300,y=425,width=110,height=35)
        
        btnDelete=Button(self.root,text="Delete",command=self.delete,bg="#f44336",fg="white",cursor="hand2",font=("goudy old style",20)).place(x=420,y=425,width=110,height=35)
        
        btnClear=Button(self.root,text="Clear",command=self.clear,bg="#607d8b",fg="white",cursor="hand2",font=("goudy old style",20)).place(x=540,y=425,width=110,height=35)

        #====supplier Details===
        supFrame=Frame(self.root,bd=3,relief=RIDGE)
        supFrame.place(x=670,y=120,width=410,height=350)

        scrolly=Scrollbar(supFrame,orient=VERTICAL)
        scrollx=Scrollbar(supFrame,orient=HORIZONTAL)

        self.supplierTable=ttk.Treeview(supFrame,columns=("invoice","name","contact","desc"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)

        self.supplierTable.heading("invoice",text="Invoice")
        self.supplierTable.heading("name",text="Name")
        self.supplierTable.heading("contact",text="Contact")
        self.supplierTable.heading("desc",text="Description")

        self.supplierTable["show"]="headings"

        self.supplierTable.column("invoice",width=90)
        self.supplierTable.column("contact",width=90)
        # self.supplierTable.column("address",width=90)
        self.supplierTable.bind("<ButtonRelease-1>",self.getData)

        self.supplierTable.pack(fill=BOTH,expand=1)

        self.show()

#========================================================================================
    #===show records in table===
    def show(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            cur.execute("Select * from supplier")
            rows=cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert("",END,values=row)
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)

    #===insert selected row data in text feilds===
    def getData(self,ev):
        f=self.supplierTable.focus()
        content=(self.supplierTable.item(f))
        row=content['values']

        self.varSupInvoice.set(row[0])
        self.varName.set(row[1])
        self.varContact.set(row[2])
        self.txtDesc.delete('1.0',END)
        self.txtDesc.insert(END,row[3])

    #===add function===
    def add(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            if self.varSupInvoice.get()=="":
                messagebox.showerror("Error","Invoice must be entered",parent=self.root)
            else:
                cur.execute(f"Select * from supplier where invoice={self.varSupInvoice.get()}")
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Invoice no. already assigned, try different",parent=self.root)
                else:
                    values=f'"{self.varSupInvoice.get()}","{self.varName.get()}","{self.varContact.get()}","{self.txtDesc.get("1.0",END)}"'
                    # print(values)
                    cur.execute(f"Insert into supplier(invoice,name,contact,desc) values({values})")
                    con.commit()
                    messagebox.showinfo("Success","Supplier Added Successfull",parent=self.root)
                    self.show()
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)
        

    #===update function===
    def update(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            if self.varSupInvoice.get()=="":
                messagebox.showerror("Error","Invoice no. must be entered",parent=self.root)
            else:
                cur.execute(f"Select * from supplier where Invoice={self.varSupInvoice.get()}")
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice no.",parent=self.root)
                else:
                    cur.execute(f"Update supplier set name='{self.varName.get()}',contact='{self.varContact.get()}',desc='{self.txtDesc.get(1.0,END)}' where invoice='{self.varSupInvoice.get()}'")
                    con.commit()
                    messagebox.showinfo("Success","Supplier updated Successfull",parent=self.root)
                    self.show()
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)
        

    #===delete function===
    def delete(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            if self.varSupInvoice.get()=="":
                messagebox.showerror("Error","Invoice no. must be entered",parent=self.root)
            else:
                cur.execute(f"Select * from supplier where Invoice='{self.varSupInvoice.get()}'")
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice no.",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?")
                    if op:
                        cur.execute(f"Delete from supplier where Invoice={self.varSupInvoice.get()}")
                        con.commit()
                        messagebox.showinfo("Success","supplier deleted Successfull",parent=self.root)
                        self.clear()
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)
        

    #===clear function===
    def clear(self):
        f=self.supplierTable.focus()
        content=(self.supplierTable.item(f))
        row=content['values']

        self.varSupInvoice.set("")
        self.varName.set("")
        self.varContact.set("")
        self.txtDesc.delete('1.0',END)
        self.show()

    #===search function===
    def search(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            if self.varSearchTxt.get()=="":
                self.clear()
            else:
                self.clear()
                cur.execute(f"Select * from supplier where {self.varSearchBy.get()} LIKE '%{self.varSearchTxt.get()}%'")
                rows=cur.fetchall()
                if rows==0:
                    messagebox.showerror("Error","No Record Found",parent=self.root)
                else:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    for row in rows:
                        self.supplierTable.insert("",END,values=row)
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)




if __name__=="__main__":
    root=Tk()
    obj=supplierClass(root)
    root.mainloop()