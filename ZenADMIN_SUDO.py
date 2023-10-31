import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

current_file = None  # Для хранения текущего открытого файла

# Функция для создания нового списка
def create_list():
    listbox.delete(0, tk.END)

# Функция для открытия существующего списка из файла
def open_list():
    global current_file
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            listbox.delete(0, tk.END)
            for line in file:
                listbox.insert(tk.END, line.strip())
        current_file = file_path
        update_title()

# Функция для добавления новой строки в список
def add_entry():
    name = entry_name.get()
    commands = entry_commands.get()

    if name and commands:
        number = len(listbox.get(0, tk.END)) + 1
        listbox.insert(tk.END, f"{number}:({name})[chcp 65001, {commands}]")
        entry_name.delete(0, tk.END)
        entry_commands.delete(0, tk.END)

# Функция для редактирования выбранной строки
def edit_entry():
    selected_index = listbox.curselection()
    if selected_index:
        selected_index = selected_index[0]
        updated_entry = f"{selected_index + 1}:({entry_name.get()})[chcp 65001, {entry_commands.get()}]"
        listbox.delete(selected_index)
        listbox.insert(selected_index, updated_entry)
    else:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите строку для редактирования")

# Функция для удаления выбранной строки
def delete_entry():
    selected_index = listbox.curselection()
    if selected_index:
        listbox.delete(selected_index)
    else:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите строку для удаления")

# Функция для сохранения списка в файл
def save_list():
    global current_file
    if current_file:
        with open(current_file, 'w') as file:
            for item in listbox.get(0, tk.END):
                file.write(item + '\n')
    else:
        save_list_as()

# Функция для сохранения списка в файл с указанием имени
def save_list_as():
    global current_file
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            for item in listbox.get(0, tk.END):
                file.write(item + '\n')
        current_file = file_path
        update_title()

# Функция для обновления заголовка окна
def update_title():
    if current_file:
        root.title(f"ZenEditor - {current_file}")
    else:
        root.title("ZenEditor")

# Создание главного окна
root = tk.Tk()
root.title("ZenEditor")
root.configure(bg='gray20')  # Установка фона на тёмно-серый

# Создание элементов интерфейса
label_name = tk.Label(root, text="Название", bg='gray20', fg='white')
entry_name = tk.Entry(root, width=20)
label_commands = tk.Label(root, text="Команды", bg='gray20', fg='white')
entry_commands = tk.Entry(root, width=30)
add_button = tk.Button(root, text="\u2795", command=add_entry, font=("Symbola", 12), bg='gray20', fg='white')
edit_button = tk.Button(root, text="\u270E", command=edit_entry, font=("Symbola", 12), bg='gray20', fg='white')
delete_button = tk.Button(root, text="\u274C", command=delete_entry, font=("Symbola", 12), bg='gray20', fg='white')
listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=50, bg='gray30', fg='white')

# Размещение элементов интерфейса
label_name.grid(row=0, column=0)
entry_name.grid(row=0, column=1, columnspan=2)
label_commands.grid(row=0, column=3)
entry_commands.grid(row=0, column=4, columnspan=3)
add_button.grid(row=0, column=7)
edit_button.grid(row=1, column=7)
delete_button.grid(row=2, column=7)
listbox.grid(row=1, column=0, rowspan=3, columnspan=7)

# Создание меню
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Меню "Файл"
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Файл", menu=file_menu)
file_menu.add_command(label="Создать список", command=create_list)
file_menu.add_command(label="Открыть список", command=open_list)
file_menu.add_separator()
file_menu.add_command(label="Сохранить", command=save_list)
file_menu.add_command(label="Сохранить как", command=save_list_as)
file_menu.add_separator()
file_menu.add_command(label="Выход", command=root.quit)

# Запуск главного цикла
root.mainloop()