from json import JSONDecodeError
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]
    shuffle(password_list)

    password = "".join(password_list)

    entry_password.delete(0, END)  # Clear any existing text
    entry_password.insert(0, password)  # Insert the new password
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website_data = entry_website.get()
    email_uname_data = entry_email_uname.get()
    password_data = entry_password.get()
    new_data = {
        website_data: {
            "email":email_uname_data,
            "password": password_data,
        }
    }
    if website_data != "" and password_data != "" and email_uname_data !="":
        is_ok = messagebox.askokcancel(title=website_data, message=f"These are the details entered: \nEmail: {email_uname_data} \nPassword: {password_data} \nIs it ok to save?")

        if is_ok:
            try:
                with open("data.json", "r") as file:
                    try:
                        data = json.load(file)  # Load existing data
                    except json.JSONDecodeError:
                        data = {}  # If file is invalid, initialize empty dictionary
            except FileNotFoundError:
                data = {}  # If file doesn't exist, initialize empty dictionary

            if website_data in data:
                messagebox.showinfo(
                    title="Duplicate Entry",
                    message=f"An entry for {website_data} already exists."
                )
            else:
                data.update(new_data)  # Add new entry to data

                with open("data.json", "w") as file:
                    json.dump(data, file, indent=4)  # Save updated data

                entry_website.delete(0, END)
                entry_password.delete(0, END)
    else:
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty")

# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search():
    website_data = entry_website.get()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            print(data[website_data]["email"])
            email = data[website_data]["email"]
            password = data[website_data]["password"]
            messagebox.showinfo(
                title=f"{entry_website.get()}",
                message=f"Email: {email} \nPassword: {password}"
            )
    except KeyError:
        messagebox.showwarning(title="Oops", message="No Website Found")
    except json.JSONDecodeError:
        messagebox.showwarning(title="Oops", message="No File Found")
    except FileNotFoundError:
        messagebox.showwarning(title="Oops", message="No File Found")
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Generator")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
tomato_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=tomato_img)
canvas.grid(column=1, row=0)

label_website = Label(text="Website:")
label_website.grid(column=0, row=1)

entry_website = Entry()
entry_website.grid(column=1, row=1, columnspan=2, sticky="EW")
entry_website.focus()

label_email_uname = Label(text="Email/Username:")
label_email_uname.grid(column=0, row=2)

entry_email_uname = Entry()
entry_email_uname.grid(column=1, row=2, columnspan=2, sticky="EW")

label_password = Label(text="Password:")
label_password.grid(column=0, row=3)

entry_password = Entry()
entry_password.grid(column=1, row=3, sticky="EW")

generate_btn = Button(text="Generate Password", command=generate_password)
generate_btn.grid(column=2, row=3, sticky="EW")

add_btn = Button(text="Add", width=35, command=save)
add_btn.grid(column=1, row=4, columnspan=2, sticky="EW")

search_btn = Button(text="Search", command=search)
search_btn.grid(column=2, row=1, sticky="EW")

mainloop()







window.mainloop()