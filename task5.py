import tkinter as tk
from tkinter import messagebox, simpledialog, font

contacts = []

def add_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()
    address = address_entry.get().strip()

    if not name or not phone:
        update_status("Name and Phone are required!", error=True)
        return

    for c in contacts:
        if c['name'].lower() == name.lower() and c['phone'] == phone:
            update_status("Contact already exists!", error=True)
            return

    contacts.append({
        "name": name,
        "phone": phone,
        "email": email,
        "address": address
    })

    update_status(f"Added '{name}' successfully!")
    clear_fields()
    view_contacts()

# View All Contacts
def view_contacts():
    listbox.delete(0, tk.END)
    colors = ["#FFCDD2", "#E1BEE7", "#BBDEFB", "#C8E6C9", "#FFF9C4", "#D7CCC8", "#B2EBF2", "#FFE0B2"]

    for i, contact in enumerate(contacts):
        display = f"{i+1}. {contact['name']} | 📞 {contact['phone']} | 📧 {contact['email']} | 📍 {contact['address']}"
        listbox.insert(tk.END, display)
        color_index = sum(ord(c) for c in contact['name']) % len(colors)
        listbox.itemconfig(i, bg=colors[color_index], fg="#212121")

    update_status(f"Showing {len(contacts)} contacts.")

def search_contact():
    query = simpledialog.askstring("Search", "Enter name or phone number:")
    if not query:
        update_status("Search cancelled.")
        return

    query = query.lower()
    listbox.delete(0, tk.END)
    found = False

    for i, contact in enumerate(contacts):
        if query in contact['name'].lower() or query in contact['phone']:
            display = f"{i+1}. {contact['name']} | 📞 {contact['phone']} | 📧 {contact['email']} | 📍 {contact['address']}"
            listbox.insert(tk.END, display)
            listbox.itemconfig(tk.END, bg="#FFF176", fg="#000000")
            found = True
 
    if not found:
        update_status("No contact found.")
    else:
        update_status("Search complete.")


def delete_contact():
    selection = listbox.curselection()
    if not selection:
        update_status("Select a contact to delete.", error=True)
        return
    index = selection[0]
    confirm = messagebox.askyesno("Delete", "Are you sure you want to delete this contact?")
    if confirm:
        removed = contacts.pop(index)
        view_contacts()
        detail_var.set("")
        update_status(f"Deleted '{removed['name']}'")


def update_contact():
    selection = listbox.curselection()
    if not selection:
        update_status("Select a contact to update.", error=True)
        return

    index = selection[0]
    contact = contacts[index]

    name = simpledialog.askstring("Update Name", "Enter new name:", initialvalue=contact['name'])
    phone = simpledialog.askstring("Update Phone", "Enter new phone:", initialvalue=contact['phone'])
    email = simpledialog.askstring("Update Email", "Enter new email:", initialvalue=contact['email'])
    address = simpledialog.askstring("Update Address", "Enter new address:", initialvalue=contact['address'])

    if name and phone:
        contacts[index] = {
            "name": name.strip(),
            "phone": phone.strip(),
            "email": email.strip() if email else "",
            "address": address.strip() if address else ""
        }
        view_contacts()
        update_status("Contact updated.")
    else:
        update_status("Name and Phone required to update.", error=True)

def clear_fields():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)


def update_status(message, error=False):
    status_var.set(message)
    status_label.config(fg="#D32F2F" if error else "#388E3C")


def on_list_select(event):
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        c = contacts[index]
        detail_var.set(f" Name: {c['name']}\n Phone: {c['phone']}\n Email: {c['email']}\n Address: {c['address']}")
    else:
        detail_var.set("")


def on_enter(e):
    e.widget.config(bg="#FFD54F", fg="#000000")

def on_leave(e):
    btn_colors = {
        add_btn: "#43A047",
        view_btn: "#1E88E5",
        search_btn: "#FDD835",
        update_btn: "#8E24AA",
        delete_btn: "#E53935"
    }
    e.widget.config(bg=btn_colors.get(e.widget, "#cccccc"), fg="white" if e.widget != search_btn else "black")

root = tk.Tk()
root.title("Unique Contact Book")
root.geometry("600x650")
root.configure(bg="#FFFDE7")

app_font = font.Font(family="Comic Sans MS", size=12, weight="bold")


def make_label(text):
    return tk.Label(root, text=text, bg="#FFFDE7", font=app_font)

make_label("Name:").pack(pady=(10, 0))
name_entry = tk.Entry(root, width=60, font=app_font)
name_entry.pack()

make_label("Phone:").pack(pady=(10, 0))
phone_entry = tk.Entry(root, width=60, font=app_font)
phone_entry.pack()

make_label("Email:").pack(pady=(10, 0))
email_entry = tk.Entry(root, width=60, font=app_font)
email_entry.pack()

make_label("Address:").pack(pady=(10, 0))
address_entry = tk.Entry(root, width=60, font=app_font)
address_entry.pack()


add_btn = tk.Button(root, text="Add Contact", bg="#43A047", fg="white", font=app_font, width=20, command=add_contact)
view_btn = tk.Button(root, text="View Contacts", bg="#1E88E5", fg="white", font=app_font, width=20, command=view_contacts)
search_btn = tk.Button(root, text="Search Contact", bg="#FDD835", fg="black", font=app_font, width=20, command=search_contact)
update_btn = tk.Button(root, text="Update Contact", bg="#8E24AA", fg="white", font=app_font, width=20, command=update_contact)
delete_btn = tk.Button(root, text="Delete Contact", bg="#E53935", fg="white", font=app_font, width=20, command=delete_contact)

for btn in [add_btn, view_btn, search_btn, update_btn, delete_btn]:
    btn.pack(pady=6)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)


listbox = tk.Listbox(root, width=80, height=12, font=("Arial", 11), bd=2, relief="groove", highlightthickness=0)
listbox.pack(pady=10)
listbox.bind('<<ListboxSelect>>', on_list_select)

detail_var = tk.StringVar()
detail_label = tk.Label(root, textvariable=detail_var, bg="#F5F5F5", fg="#4E342E", font=("Arial", 11), wraplength=550, justify="left", anchor="w")
detail_label.pack(pady=(0, 15))


status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var, bg="#FFF9C4", fg="#388E3C", font=("Arial", 10, "bold"), anchor="w", relief="sunken", bd=1)
status_label.pack(fill='x', side='bottom')

update_status("Welcome to your unique colorful contact book!")
root.mainloop()
