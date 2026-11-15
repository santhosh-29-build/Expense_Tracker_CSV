
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import pandas as pd 
from model.account_service import Service



def open_section(section_name):
    section_window = tk.Toplevel(dashboard)
    section_window.title(section_name)
    section_window.geometry("800x500")
    section_window.configure(bg="white")

    tk.Label(
        section_window,
        text=section_name,
        font=("Arial", 22, "bold"),
        bg="white"
    ).pack(pady=30)



def open_dashboard(id: int):
    global dashboard

    root.destroy()

    dashboard = tk.Tk()
    dashboard.title("Expense Tracker - Dashboard")
    dashboard.geometry("1100x650")
    dashboard.configure(bg="#F1F5F9")

    tk.Label(
        dashboard,
        text="EXPENSE TRACKER",
        font=("Arial", 26, "bold"),
        bg="#F1F5F9",
        fg="#1E293B"
    ).pack(pady=30)

    tk.Label(
        dashboard,
        text="Welcome! Select an option",
        font=("Arial", 13),
        bg="#F1F5F9",
        fg="#64748B"
    ).pack(pady=5)

    button_frame = tk.Frame(
        dashboard,
        bg="#F1F5F9"
    )
    button_frame.pack(pady=40)

    # Button name, function, row, column
    options = [
        ("Account Info", show_account_info, 0, 0),
        ("Credit", show_credit, 0, 1),
        ("Debit", show_debit, 1, 0),
        ("Transaction History", show_transaction_history, 1, 1),
        ("Recent Transaction History", show_recent_transactions, 2, 0),
        ("Check Balance",show_balance,2,1)
    ]

    for name, function, row, col in options:

        btn = tk.Button(
            button_frame,
            text=name,
            font=("Arial", 14, "bold"),
            width=25,
            height=3,
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            cursor="hand2",
            command=lambda f=function: f(id)
        )

        btn.grid(
            row=row,
            column=col,
            padx=20,
            pady=15
        )

    dashboard.mainloop()
    
    
def show_balance(user_id):
    balance_window = tk.Toplevel(dashboard)
    balance_window.title("Check Balance")
    balance_window.geometry("400x250")
    balance_window.configure(bg="#F1F5F9")

    try:
        balance = Service.check_balance(user_id)

        tk.Label(
            balance_window,
            text="AVAILABLE BALANCE",
            font=("Arial", 16, "bold"),
            bg="#F1F5F9",
            fg="#1E293B"
        ).pack(pady=25)

        tk.Label(
            balance_window,
            text=f"₹ {balance:,.2f}",
            font=("Arial", 25, "bold"),
            bg="#F1F5F9",
            fg="#16A34A"
        ).pack(pady=15)

    except FileNotFoundError:
        messagebox.showerror("Error", "Account transaction file not found.")

    except pd.errors.EmptyDataError:
        messagebox.showinfo("Information", "No transactions found.")
    
    
def show_recent_transactions(user_id):
    recent_window = tk.Toplevel(dashboard)
    recent_window.title("Recent Transactions")
    recent_window.geometry("800x400")

    try:
        df = Service.recent_transaction_history(user_id)

        recent_text = tk.Text(
            recent_window,
            font=("Consolas", 11),
            wrap="none"
        )
        recent_text.pack(fill="both", expand=True)

        recent_text.insert("1.0", df.to_string(index=False))
        recent_text.config(state="disabled")

    except FileNotFoundError:
        messagebox.showerror("Error", "Transaction file not found.")

    except pd.errors.EmptyDataError:
        messagebox.showinfo("Information", "No transactions found.")
        


def show_transaction_history(user_id):
    history_window = tk.Toplevel(dashboard)
    history_window.title("Transaction History")
    history_window.geometry("800x500")

    try:
        df = Service.transaction_history(user_id)

        history_text = tk.Text(
            history_window,
            font=("Consolas", 11),
            wrap="none"
        )
        history_text.pack(fill="both", expand=True)

        history_text.insert(
            "1.0",
            df.to_string(index=False)
        )

        history_text.config(state="disabled")

    except FileNotFoundError:
        messagebox.showerror(
            "Error",
            "Transaction file not found."
        )

    except pd.errors.EmptyDataError:
        messagebox.showinfo(
            "Information",
            "No transactions found."
        )



def show_debit(user_id):
    debit_window = tk.Toplevel(dashboard)
    debit_window.title("Debit Amount")
    debit_window.geometry("400x250")

    tk.Label(
        debit_window,
        text="Amount:",
        font=("Arial", 13)
    ).pack(pady=10)

    amount_entry = tk.Entry(debit_window, font=("Arial", 13))
    amount_entry.pack(pady=10)

    def process_debit():
        try:
            amount = float(amount_entry.get())

            if amount <= 0:
                messagebox.showerror("Error", "Enter a valid amount")
                return

            result = Service.debit(user_id, amount)

            if result is True:
                messagebox.showinfo("Success", "Successfully Debited!")
                debit_window.destroy()
            else:
                messagebox.showerror("Failed", "Debit Unsuccessful!")

        except ValueError:
            messagebox.showerror("Error", "Enter a valid amount")

    debit_button = tk.Button(
    debit_window,
    text="DEBIT",
    font=("Arial", 13, "bold"),
    width=18,
    height=2,
    bg="#DC2626",
    fg="white",
    activebackground="#B91C1C",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=process_debit
)
    debit_button.pack(pady=20)
    # Hover effect
    debit_button.bind(
        "<Enter>",
        lambda event: debit_button.config(bg="#B91C1C")
    )
    debit_button.bind(
        "<Leave>",
        lambda event: debit_button.config(bg="#DC2626")
    )
    
    
       
    
def show_credit(user_id):
    credit_window = tk.Toplevel(dashboard)
    credit_window.title("Add Credit")
    credit_window.geometry("400x250")

    tk.Label(
        credit_window,
        text="Amount:",
        font=("Arial", 13)
    ).pack(pady=10)

    amount_entry = tk.Entry(credit_window, font=("Arial", 13))
    amount_entry.pack(pady=10)

    def process_credit():
        try:
            amount = float(amount_entry.get())

            if amount <= 0:
                messagebox.showerror("Error", "Enter a valid amount")
                return

            result = Service.credit(user_id, amount)

            if result is True:
                messagebox.showinfo("Success", "Successfully Credited!")
                credit_window.destroy()
            else:
                messagebox.showerror("Failed", "Credit Unsuccessful!")

        except ValueError:
            messagebox.showerror("Error", "Enter a valid amount")

    credit_button = tk.Button(
    credit_window,
    text="CREDIT",
    font=("Arial", 13, "bold"),
    width=18,
    height=2,
    bg="#16A34A",
    fg="white",
    activebackground="#15803D",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=process_credit
    )
    
    credit_button.pack(pady=20)
    
    # Hover effect
    credit_button.bind(
        "<Enter>",
        lambda event: credit_button.config(bg="#15803D")
    )
    
    credit_button.bind(
        "<Leave>",
        lambda event: credit_button.config(bg="#16A34A")
    )
    
    

def show_account_info(user_id):

    # Fetch account details
    account = Service.account_info(user_id)

    if account is None:
        messagebox.showerror(
            "Error",
            "Account details not found"
        )
        return

    # Create Account Info window
    info_window = tk.Toplevel(dashboard)
    info_window.title("Account Information")
    info_window.geometry("500x450")
    info_window.configure(bg="white")

    # Heading
    tk.Label(
        info_window,
        text="ACCOUNT INFORMATION",
        font=("Arial", 20, "bold"),
        bg="white"
    ).pack(pady=20)

    # Display account details
    details_frame = tk.Frame(info_window, bg="white")
    details_frame.pack(padx=30, pady=10, fill="both")

    for index, (key, value) in enumerate(account.items()):

        tk.Label(
            details_frame,
            text=f"{key}:",
            font=("Arial", 12, "bold"),
            bg="white",
            anchor="w"
        ).grid(row=index, column=0, padx=10, pady=12, sticky="w")

        tk.Label(
            details_frame,
            text=str(value),
            font=("Arial", 12),
            bg="white",
            anchor="w"
        ).grid(row=index, column=1, padx=10, pady=12, sticky="w")



def login():
    user_id = id_entry.get().strip()
    password = password_entry.get()

    if not user_id.isdigit():
        messagebox.showerror(
            "Login Failed",
            "User ID should contain only numbers"
        )
        return

    if not password:
        messagebox.showerror(
            "Login Failed",
            "Please enter your password"
        )
        return

    if Service.login(int(user_id), password):
        messagebox.showinfo("Success", "Login Successful")
        open_dashboard(user_id)

    else:
        messagebox.showerror(
            "Login Failed",
            "Invalid ID or Password"
        )


# Registration function
def register():
    user_id = reg_id_entry.get().strip()
    user_name=reg_user_entry.get()
    password = reg_password_entry.get()
    confirm_password = reg_confirm_entry.get()

    # Validate empty fields
    if not user_id or not password or not confirm_password:
        messagebox.showerror(
            "Registration Failed",
            "All fields are required",
            parent=register_window
        )
        return

    # Validate User ID
    if not user_id.isdigit():
        messagebox.showerror(
            "Registration Failed",
            "User ID must contain only numbers",
            parent=register_window
        )
        return
    
    
    if not user_name.isalpha():
        messagebox.showerror(
            "Registration Failed",
            "Enter Appropriate user name",
            parent=register_window
        )
        return

    # Validate password length
    if len(password) < 8:
        messagebox.showerror(
            "Registration Failed",
            "Password must contain at least 8 characters",
            parent=register_window
        )
        return

    # Confirm password
    if password != confirm_password:
        messagebox.showerror(
            "Registration Failed",
            "Passwords do not match",
            parent=register_window
        )
        return

    # Call account service
    try:
        result = Service.register(int(user_id),user_name, password)

        if result:
            messagebox.showinfo(
                "Success",
                "Registration Successful!",
                parent=register_window
            )

            register_window.destroy()

        else:
            messagebox.showerror(
                "Registration Failed",
                "User ID already exists Try Login",
                parent=register_window
            )

    except Exception as error:
        messagebox.showerror(
            "Error",
            str(error),
            parent=register_window
        )


# Open registration window
def open_register():
    global register_window
    global reg_id_entry
    global reg_user_entry
    global reg_password_entry
    global reg_confirm_entry

    register_window = tk.Toplevel(root)
    register_window.title("Register")
    register_window.geometry("400x400")
    register_window.resizable(False, False)

    tk.Label(
        register_window,
        text="REGISTER",
        font=("Arial", 22, "bold")
    ).pack(pady=20)

    tk.Label(register_window, text="User ID").pack()

    reg_id_entry = tk.Entry(
        register_window,
        width=25,
        font=("Arial", 12)
    )
    reg_id_entry.pack(pady=5)
    
    tk.Label(register_window, text="User Name").pack()

    reg_user_entry = tk.Entry(
        register_window,
        width=25,
        font=("Arial", 12)
    )
    reg_user_entry.pack(pady=5)

    tk.Label(register_window, text="Password").pack()

    reg_password_entry = tk.Entry(
        register_window,
        width=25,
        font=("Arial", 12),
        show="*"
    )
    reg_password_entry.pack(pady=5)

    tk.Label(register_window, text="Confirm Password").pack()

    reg_confirm_entry = tk.Entry(
        register_window,
        width=25,
        font=("Arial", 12),
        show="*"
    )
    reg_confirm_entry.pack(pady=5)

    tk.Button(
        register_window,
        text="Register",
        width=15,
        bg="green",
        fg="white",
        font=("Arial", 11, "bold"),
        command=register
    ).pack(pady=20)


# LOGIN WINDOW
root = tk.Tk()
root.title("Login")
root.geometry("400x350")
root.resizable(False, False)

tk.Label(
    root,
    text="LOGIN",
    font=("Arial", 22, "bold")
).pack(pady=20)

tk.Label(root, text="User ID").pack()

id_entry = tk.Entry(
    root,
    width=25,
    font=("Arial", 12)
)
id_entry.pack(pady=5)

tk.Label(root, text="Password").pack()

password_entry = tk.Entry(
    root,
    width=25,
    font=("Arial", 12),
    show="*"
)
password_entry.pack(pady=5)

tk.Button(
    root,
    text="Login",
    width=15,
    bg="blue",
    fg="white",
    font=("Arial", 12, "bold"),
    command=login
).pack(pady=10)

tk.Button(
    root,
    text="Create New Account",
    width=20,
    command=open_register
).pack(pady=5)

root.mainloop()
