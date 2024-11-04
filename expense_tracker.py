

import mysql.connector as mc
import tkinter as tk
from tkinter import messagebox



class ExpenseManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Manager")

        self.name_label = tk.Label(root, text="Name:")
        self.name_entry = tk.Entry(root)

        self.date_label = tk.Label(root, text="Date:")
        self.date_entry = tk.Entry(root)

        self.month_label = tk.Label(root, text="Month:")
        self.month_entry = tk.Entry(root)

        self.year_label = tk.Label(root, text="Year:")
        self.year_entry = tk.Entry(root)

        self.salary_label = tk.Label(root, text="Salary:")
        self.salary_entry = tk.Entry(root)

        self.limit_label = tk.Label(root, text="Daily Limit:")
        self.limit_entry = tk.Entry(root)

        self.expense_button = tk.Button(root, text="Enter Expenses", command=self.enter_expenses)
        self.view_table_button = tk.Button(root, text="View Table", command=self.view_table)
        self.sum_expense_button = tk.Button(root, text="Total Expense", command=self.sum_total_expense_by_name_and_month)
        self.sum_expense_button.grid(row=8, column=0, columnspan=2, pady=10)
        # Grid layout
        self.name_label.grid(row=0, column=0, sticky=tk.E)
        self.name_entry.grid(row=0, column=1)
        self.date_label.grid(row=1, column=0, sticky=tk.E)
        self.date_entry.grid(row=1, column=1)
        self.month_label.grid(row=2, column=0, sticky=tk.E)
        self.month_entry.grid(row=2, column=1)
        self.year_label.grid(row=3, column=0, sticky=tk.E)
        self.year_entry.grid(row=3, column=1)
        self.salary_label.grid(row=4, column=0, sticky=tk.E)
        self.salary_entry.grid(row=4, column=1)
        self.limit_label.grid(row=5, column=0, sticky=tk.E)
        self.limit_entry.grid(row=5, column=1)
        self.expense_button.grid(row=6, column=0, columnspan=2, pady=10)
        self.view_table_button.grid(row=7, column=0, columnspan=2)

    def get_db_connection(self):
        return mc.connect(host='localhost', user='root', passwd='aparna@2004', database='student')

    def enter_expenses(self):
        try:
            mycon = self.get_db_connection()
            cur = mycon.cursor()

            name = self.name_entry.get()
            date = int(self.date_entry.get())
            month = self.month_entry.get()
            year = int(self.year_entry.get())
            sal = int(self.salary_entry.get())
            lim = int(self.limit_entry.get())

            
            exp1=0
            exp2=0
            exp3=0
            exp4=0
            exp5=0
            exp6=0
            while True:
                
                print("*********************************")
                print("Enter your todays expense!!: ")
                print()
                n=int(input("Enter 1. shopping\n2. travel\n3. bills\n4. food\n5. rent\n6. other\n7. exit "))
                if n==1:
                  exp1=int(input("Enter expense: "))
                elif n==2:
                  exp2=int(input("Enter expense: "))
                elif n==3:
                  exp3=int(input("Enter expense: "))
                elif n==4:
                  exp4=int(input("Enter expense: "))
                elif n==5:
                  exp5=int(input("Enter expense: "))
                elif n==6:
                  exp6=int(input("Enter expense: "))
                else:
                     break
            total_expense = exp1 + exp2 + exp3 + exp4 + exp5 + exp6
            st = "INSERT INTO abcde(name, Date, month, year, food, shopping, travel, bills, rent, other, total_expense) VALUES('{}', {}, '{}', {}, {}, {}, {}, {}, {}, {}, {})".format(name, date, month, year, exp4, exp1, exp2, exp3, exp5, exp6, total_expense)
            cur.execute(st)
            mycon.commit()
            t=exp1+exp2+exp3+exp4+exp5+exp6
            
            if t>lim:
               print("You have crossed your daily limit!!")
               print("Remaining savings: ",sal-int(t))
               
            elif t<lim:
               print("You spent: ",t)
               print("remaining savings: ",sal-int(t)) 
            elif t==lim:
               print("you have reached your limit for today!!")
               print("Remaining savings: ",sal-int(t))

            messagebox.showinfo("Expense Manager", "Expenses entered successfully!")

        except mc.Error as e:
            messagebox.showerror("Expense Manager", f"Error: {e}")

        finally:
            if mycon.is_connected():
                cur.close()
                mycon.close()

    def view_table(self):
        try:
            mycon = self.get_db_connection()
            cur = mycon.cursor()

            
            print("EXPENSE TABLE:\n ")
            print("(name,date,month,year,food,shopping,travel,bills,rent,other,Total expense)")
            string="select * from abcde"
            cur.execute(string)
            data=cur.fetchall()
            for i in data:
              print(i)
                        
            table_str = "\n".join(map(str, data))
            messagebox.showinfo("Expense Manager - Table", f"Expense Table:\n{table_str}")

        except mc.Error as e:
            messagebox.showerror("Expense Manager", f"Error: {e}")
        finally:
            if mycon.is_connected():
                cur.close()
                mycon.close()
    def sum_total_expense_by_name_and_month(self):
     try:
        mycon = self.get_db_connection()
        cur = mycon.cursor()

        name_to_search = self.name_entry.get()  
        month_to_search = self.month_entry.get()  

        query = f"SELECT name, month, SUM(total_expense) FROM abcde WHERE name = '{name_to_search}' AND month = '{month_to_search}' GROUP BY name, month"
        cur.execute(query)
        result = cur.fetchall()

        if not result:
            print(f"No data found for the name '{name_to_search}' and month '{month_to_search}'.")
        else:
            total_expense = result[0][2]
            daily_limit = int(self.limit_entry.get())
            days_in_month = 30  

            total_limit = daily_limit * days_in_month

            if total_expense <= total_limit:
                print(f"Total expenses for {name_to_search} in {month_to_search}: {total_expense}")
                print("Good job! You are within the total limit for the month.")
            else:
                print(f"Total expenses for {name_to_search} in {month_to_search}: {total_expense}")
                print("Warning! You have exceeded the total limit for the month.")

     except mc.Error as e:
        print(f"Error: {e}")

     finally:
        if mycon.is_connected():
            cur.close()
            mycon.close()            
                
                

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseManagerApp(root)
    root.mainloop()