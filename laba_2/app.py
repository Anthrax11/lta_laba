from tkinter import *
from tkinter import messagebox
from file_operations import format_input, parse_line, read_file

# Инициализация глобальных переменных:
laba_name = "ЛТА. Технологии обработки информации. ЛР2"
cur_line = 0            # хранит текущую (отоброжаемую) строку файла
just_started = True     # меняется на False после первого клика

def clear_entry_fields():
    """Удаляет данные из всех полей"""
    surname_ent.delete(0, END)
    name_ent.delete(0, END)
    midname_ent.delete(0, END)
    dob_ent.delete(0, END)
    phone_ent.delete(0, END)

def fill_entry_fields(row: int=0) -> None:
    """Наполняет поля данными из требуемой 
    строки прочитанного файла.
    """
    data_row = data[row]

    surname_ent.insert(0, parse_line(data_row)["surname"])
    name_ent.insert(0, parse_line(data_row)["name"])
    midname_ent.insert(0, parse_line(data_row)["midname"])
    dob_ent.insert(0, parse_line(data_row)["dob"])
    phone_ent.insert(0, parse_line(data_row)["phone"])

def show_info(message: str) -> None:
    """Показывает всплывающее окно 
    с сообщением message
    """
    messagebox.showinfo("Информация", message)

def check_position():
    """При вызове проверяет является ли текущий блок 
    крайним в файле. Если так, деактивирует кнуопку,
    предотвращая возможность уйти за пределы диапазона.
    Выводит сообщение о достижении крайнего блока при условии,
    что программа не запущена только что (должно быть
    совершено хотя бы одно перемещение).
    """
    global cur_line
    if cur_line == 0:
        prev_btn.config(state=DISABLED)
        if not just_started and data:
            show_info("Достигнуто начало файла")
    else:
        prev_btn.config(state=ACTIVE)

    if cur_line+1 >= len(data):
        next_btn.config(state=DISABLED)
        if not just_started and data:
            show_info("Достигнут конец файла")
    else:
        next_btn.config(state=ACTIVE)

def move_line(forward: bool) -> None:
    """Обработчик команды вперёд/назад.
    Если forward==True - обновляет поля следующим
    блоком файла. В противном случае - предыдущим.
    Вызывает функцию check_position() для проверки
    позиции.
    """
    global cur_line
    global just_started
    just_started = False
    clear_entry_fields()
    if forward:
        cur_line += 1
    else:
        cur_line -= 1
    fill_entry_fields(cur_line)
    check_position()

def next_line() -> None:
    """Обработчик клика по кнопке
    Следующий
    """
    move_line(True)
    
def prev_line() -> None:
    """Обработчик клика по кнопке
    Предыдущий
    """
    move_line(False)

def delete_block() -> None:
    """Обработчик клика по кнопке
    Удалить
    """
    global cur_line
    data.remove(data[cur_line])
    if data:
        cur_line = 0
        clear_entry_fields()
        fill_entry_fields()
    else:
        clear_entry_fields()
        cur_line = 0
        check_position()
        del_btn.config(state=DISABLED)
        show_info("Нет данных для отоображения")

def add_block() -> None:
    """Обработчик клика по кнопке
    Добавить
    NOTE: условия задачи не описывают
    как должна работать эта кнопка.
    Установлено поведение схожее с
    удалением.
    """
    global cur_line
    if not '' in data:
        data.append('')
        cur_line = data.index('')
        clear_entry_fields()
        check_position()

def save_changes() -> None:
    """Обработчик клика по кнопке
    Сохранить
    """
    new_data = (
        surname_var.get(),
        name_var.get(),
        midname_var.get(),
        dob_var.get(),
        phone_var.get()
    )
    formatted = format_input(new_data)
    data[cur_line] = formatted

# Конфигурация интерфейса программы

# Поля ввода данных:
root = Tk()
root.title(laba_name)
root.geometry("500x200+500+250")

surname_var = StringVar()
surname_lbl = Label(text="Фамилия", justify=LEFT, width="20", anchor="w")
surname_lbl.grid(row=0, column=0)
surname_ent = Entry(textvariable=surname_var)
surname_ent.grid(row=0, column=1)

name_var = StringVar()
name_lbl = Label(text="Имя", justify=LEFT, width="20", anchor="w")
name_lbl.grid(row=1, column=0)
name_ent = Entry(textvariable=name_var)
name_ent.grid(row=1, column=1)

midname_var = StringVar()
midname_lbl = Label(text="Отчество", justify=LEFT, width="20", anchor="w")
midname_lbl.grid(row=2, column=0)
midname_ent = Entry(textvariable=midname_var)
midname_ent.grid(row=2, column=1)

dob_var = StringVar()
dob_lbl = Label(text="Дата рождения", justify=LEFT, width="20", anchor="w")
dob_lbl.grid(row=3, column=0)
dob_ent = Entry(textvariable=dob_var)
dob_ent.grid(row=3, column=1)

phone_var = StringVar()
phone_lbl = Label(text="Телефон(ы)", justify=LEFT, width="20", anchor="w")
phone_lbl.grid(row=4, column=0)
phone_ent = Entry(textvariable=phone_var)
phone_ent.grid(row=4, column=1)

# кнопки:
prev_btn = Button(text="Предыдущий", anchor="e", command=prev_line)
next_btn = Button(text="Следующий", command=next_line)
prev_btn.grid(row=6, column=0, pady="20")
next_btn.grid(row=6, column=1)

# новые кнопки (ЛР2)
add_btn = Button(text="Добавить", width="16", command=add_block)
del_btn = Button(text="Удалить", width="16", command=delete_block)
save_btn = Button(text="Сохранить", width="16", command=save_changes)
add_btn.grid(row=0, column=3, padx="20")
del_btn.grid(row=1, column=3)
save_btn.grid(row=2, column=3)

# блок вызова программы
data = read_file()      # чтение файла
if data:
    fill_entry_fields() # заполняет поля первым блоком
else:
    data = ['']           # если файл пустой
check_position()        # проверяет, куда можно двигаться

root.mainloop()
