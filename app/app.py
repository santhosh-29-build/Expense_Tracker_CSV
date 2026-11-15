"""
Expense Tracker - Modern Tkinter UI
-----------------------------------
Keeps the original application window dimensions and Service API:
    Service.login(user_id, password)
    Service.register(user_id, user_name, password)
    Service.account_info(user_id)
    Service.check_balance(user_id)
    Service.credit(user_id, amount)
    Service.debit(user_id, amount)
    Service.transaction_history(user_id)
    Service.recent_transaction_history(user_id)

Run from the project directory so `model.account_service` can be imported.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

from model.account_service import Service


# ---------------------------------------------------------------------
# Theme
# ---------------------------------------------------------------------
COLORS = {
    "page": "#F3F6FC",
    "surface": "#FFFFFF",
    "surface_alt": "#F8FAFD",
    "primary": "#4F46E5",
    "primary_hover": "#4338CA",
    "primary_soft": "#EEF2FF",
    "text": "#172033",
    "muted": "#718096",
    "border": "#E4E9F2",
    "green": "#0F9D78",
    "green_hover": "#0B8062",
    "green_soft": "#E8F7F1",
    "red": "#DC5263",
    "red_hover": "#C43D50",
    "red_soft": "#FFF0F1",
    "sidebar": "#171D36",
    "sidebar_muted": "#AAB3CE",
}

FONT = "Segoe UI"


def configure_styles():
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(
        "App.TFrame",
        background=COLORS["page"],
    )
    style.configure(
        "Card.TFrame",
        background=COLORS["surface"],
        relief="flat",
    )
    style.configure(
        "Title.TLabel",
        background=COLORS["page"],
        foreground=COLORS["text"],
        font=(FONT, 23, "bold"),
    )
    style.configure(
        "Subtitle.TLabel",
        background=COLORS["page"],
        foreground=COLORS["muted"],
        font=(FONT, 10),
    )
    style.configure(
        "CardTitle.TLabel",
        background=COLORS["surface"],
        foreground=COLORS["text"],
        font=(FONT, 11, "bold"),
    )
    style.configure(
        "Field.TLabel",
        background=COLORS["surface"],
        foreground=COLORS["text"],
        font=(FONT, 9, "bold"),
    )
    style.configure(
        "Muted.TLabel",
        background=COLORS["surface"],
        foreground=COLORS["muted"],
        font=(FONT, 9),
    )
    style.configure(
        "Value.TLabel",
        background=COLORS["surface"],
        foreground=COLORS["text"],
        font=(FONT, 22, "bold"),
    )
    style.configure(
        "Primary.TButton",
        background=COLORS["primary"],
        foreground="#FFFFFF",
        font=(FONT, 10, "bold"),
        padding=(14, 10),
        borderwidth=0,
    )
    style.map(
        "Primary.TButton",
        background=[("active", COLORS["primary_hover"]), ("pressed", COLORS["primary_hover"])],
        foreground=[("disabled", "#D9DDF5")],
    )
    style.configure(
        "Success.TButton",
        background=COLORS["green"],
        foreground="#FFFFFF",
        font=(FONT, 10, "bold"),
        padding=(14, 10),
        borderwidth=0,
    )
    style.map(
        "Success.TButton",
        background=[("active", COLORS["green_hover"]), ("pressed", COLORS["green_hover"])],
    )
    style.configure(
        "Danger.TButton",
        background=COLORS["red"],
        foreground="#FFFFFF",
        font=(FONT, 10, "bold"),
        padding=(14, 10),
        borderwidth=0,
    )
    style.map(
        "Danger.TButton",
        background=[("active", COLORS["red_hover"]), ("pressed", COLORS["red_hover"])],
    )
    style.configure(
        "Secondary.TButton",
        background=COLORS["surface_alt"],
        foreground=COLORS["text"],
        font=(FONT, 9, "bold"),
        padding=(12, 8),
        borderwidth=1,
        relief="solid",
    )
    style.map(
        "Secondary.TButton",
        background=[("active", COLORS["primary_soft"])],
    )
    style.configure(
        "Modern.TEntry",
        fieldbackground="#FFFFFF",
        foreground=COLORS["text"],
        insertcolor=COLORS["text"],
        padding=10,
        bordercolor=COLORS["border"],
        lightcolor=COLORS["border"],
        darkcolor=COLORS["border"],
    )
    style.configure(
        "Treeview",
        background="#FFFFFF",
        fieldbackground="#FFFFFF",
        foreground=COLORS["text"],
        rowheight=30,
        font=(FONT, 9),
        borderwidth=0,
    )
    style.configure(
        "Treeview.Heading",
        background=COLORS["surface_alt"],
        foreground=COLORS["muted"],
        font=(FONT, 9, "bold"),
        padding=8,
        relief="flat",
    )
    style.map(
        "Treeview",
        background=[("selected", COLORS["primary_soft"])],
        foreground=[("selected", COLORS["text"])],
    )


def place_window(window, geometry, resizable=False):
    window.geometry(geometry)
    if not resizable:
        window.resizable(False, False)


def make_card(parent, padding=22):
    outer = tk.Frame(parent, bg=COLORS["surface"], highlightthickness=1,
                     highlightbackground=COLORS["border"], bd=0)
    inner = tk.Frame(outer, bg=COLORS["surface"])
    inner.pack(fill="both", expand=True, padx=padding, pady=padding)
    return outer, inner


def make_heading(parent, title, subtitle=None):
    tk.Label(
        parent, text=title, bg=COLORS["page"], fg=COLORS["text"],
        font=(FONT, 22, "bold")
    ).pack(anchor="w")
    if subtitle:
        tk.Label(
            parent, text=subtitle, bg=COLORS["page"], fg=COLORS["muted"],
            font=(FONT, 10)
        ).pack(anchor="w", pady=(5, 0))


def make_field(parent, label, show=None):
    tk.Label(
        parent, text=label, bg=COLORS["surface"], fg=COLORS["text"],
        font=(FONT, 9, "bold")
    ).pack(anchor="w", pady=(12, 6))
    entry = ttk.Entry(parent, style="Modern.TEntry", font=(FONT, 10), show=show or "")
    entry.pack(fill="x")
    return entry


def show_error(title, message, parent=None):
    messagebox.showerror(title, message, parent=parent)


def show_info(title, message, parent=None):
    messagebox.showinfo(title, message, parent=parent)


# ---------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------
root = tk.Tk()
root.title("Expense Tracker | Sign in")
place_window(root, "800x600")
root.configure(bg=COLORS["page"])
configure_styles()

dashboard = None
current_user_id = None


def open_section(section_name):
    """Generic section window retained for future sections."""
    section_window = tk.Toplevel(dashboard)
    section_window.title(section_name)
    place_window(section_window, "800x500", resizable=True)
    section_window.configure(bg=COLORS["page"])

    content = tk.Frame(section_window, bg=COLORS["page"], padx=30, pady=28)
    content.pack(fill="both", expand=True)
    make_heading(content, section_name)
    card, body = make_card(content)
    card.pack(fill="both", expand=True, pady=(22, 0))
    tk.Label(
        body, text=section_name, bg=COLORS["surface"],
        fg=COLORS["text"], font=(FONT, 16, "bold")
    ).pack(anchor="w")


def show_data_table(parent, dataframe, title):
    window = tk.Toplevel(parent)
    window.title(title)
    place_window(window, "800x400", resizable=True)
    window.configure(bg=COLORS["page"])

    page = tk.Frame(window, bg=COLORS["page"], padx=24, pady=22)
    page.pack(fill="both", expand=True)
    make_heading(page, title, "Your account activity at a glance")

    card, body = make_card(page, padding=12)
    card.pack(fill="both", expand=True, pady=(18, 0))

    if dataframe is None or dataframe.empty:
        tk.Label(
            body, text="No transactions found.", bg=COLORS["surface"],
            fg=COLORS["muted"], font=(FONT, 11)
        ).pack(expand=True)
        return

    columns = [str(column) for column in dataframe.columns]
    table_wrap = tk.Frame(body, bg=COLORS["surface"])
    table_wrap.pack(fill="both", expand=True)

    tree = ttk.Treeview(table_wrap, columns=columns, show="headings")
    vertical = ttk.Scrollbar(table_wrap, orient="vertical", command=tree.yview)
    horizontal = ttk.Scrollbar(table_wrap, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)

    for column in columns:
        tree.heading(column, text=column.replace("_", " ").title())
        tree.column(column, width=140, minwidth=90, anchor="w")

    for _, row in dataframe.iterrows():
        tree.insert("", "end", values=[str(value) for value in row.tolist()])

    tree.grid(row=0, column=0, sticky="nsew")
    vertical.grid(row=0, column=1, sticky="ns")
    horizontal.grid(row=1, column=0, sticky="ew")
    table_wrap.rowconfigure(0, weight=1)
    table_wrap.columnconfigure(0, weight=1)


def show_balance(user_id):
    window = tk.Toplevel(dashboard)
    window.title("Check Balance")
    place_window(window, "400x250")
    window.configure(bg=COLORS["page"])

    try:
        balance = Service.check_balance(user_id)
        card, body = make_card(window, padding=24)
        card.pack(fill="both", expand=True, padx=22, pady=22)

        tk.Label(
            body, text="AVAILABLE BALANCE", bg=COLORS["surface"],
            fg=COLORS["muted"], font=(FONT, 9, "bold")
        ).pack(pady=(10, 12))
        tk.Label(
            body, text=f"₹ {balance:,.2f}", bg=COLORS["surface"],
            fg=COLORS["green"], font=(FONT, 27, "bold")
        ).pack()
        tk.Label(
            body, text="Current account balance", bg=COLORS["surface"],
            fg=COLORS["muted"], font=(FONT, 9)
        ).pack(pady=(8, 4))
    except FileNotFoundError:
        window.destroy()
        show_error("Account file not found", "Account transaction file not found.", dashboard)
    except pd.errors.EmptyDataError:
        window.destroy()
        show_info("No transactions", "No transactions found.", dashboard)
    except Exception as error:
        window.destroy()
        show_error("Unable to check balance", str(error), dashboard)


def show_recent_transactions(user_id):
    try:
        dataframe = Service.recent_transaction_history(user_id)
        show_data_table(dashboard, dataframe, "Recent Transactions")
    except FileNotFoundError:
        show_error("File not found", "Transaction file not found.", dashboard)
    except pd.errors.EmptyDataError:
        show_info("No transactions", "No transactions found.", dashboard)
    except Exception as error:
        show_error("Unable to load transactions", str(error), dashboard)


def show_transaction_history(user_id):
    try:
        dataframe = Service.transaction_history(user_id)
        show_data_table(dashboard, dataframe, "Transaction History")
    except FileNotFoundError:
        show_error("File not found", "Transaction file not found.", dashboard)
    except pd.errors.EmptyDataError:
        show_info("No transactions", "No transactions found.", dashboard)
    except Exception as error:
        show_error("Unable to load transactions", str(error), dashboard)


def show_amount_dialog(user_id, transaction_type):
    is_credit = transaction_type == "credit"
    title = "Add Credit" if is_credit else "Debit Amount"
    action = "CREDIT" if is_credit else "DEBIT"
    service_method = Service.credit if is_credit else Service.debit
    accent = COLORS["green"] if is_credit else COLORS["red"]
    accent_soft = COLORS["green_soft"] if is_credit else COLORS["red_soft"]

    window = tk.Toplevel(dashboard)
    window.title(title)
    place_window(window, "400x250")
    window.configure(bg=COLORS["page"])
    window.transient(dashboard)
    window.grab_set()

    card, body = make_card(window, padding=22)
    card.pack(fill="both", expand=True, padx=22, pady=22)

    tk.Label(
        body, text=title, bg=COLORS["surface"], fg=COLORS["text"],
        font=(FONT, 17, "bold")
    ).pack(anchor="w")
    tk.Label(
        body, text="Enter the amount in Indian Rupees", bg=COLORS["surface"],
        fg=COLORS["muted"], font=(FONT, 9)
    ).pack(anchor="w", pady=(4, 10))

    amount_entry = ttk.Entry(body, style="Modern.TEntry", font=(FONT, 12))
    amount_entry.pack(fill="x", pady=(4, 12))
    amount_entry.focus_set()

    def process():
        try:
            amount = float(amount_entry.get().strip())
            if amount <= 0:
                show_error("Invalid amount", "Enter an amount greater than zero.", window)
                return

            result = service_method(user_id, amount)
            if result is True:
                show_info("Success", f"Successfully {('credited' if is_credit else 'debited')} ₹{amount:,.2f}.", window)
                window.destroy()
            else:
                show_error("Transaction failed", f"{action.title()} unsuccessful. Please try again.", window)
        except ValueError:
            show_error("Invalid amount", "Enter a valid numeric amount.", window)
        except Exception as error:
            show_error("Transaction error", str(error), window)

    button = tk.Button(
        body, text=action, command=process, cursor="hand2",
        bg=accent, activebackground=COLORS["green_hover"] if is_credit else COLORS["red_hover"],
        fg="#FFFFFF", activeforeground="#FFFFFF", relief="flat",
        bd=0, font=(FONT, 10, "bold"), padx=20, pady=10
    )
    button.pack(fill="x", pady=(2, 0))


def show_account_info(user_id):
    try:
        account = Service.account_info(user_id)
    except Exception as error:
        show_error("Unable to load account", str(error), dashboard)
        return

    if account is None:
        show_error("Account not found", "Account details not found.", dashboard)
        return

    window = tk.Toplevel(dashboard)
    window.title("Account Information")
    place_window(window, "500x450", resizable=True)
    window.configure(bg=COLORS["page"])

    page = tk.Frame(window, bg=COLORS["page"], padx=26, pady=24)
    page.pack(fill="both", expand=True)
    make_heading(page, "Account Information", "Your registered account details")

    card, body = make_card(page, padding=18)
    card.pack(fill="both", expand=True, pady=(18, 0))

    for index, (key, value) in enumerate(account.items()):
        row_bg = COLORS["surface"] if index % 2 == 0 else COLORS["surface_alt"]
        row = tk.Frame(body, bg=row_bg, padx=12, pady=11)
        row.pack(fill="x", pady=2)
        tk.Label(
            row, text=f"{str(key).replace('_', ' ').title()}",
            bg=row_bg, fg=COLORS["muted"], font=(FONT, 9, "bold"),
            width=18, anchor="w"
        ).pack(side="left")
        tk.Label(
            row, text=str(value), bg=row_bg, fg=COLORS["text"],
            font=(FONT, 10), anchor="w"
        ).pack(side="left", fill="x", expand=True)


def open_dashboard(user_id):
    global dashboard, current_user_id
    current_user_id = int(user_id)
    root.withdraw()

    dashboard = tk.Toplevel(root)
    dashboard.title("Expense Tracker | Dashboard")
    place_window(dashboard, "1100x650", resizable=True)
    dashboard.configure(bg=COLORS["page"])
    dashboard.minsize(900, 560)

    def return_to_login():
        dashboard.destroy()
        root.deiconify()
        root.lift()

    dashboard.protocol("WM_DELETE_WINDOW", return_to_login)

    # Sidebar
    sidebar = tk.Frame(dashboard, bg=COLORS["sidebar"], width=235)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    brand = tk.Frame(sidebar, bg=COLORS["sidebar"], padx=22, pady=26)
    brand.pack(fill="x")
    tk.Label(
        brand, text="◈", bg=COLORS["sidebar"], fg="#A5B4FC",
        font=(FONT, 24, "bold")
    ).pack(anchor="w")
    tk.Label(
        brand, text="PULSE", bg=COLORS["sidebar"], fg="#FFFFFF",
        font=(FONT, 16, "bold")
    ).pack(anchor="w", pady=(8, 0))
    tk.Label(
        brand, text="EXPENSE TRACKER", bg=COLORS["sidebar"],
        fg=COLORS["sidebar_muted"], font=(FONT, 8, "bold")
    ).pack(anchor="w", pady=(2, 0))

    tk.Frame(sidebar, bg="#343B57", height=1).pack(fill="x", padx=20, pady=12)

    tk.Label(
        sidebar, text="WORKSPACE", bg=COLORS["sidebar"],
        fg=COLORS["sidebar_muted"], font=(FONT, 8, "bold")
    ).pack(anchor="w", padx=22, pady=(8, 10))

    # Main content
    content = tk.Frame(dashboard, bg=COLORS["page"], padx=34, pady=28)
    content.pack(side="left", fill="both", expand=True)

    def nav_button(label, callback):
        button = tk.Button(
            sidebar, text=label, command=callback, anchor="w",
            bg=COLORS["sidebar"], fg="#E5E9F5",
            activebackground="#2A3150", activeforeground="#FFFFFF",
            relief="flat", bd=0, cursor="hand2",
            font=(FONT, 9, "bold"), padx=22, pady=12
        )
        button.pack(fill="x", padx=10, pady=2)
        return button

    nav_button("▦   Overview", lambda: None)
    nav_button("＋   Add Credit", lambda: show_amount_dialog(current_user_id, "credit"))
    nav_button("－   Debit Amount", lambda: show_amount_dialog(current_user_id, "debit"))
    nav_button("◷   Transaction History", lambda: show_transaction_history(current_user_id))
    nav_button("↻   Recent Transactions", lambda: show_recent_transactions(current_user_id))
    nav_button("◎   Account Information", lambda: show_account_info(current_user_id))
    nav_button("₹   Check Balance", lambda: show_balance(current_user_id))

    spacer = tk.Frame(sidebar, bg=COLORS["sidebar"])
    spacer.pack(fill="both", expand=True)
    nav_button("⇥   Sign Out", return_to_login)

    # Dashboard header
    header = tk.Frame(content, bg=COLORS["page"])
    header.pack(fill="x")
    header_left = tk.Frame(header, bg=COLORS["page"])
    header_left.pack(side="left", fill="x", expand=True)
    make_heading(header_left, "Dashboard", "Welcome back. Here's your account overview.")
    tk.Label(
        header, text=f"USER  #{current_user_id}", bg=COLORS["primary_soft"],
        fg=COLORS["primary"], font=(FONT, 8, "bold"), padx=12, pady=8
    ).pack(side="right", anchor="n")

    # Balance feature card
    balance_card = tk.Frame(
        content, bg=COLORS["primary"], highlightthickness=0, bd=0
    )
    balance_card.pack(fill="x", pady=(26, 22))
    balance_inner = tk.Frame(balance_card, bg=COLORS["primary"], padx=25, pady=21)
    balance_inner.pack(fill="x")
    tk.Label(
        balance_inner, text="ACCOUNT BALANCE", bg=COLORS["primary"],
        fg="#D9DDFF", font=(FONT, 9, "bold")
    ).pack(anchor="w")
    balance_line = tk.Frame(balance_inner, bg=COLORS["primary"])
    balance_line.pack(fill="x", pady=(6, 0))
    tk.Label(
        balance_line, text="Check your latest available balance",
        bg=COLORS["primary"], fg="#FFFFFF", font=(FONT, 15, "bold")
    ).pack(side="left")
    ttk.Button(
        balance_line, text="View Balance  →", style="Secondary.TButton",
        command=lambda: show_balance(current_user_id)
    ).pack(side="right")

    # Quick actions
    tk.Label(
        content, text="QUICK ACTIONS", bg=COLORS["page"],
        fg=COLORS["muted"], font=(FONT, 9, "bold")
    ).pack(anchor="w", pady=(2, 12))

    actions = tk.Frame(content, bg=COLORS["page"])
    actions.pack(fill="both", expand=True)
    actions.columnconfigure((0, 1, 2), weight=1, uniform="action")
    actions.rowconfigure((0, 1), weight=1, uniform="action")

    action_items = [
        ("＋", "Add Credit", "Add money to your account", COLORS["green"], lambda: show_amount_dialog(current_user_id, "credit")),
        ("－", "Debit Amount", "Record an outgoing amount", COLORS["red"], lambda: show_amount_dialog(current_user_id, "debit")),
        ("◷", "Transaction History", "Review all transactions", COLORS["primary"], lambda: show_transaction_history(current_user_id)),
        ("↻", "Recent Transactions", "See your latest activity", "#0D9488", lambda: show_recent_transactions(current_user_id)),
        ("◎", "Account Information", "View your account details", "#7C3AED", lambda: show_account_info(current_user_id)),
        ("₹", "Check Balance", "View your available balance", "#D97706", lambda: show_balance(current_user_id)),
    ]

    for index, (symbol, title, description, accent, callback) in enumerate(action_items):
        row, col = divmod(index, 3)
        tile = tk.Frame(
            actions, bg=COLORS["surface"], highlightthickness=1,
            highlightbackground=COLORS["border"], cursor="hand2"
        )
        tile.grid(row=row, column=col, sticky="nsew", padx=(0 if col == 0 else 8, 8 if col < 2 else 0),
                  pady=(0 if row == 0 else 8, 8 if row == 0 else 0))

        tile_inner = tk.Frame(tile, bg=COLORS["surface"], padx=16, pady=14)
        tile_inner.pack(fill="both", expand=True)
        icon = tk.Label(
            tile_inner, text=symbol, bg=accent, fg="#FFFFFF",
            font=(FONT, 15, "bold"), width=3, height=1, pady=5
        )
        icon.pack(anchor="w")
        tk.Label(
            tile_inner, text=title, bg=COLORS["surface"],
            fg=COLORS["text"], font=(FONT, 10, "bold")
        ).pack(anchor="w", pady=(11, 3))
        tk.Label(
            tile_inner, text=description, bg=COLORS["surface"],
            fg=COLORS["muted"], font=(FONT, 8)
        ).pack(anchor="w")
        for widget in (tile, tile_inner, icon):
            widget.bind("<Button-1>", lambda event, fn=callback: fn())


# ---------------------------------------------------------------------
# Login and registration
# ---------------------------------------------------------------------
def login():
    user_id = id_entry.get().strip()
    password = password_entry.get()

    if not user_id.isdigit():
        show_error("Login failed", "User ID should contain only numbers.", root)
        return
    if not password:
        show_error("Login failed", "Please enter your password.", root)
        return

    try:
        if Service.login(int(user_id), password):
            show_info("Welcome", "Login successful.", root)
            open_dashboard(int(user_id))
        else:
            show_error("Login failed", "Invalid ID or password.", root)
    except Exception as error:
        show_error("Login error", str(error), root)


def open_register():
    register_window = tk.Toplevel(root)
    register_window.title("Create Account")
    place_window(register_window, "400x400")
    register_window.configure(bg=COLORS["page"])
    register_window.transient(root)
    register_window.grab_set()

    page = tk.Frame(register_window, bg=COLORS["page"], padx=28, pady=22)
    page.pack(fill="both", expand=True)

    tk.Label(
        page, text="Create account", bg=COLORS["page"],
        fg=COLORS["text"], font=(FONT, 21, "bold")
    ).pack(anchor="w")
    tk.Label(
        page, text="Enter your details to get started",
        bg=COLORS["page"], fg=COLORS["muted"], font=(FONT, 9)
    ).pack(anchor="w", pady=(3, 5))

    card, body = make_card(page, padding=16)
    card.pack(fill="both", expand=True, pady=(13, 0))

    reg_id_entry = make_field(body, "USER ID")
    reg_user_entry = make_field(body, "USER NAME")
    reg_password_entry = make_field(body, "PASSWORD", show="*")
    reg_confirm_entry = make_field(body, "CONFIRM PASSWORD", show="*")

    def register():
        user_id = reg_id_entry.get().strip()
        user_name = reg_user_entry.get().strip()
        password = reg_password_entry.get()
        confirm_password = reg_confirm_entry.get()

        if not user_id or not user_name or not password or not confirm_password:
            show_error("Registration failed", "All fields are required.", register_window)
            return
        if not user_id.isdigit():
            show_error("Registration failed", "User ID must contain only numbers.", register_window)
            return
        if not user_name.replace(" ", "").isalpha():
            show_error("Registration failed", "Enter an appropriate user name.", register_window)
            return
        if len(password) < 8:
            show_error("Registration failed", "Password must contain at least 8 characters.", register_window)
            return
        if password != confirm_password:
            show_error("Registration failed", "Passwords do not match.", register_window)
            return

        try:
            result = Service.register(int(user_id), user_name, password)
            if result:
                show_info("Success", "Registration successful. You can now log in.", register_window)
                register_window.destroy()
            else:
                show_error("Registration failed", "User ID already exists. Try logging in.", register_window)
        except Exception as error:
            show_error("Registration error", str(error), register_window)

    ttk.Button(body, text="Create Account", style="Primary.TButton", command=register).pack(fill="x", pady=(18, 0))


# Compact login layout: preserves the original 400x350 window while
# keeping both actions fully visible on standard and high-DPI displays.
login_page = tk.Frame(root, bg=COLORS["page"], padx=24, pady=9)
login_page.pack(fill="both", expand=True)

tk.Label(
    login_page, text="◈", bg=COLORS["page"], fg=COLORS["primary"],
    font=(FONT, 18, "bold")
).pack()
tk.Label(
    login_page, text="Welcome back", bg=COLORS["page"],
    fg=COLORS["text"], font=(FONT, 18, "bold")
).pack(pady=(0, 1))
tk.Label(
    login_page, text="Sign in to continue to Expense Tracker",
    bg=COLORS["page"], fg=COLORS["muted"], font=(FONT, 8)
).pack()

login_card, login_body = make_card(login_page, padding=12)
login_card.pack(fill="x", pady=(9, 0))

tk.Label(
    login_body, text="USER ID", bg=COLORS["surface"],
    fg=COLORS["text"], font=(FONT, 8, "bold")
).pack(anchor="w", pady=(2, 3))
id_entry = ttk.Entry(login_body, style="Modern.TEntry", font=(FONT, 10))
id_entry.pack(fill="x")

tk.Label(
    login_body, text="PASSWORD", bg=COLORS["surface"],
    fg=COLORS["text"], font=(FONT, 8, "bold")
).pack(anchor="w", pady=(8, 3))
password_entry = ttk.Entry(login_body, style="Modern.TEntry", font=(FONT, 10), show="*")
password_entry.pack(fill="x")

ttk.Button(login_body, text="Sign In", style="Primary.TButton", command=login).pack(fill="x", pady=(10, 5))
ttk.Button(login_body, text="Create New Account", style="Secondary.TButton", command=open_register).pack(fill="x")

password_entry.bind("<Return>", lambda event: login())
id_entry.bind("<Return>", lambda event: password_entry.focus_set())

root.mainloop()
