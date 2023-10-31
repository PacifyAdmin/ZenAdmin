import tkinter as tk
from tkinter import filedialog
import subprocess
import sys

def open_list():
    global current_file
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        current_file = file_path
        with open(current_file, 'r') as file:
            text.delete('1.0', tk.END)
            text.insert('1.0', file.read())
        update_title()
        update_checkbuttons()

def execute_commands(commands):
    command_list = commands.split(',')
    for command in command_list:
        try:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = result.stdout
            text.insert(tk.END, f"Выполнено: {command}\n")
            text.insert(tk.END, f"Выывод:\n{output}\n")
        except subprocess.CalledProcessError as e:
            text.insert(tk.END, f"Ошибка выполнения команды: {command}\n")
            text.insert(tk.END, f"Ошибка:\n{e.stderr}\n")

def create_checkbuttons_from_current_file():
    with open(current_file, 'r') as file:
        entries = file.read().splitlines()
        checkbuttons = []

        for entry in entries:
            entry_parts = entry.split('(', 1)
            if len(entry_parts) == 2:
                name, commands_part = entry_parts[1].split(')', 1)
                if '[' in commands_part and ']' in commands_part:
                    commands = commands_part[commands_part.find('[') + 1:commands_part.rfind(']')]
                    var = tk.BooleanVar()

                    checkbutton = tk.Checkbutton(checkbutton_frame, text=name, variable=var)
                    checkbuttons.append((var, commands))
                    checkbutton.pack(anchor='w')

        return checkbuttons

def update_checkbuttons():
    global checkbuttons
    for widget in checkbutton_frame.winfo_children():
        widget.destroy()
    checkbuttons = create_checkbuttons_from_current_file()

def execute_selected_commands():
    for var, commands in checkbuttons:
        if var.get():
            execute_commands(commands)

def open_zenadmin_sudo():
    try:
        result = subprocess.run(["python", "ZenAdmin_sudo.py"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
        text.insert(tk.END, "Выполнено ZenAdmin_sudo.py\n")
        text.insert(tk.END, f"Вывод:\n{output}\n")
    except subprocess.CalledProcessError as e:
        text.insert(tk.END, "Ошибка выполнения ZenAdmin_sudo.py\n")
        text.insert(tk.END, f"Ошибка:\n{e.stderr}\n")

def update_title():
    if current_file:
        root.title(f"ZenAdmin - {current_file}")
    else:
        root.title("ZenAdmin")

root = tk.Tk()
root.title("ZenAdmin")
root.geometry("800x600")
root.configure(bg='#f0f0f0')
root.resizable(False, False)  # Запретить растягивание окна

# Создаем фрейм для списка чекбоксов
checkbutton_frame = tk.Frame(root, bg='#f0f0f0')
checkbutton_frame.pack(side='left', fill='y', padx=10, pady=10)

# Размещение виджетов
text = tk.Text(root, wrap=tk.NONE)
text.pack(side='top', fill='both', expand=True, padx=10, pady=10)

bg_image = tk.PhotoImage(file='img/wp.png')
bg_label = tk.Label(root, image=bg_image)
bg_label.pack(side='top', fill='both', expand=True, padx=10, pady=10)

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Файл", menu=file_menu)
file_menu.add_command(label="Открыть список", command=open_list)
file_menu.add_command(label="Открыть ZenEditor", command=open_zenadmin_sudo)
file_menu.add_separator()
file_menu.add_command(label="Выход", command=root.quit)


current_file = "list.txt"
checkbuttons = create_checkbuttons_from_current_file()

execute_button = tk.Button(root, text="Start", command=execute_selected_commands)
execute_button.config(width=30, height=1, padx=10, pady=10)
execute_button.place(relx=0.835, rely=0.98, anchor='s')

root.mainloop()
