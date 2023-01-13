"""A warehouse stock management application written in Python with Tkinter."""

import tkinter as tk
from Shoe import Shoe
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog as sd


# To hold a list of Shoe objects
shoe_list = []

# -----GUI Root-----
# Root window
root = tk.Tk()
root.title("Warehouse Stock Management")
# Set only column to expand
root.columnconfigure(0, weight=1)

# Heading
ttk.Label(root, text="Warehouse Stock Management", font=("TkDefaultFont", 18)).grid(pady=(20, 0))

# Top frame to hold 'All', 'View' and 'Edit' frames
top_frame = ttk.Frame(root)
top_frame.grid(padx=10, sticky=(tk.E + tk.W))
# Set column to expand
top_frame.columnconfigure(0, weight=1)


# -----Application Functions-----
def read_shoes_data():
    """Reads txt file and populates shoe_list"""
    filename = "inventory.txt"
    try:
        with open(filename, 'r') as file:
            # Skip first line
            next(file)
            # Read line by line, create shoe object with data in line and append to new list
            for line in file:
                line.rstrip()
                line = line.split(',')
                shoe = Shoe(line[0], line[1], line[2], line[3], line[4])
                shoe_list.append(shoe)
    except FileNotFoundError:
        messagebox.showerror("Error", "Could not read file")


def view_all():
    """Displays Shoe instances from shoe_list in the GUI text box."""
    # Clears Text box
    display_data.delete("1.0", tk.END)

    for shoe in shoe_list:
        data = shoe.__str__()
        display_data.insert(tk.END, data)


def capture_shoes():
    """Accepts user input to create and store a new Shoe instance."""
    # Clears Text box
    display_data.delete("1.0", tk.END)

    # Get bound variables
    country = selected.get()
    code = code_var.get().upper()
    product = name_var.get()
    try:
        int(cost_var.get())
    except ValueError:
        messagebox.showerror(title="Not a number", message="Cost must be an integer")
        cost_var.set("")
    else:
        cost = cost_var.get()

    try:
        int(quantity_var.get())
    except ValueError:
        messagebox.showerror(title="Not a number", message="Quantity must be an integer")
        quantity_var.set("")
    else:
        quantity = quantity_var.get()

    if selected.get() and code_var.get() and name_var.get() and cost_var.get() and quantity_var.get():
        # Create a new Shoe instance with inputs
        new_shoe = Shoe(country, code, product, cost, quantity)
        # Add new Shoe to list
        shoe_list.append(new_shoe)
        # Append new Shoe to file
        with open("inventory.txt", 'a') as file:
            file.write(f"\n{new_shoe.country},{new_shoe.code},{new_shoe.product},{new_shoe.get_cost()},"
                       f"{new_shoe.get_quantity()}")

        # Display output
        message = (
            f"\n{shoe_list[-1].__str__()}\n"
            "New product confirmed\n"
        )
        display_data.insert(tk.END, message)
    else:
        messagebox.showerror(title="Enter all fields", message="Fields cannot be left blank")

    # Re-set entry boxes
    selected.set("")
    code_var.set("")
    name_var.set("")
    cost_var.set("")
    quantity_var.set("")


def re_stock():
    """Displays lowest stocked Shoe and accepts user input to change quantity."""
    # Clears Text box
    display_data.delete("1.0", tk.END)

    # Set an arbitrarily large quantity to compare to each instance's quantity value.
    # Initialise 'lowest' to point to no value. After iteration this will point to a Shoe instance.
    quantity = 1000000000
    lowest = None

    # Iterate through list to return shoe with the lowest quantity
    for shoe in shoe_list:
        if int(shoe.get_quantity()) < quantity:
            lowest = shoe
            quantity = int(shoe.get_quantity())

    # Display result
    display_data.insert(tk.END, lowest.__str__())

    # Call messagebox to ask yes/no
    msg = "This product quantity is low. Would you like to re-stock?"
    restock = messagebox.askokcancel(title="Re-stock", message=msg)

    if restock:
        quantity = sd.askinteger("Quantity", "Enter quantity to re-stock to:")
        quantity = f"{quantity}\n"
        lowest.set_quantity(quantity)
        with open("inventory.txt", 'w') as file:
            # First line
            file.write("Country,Code,Product,Cost,Quantity\n")
            # Write each instance to a line in the file
            for shoe in shoe_list:
                file.write(f"{shoe.country},{shoe.code},{shoe.product},{shoe.get_cost()},{shoe.get_quantity()}")
        # Display confirmation
        restock_msg = f"\nItem has now been re-stocked\n\nQuantity is now {lowest.get_quantity()}"
        display_data.insert(tk.END, restock_msg)


def highest_qty():
    """Displays the highest stocked Shoe and a message to place on sale."""
    # Clears Text box
    display_data.delete("1.0", tk.END)

    # Initialise quantity to 0 to compare to each instance's quantity value
    # Initialise 'highest' to point to no value. After iteration this will point to a Shoe instance
    quantity = 0
    highest = None

    # Iterate through list and compare values
    for shoe in shoe_list:
        amount = (int(shoe.get_quantity()))
        if amount > quantity:
            quantity = amount
            highest = shoe

    # Display result
    display_data.insert(tk.END, highest.__str__())

    # Call message box to ask ok/cancel
    message = "This item is overstocked. Place on sale?."
    sale = messagebox.askokcancel(title="Sale", message=message)
    sale_msg = "\nItem now on sale\n"
    if sale:
        display_data.insert(tk.END, sale_msg)


def value_per_item():
    """Calculates the value of all Shoe instances and displays result in GUI text box."""
    # Clears Text box
    display_data.delete("1.0", tk.END)

    # Iterate through list and calculate value of each instance
    for shoe in shoe_list:
        value = int(shoe.get_cost()) * int(shoe.get_quantity())
        # Displays each instances name, code and value in text box
        data = f"{shoe.product}, {shoe.code}:  £{value}\n\n"
        display_data.insert(tk.END, data)


def search_shoe():
    """Accepts an input to search and display a specific Shoe instance."""
    # Clears Text box
    display_data.delete("1.0", tk.END)

    # Initialise check flag to False, sets True if Shoe is found
    product_code = search_var.get()
    check = False
    product = Shoe
    # Iterate through list, comparing code values
    for shoe in shoe_list:
        if shoe.code == product_code.upper():
            check = True
            product = shoe
            break
    # If flag is True, return str method of shoe. Else return not found.
    if check:
        data = f"\n{product.__str__()}"
    else:
        data = "\nProduct not found\n"

    # Display data and re-set entry box
    display_data.insert(tk.END, data)
    search_var.set("")


# -----GUI Styles-----
basic_style = ttk.Style()
basic_style.configure("basic.TButton", font=("TkDefaultFont", 12), background="grey")
label_style = ttk.Style()
label_style.configure("font.TLabel", font=("TkDefaultFont", 12))

# -----GUI Menu Layout-----

# -----VIEW-----
view_lbl = ttk.Label(text="View", style="font.TLabel")
view_frame = ttk.Labelframe(top_frame, labelwidget=view_lbl)
view_frame.grid(padx=10, pady=10, ipady=5, ipadx=5, sticky=(tk.W + tk.E))
# Configure all 3 columns
for i in range(3):
    view_frame.columnconfigure(i, weight=1, uniform="col")

# View all button
view_all_btn = ttk.Button(view_frame, text="View all stock", style="basic.TButton", command=view_all)
view_all_btn.grid(pady=(0, 5), row=1, column=0, sticky=(tk.W + tk.E))

# View stock value
value_btn = ttk.Button(view_frame, text="View stock value", style="basic.TButton", command=value_per_item)
value_btn.grid(row=2, column=0, sticky=(tk.W + tk.E))

# Individual product search
search_lbl = ttk.Label(view_frame, text="Enter product code", font=("TkDefaultFont", 11))
search_lbl.grid(row=0, column=2)
search_var = tk.StringVar()
search_ent = ttk.Entry(view_frame, textvariable=search_var, font=("TkDefaultFont", 12))
search_ent.grid(pady=(0, 5), row=1, column=2, sticky=(tk.W + tk.E))
# Individual product search button
search_btn = ttk.Button(view_frame, text="Search", style="basic.TButton", command=search_shoe)
search_btn.grid(row=2, column=2)

# -----EDIT-----
edit_lbl = ttk.Label(text="Edit", style="font.TLabel")
edit_frame = ttk.Labelframe(top_frame, labelwidget=edit_lbl)
edit_frame.grid(padx=10, pady=10, ipady=5, ipadx=5, sticky=(tk.W + tk.E))
# Configure all 3 columns
for i in range(3):
    edit_frame.columnconfigure(i, weight=1, uniform="col")

# Lowest stocked
restock_btn = ttk.Button(edit_frame, text="Edit lowest stocked", style="basic.TButton", command=re_stock)
restock_btn.grid(row=0, column=0, sticky=(tk.W + tk.E))

# Highest stocked
sale_btn = ttk.Button(edit_frame, text="Edit highest stocked", style="basic.TButton", command=highest_qty)
sale_btn.grid(row=0, column=2, sticky=(tk.W + tk.E))

# -----ADD-----
add_lbl = ttk.Label(text="Add", style="font.TLabel")
add_frame = ttk.Labelframe(top_frame, labelwidget=add_lbl)
add_frame.grid(padx=10, pady=10, ipady=5, ipadx=5, sticky=(tk.W + tk.E))
# Configure all 3 columns
for i in range(3):
    add_frame.columnconfigure(i, weight=1, uniform="col")

# Country
ttk.Label(add_frame, text="Country", font=("TkDefaultFont", 11)).grid(row=0, column=0)
selected = tk.StringVar()
selected.set("South Africa")
selected.get()
countries = [
    "South Africa", "China", "Vietnam",
    "United States", "Australia", "Canada", "Egypt",
    "Britain", "France", "Zimbabwe", "Morocco", "Israel",
    "Uganda", "Pakistan", "Brazil", "Columbia", "India",
    "South Korea"
]
drop = ttk.Combobox(add_frame, textvariable=selected, values=countries, font=("TkDefaultFont", 11))
drop.grid(padx=5, pady=(0, 5), row=1, column=0, sticky=(tk.W + tk.E))

# Cost per item
ttk.Label(add_frame, text="Cost Per Item", font=("TkDefaultFont", 11)).grid(row=2, column=0)
cost_var = tk.StringVar()
cost_ent = ttk.Entry(add_frame, textvariable=cost_var)
cost_ent.grid(padx=5, row=3, column=0, sticky=(tk.W + tk.E))

# Product Code
ttk.Label(add_frame, text="Product Code", font=("TkDefaultFont", 11)).grid(row=0, column=1)
code_var = tk.StringVar()
code_ent = ttk.Entry(add_frame, textvariable=code_var)
code_ent.grid(padx=5, pady=(0, 5), row=1, column=1, sticky=(tk.W + tk.E))

# Quantity
ttk.Label(add_frame, text="Quantity", font=("TkDefaultFont", 11)).grid(row=2, column=1)
quantity_var = tk.StringVar()
quantity_ent = ttk.Entry(add_frame, textvariable=quantity_var)
quantity_ent.grid(padx=5, row=3, column=1, sticky=(tk.W + tk.E))

# Product name
ttk.Label(add_frame, text="Product Name", font=("TkDefaultFont", 11)).grid(row=0, column=2)
name_var = tk.StringVar()
name_ent = ttk.Entry(add_frame, textvariable=name_var, font=("TkDefaultFont", 12))
name_ent.grid(padx=5, pady=(0, 5), row=1, column=2, sticky=(tk.W + tk.E))

# Enter
enter_btn = ttk.Button(add_frame, text="Add", style="basic.TButton", command=capture_shoes)
enter_btn.grid(padx=5, row=3, column=2)

# -----TEXT BOX-----
# To display output with a scrollbar
text_frame = ttk.Frame(top_frame)
text_frame.grid(padx=10, pady=10, ipady=5, ipadx=5, sticky=(tk.W + tk.E))
scroll = ttk.Scrollbar(text_frame)
scroll.pack(side="right", fill="y")
display_data = tk.Text(text_frame, padx=10, pady=10, height=16, width=75,
                       font=("TkDefaultFont", 12), yscrollcommand=scroll.set)
display_data.pack(side="left", fill="x")
scroll.config(command=display_data.yview)

# Populate shoe_list and run event loop
read_shoes_data()
root.mainloop()