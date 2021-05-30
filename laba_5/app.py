from tkinter import *
from tkinter import messagebox
from file_operations import format_input, parse_line, read_file, write_file

# Инициализация глобальных переменных:
laba_name = "ЛТА. Технологии обработки информации. ЛР5"
cur_line = 0     # хранит индекс текущей (отоброжаемой) строки файла

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
    global data_indexes

    if cur_line == data_indexes[0]:
        prev_btn.config(state=DISABLED)
    else:
        prev_btn.config(state=ACTIVE)

    if cur_line >= data_indexes[-1]:
        next_btn.config(state=DISABLED)
    else:
        next_btn.config(state=ACTIVE)

def move_line(forward: bool) -> None:
    """Обработчик команды вперёд/назад.
    Если forward==True - обновляет поля следующим
    блоком файла. В противном случае - предыдущим.
    Вызывает функцию check_position() для проверки
    позиции.
    Для реализации функционала фильтрации из ЛР5
    добавлена глобальная переменная data_indexes,
    которая содержит индексы, по которым возможно 
    перемещение. Если фильтры не установлены,
    все индексы данных из файла доступны.
    """
    global data_indexes
    global cur_line

    cur_idx_line = data_indexes.index(cur_line)
    clear_entry_fields()
    if forward:
        jump_to = cur_idx_line + 1
    else:
        jump_to = cur_idx_line - 1
    cur_line = data_indexes[jump_to]
    fill_entry_fields(cur_line)
    check_position()
    if cur_line == data_indexes[0]:
        show_info("Достигнуто начало файла")
    elif cur_line >= data_indexes[-1]:
        show_info("Достигнут конец файла")

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
    Согласно условиям задачи, удаляет
    запись не из файла, а из хранимого в 
    памяти списка data.
    Также проверяет, остались ли данные для отображения.
    """
    global cur_line
    data.remove(data[cur_line])
    cur_line = 0
    if data:
        clear_entry_fields()
        fill_entry_fields()
    else:
        clear_entry_fields()
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
    global data_indexes
    if not '' in data:
        data.append('')
        cur_line = data.index('')
        data_indexes.append(cur_line)
        clear_entry_fields()
        check_position()

def save_changes() -> None:
    """Обработчик клика по кнопке
    Сохранить.
    Забирает данные из полей ввода данных,
    форматирует их в требуемый формат хранения
    и обновляет хранимый в памяти список данных.
    По вызову активирует кнопку "Упаковать",
    позволяющую записать изменения из памяти в файл.
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
    pack_btn.config(state=ACTIVE)

def pack_data() -> None:
    """Обработчик клика по кнопке
    Упаковать.
    Сохраняет хранимые в памяти данные со всеми
    изменениями.
    """
    write_file(data)
    pack_btn.config(state=DISABLED)
    show_info("Изменения сохранены!")

def entry_to_name(entry: str) -> list:
    """Получаем необходимые для отображения/поиска
    параметры по имения виджета на котором
    находится курсор
    """
    entries = {
        "!entry": ["Фамилия", "surname"],
        "!entry2": ["Имя", "name"],
        "!entry3": ["Отчество", "midname"],
        "!entry4": ["Дата рождения", "dob"],
        "!entry5": ["Телефон", "phone"]
    }
    return entries[entry]

def search_window() -> None:
    """Конфигурирует и открывает окно поиска
    в зависимости от того, где находился 
    курсор в момент клика по кнопке "Искать"
    """
    global field
    try:
        focus = root.focus_get().__dict__["_name"]   # имя поля в котором находится курсор
        field = entry_to_name(focus)
    except KeyError:
        show_info("Кликните на поле, по которому хотите совершить поиск")
        return
    search_wdw = Toplevel(root)
    search_wdw.title("Искать")
    search_wdw.geometry("500x100")

    global srch_var
    srch_var = StringVar()
    srch_lbl = Label(search_wdw, width="10", text=field[0])
    srch_ent = Entry(search_wdw, width="50", textvariable=srch_var)
    srch_btn = Button(search_wdw, width="10", text="Искать", command=search_item)
    srch_lbl.grid(row=0, column=0)
    srch_ent.grid(row=0, column=1)
    srch_btn.grid(row=0, column=2)

def search_item() -> None:
    """Выполняет поиск записи по заданному ключу и
    значению по всем записям начиная от отображаемой
    (поиск вперёд).
    """
    global cur_line
    found = False
    for row in range(cur_line+1, len(data)):
        parsed = parse_line(data[row])
        if parsed[field[1]].lower() == srch_var.get().lower():
            found = True
            clear_entry_fields()
            fill_entry_fields(row)
            cur_line = row
            check_position()
            break
    if not found:
        show_info("Запись не найдена")

def set_filters(filt_data: list) -> None:
    """Создает список индексов для переданного
    спискаю. Необходимо для реализации механизма
    фильтрации. Результат работы записывается в 
    глобальную переменную.
    """
    global data_indexes
    data_indexes = list(range(len(filt_data)))

def filter_rows() -> list:
    """Логика кнопки "Фильтр":
    1. Принимает введённые данные в поля фильтрации
    Если оба пустые, сообщает об этом пользователю и
    прерывает работу функции.
    2. Осуществляет поиск по данным в зависимости от
    того, какие из полей заполнены. 
    3. В случае успешного
    поиска наполняет список found_indexes индексами
    соответствующих элементов.
    4. Если ничего не найдено, сообщает об этом пользователю.
    5. Возвращает список индексов (пустой, если ничего не найдено).
    """
    surname = f_surname_var.get()
    name = f_name_var.get()
    found_indexes = []
    if not (surname or name):
        show_info("Введите фамилию или имя")
        return
    for row in range(len(data)):
        parsed = parse_line(data[row])
        if surname and not name:
            if parsed["surname"].lower() == surname.lower():
                found_indexes.append(row)
        elif name and not surname:
            if parsed["name"].lower() == name.lower():
                found_indexes.append(row)
        else:
            if (parsed["surname"].lower() == surname.lower()
            and parsed["name"].lower() == name.lower()):
                found_indexes.append(row)
    if not found_indexes:
        show_info("Не найдено")
    return found_indexes

def apply_filter() -> None:
    """Обработчик клика по кнопке
    Фильтр

    Вызывает функцию filter_rows() которой
    делегированы проверки на наличие ввода.
    Если данные найдены, сужает область навигации
    по данным при помощи навигационной переменной
    data_indexes, которая в обычном состоянии
    (без примененного фильтра) содержит в себе все
    индексы листа данных. При фильтрации эта переменная
    наполняется только индексами объектов, удовлетворяющих
    условиям поиска.
    """
    global cur_line
    global data_indexes

    found = filter_rows()
    if found:
        apply_filter_btn.config(text="Отменить фильтр", command=discard_filter)
        cur_line = found[0]
        clear_entry_fields()
        fill_entry_fields(cur_line)
        data_indexes = found
        check_position()

def discard_filter() -> None:
    """Обработчик нажатия на кнопку
    Отменить фильтр

    Сбрасывает фильтр путём перезаполнения 
    переменной data_indexes всеми доступными индексами 
    листа data.
    """
    set_filters(data)
    apply_filter_btn.config(text="Фильтр", command=apply_filter)
    check_position()

def make_selection() -> list:
    """Осуществляет поиск всех записей и возвращает их
    в виде подготовленному к отображению в списке выборки.
    Также хранит индекс найденной строки.
    """
    raw = filter_rows()
    if raw:
        result = []
        for element in raw:
            res_dict = parse_line(data[element])
            result.append((element, f"{res_dict['surname']} {res_dict['name']}"))
        return result

def selection_window() -> None:
    """Открывает окно "Выборка" при условии
    успешного поиска по имени и/или фамилии.
    Вводит новую глобальную переменную selection,
    представляющую собой список кортежей следующего
    вида: [(индекс, "Имя Фамилия"), ...]
    К этой переменной в дальнейшем обращается
    обработчик клика по элементу click_select
    """
    global select_box
    global selection

    selection = make_selection()
    if not selection:
        return
    select_wdw = Toplevel(root)
    select_wdw.title("Выборка")
    select_wdw.geometry("400x100")

    select_box = Listbox(select_wdw)
    select_box.pack(fill=BOTH)
    for idx, value in selection:
        select_box.insert(idx, value)
    select_box.bind('<Double-1>', click_select)

def click_select(event) -> None:
    """Обработчик клика по элемену из окна
    выборки.
    При помощи глобальной переменной selection
    сопоставляет id "кликнутого" элемента и
    индекс данных. По найденному индексу данных
    выводится соответсвующая запись.
    """
    global cur_line
    
    selected = select_box.curselection()[0]
    selected_idx = selection[selected][0]
    cur_line = selected_idx
    clear_entry_fields()
    fill_entry_fields(cur_line)
    check_position()

# Конфигурация интерфейса программы

# Поля ввода данных:
root = Tk()
root.title(laba_name)
root.geometry("500x300+500+250")

surname_var = StringVar()
surname_lbl = Label(text="Фамилия", justify=LEFT, width="16", anchor="w")
surname_lbl.grid(row=0, column=0)
surname_ent = Entry(textvariable=surname_var, width="40")
surname_ent.grid(row=0, column=1)

name_var = StringVar()
name_lbl = Label(text="Имя", justify=LEFT, width="16", anchor="w")
name_lbl.grid(row=1, column=0)
name_ent = Entry(textvariable=name_var, width="40")
name_ent.grid(row=1, column=1)

midname_var = StringVar()
midname_lbl = Label(text="Отчество", justify=LEFT, width="16", anchor="w")
midname_lbl.grid(row=2, column=0)
midname_ent = Entry(textvariable=midname_var, width="40")
midname_ent.grid(row=2, column=1)

dob_var = StringVar()
dob_lbl = Label(text="Дата рождения", justify=LEFT, width="16", anchor="w")
dob_lbl.grid(row=3, column=0)
dob_ent = Entry(textvariable=dob_var, width="40")
dob_ent.grid(row=3, column=1)

phone_var = StringVar()
phone_lbl = Label(text="Телефон(ы)", justify=LEFT, width="16", anchor="w")
phone_lbl.grid(row=4, column=0)
phone_ent = Entry(textvariable=phone_var, width="40")
phone_ent.grid(row=4, column=1)

# кнопки Предыдущий/Следующий:
prev_btn = Button(text="Предыдущий", anchor="e", command=prev_line)
next_btn = Button(text="Следующий", command=next_line)
prev_btn.grid(row=6, column=0, pady="10")
next_btn.grid(row=6, column=1, sticky="w")

# новые кнопки (ЛР2)
add_btn = Button(text="Добавить", width="12", command=add_block)
del_btn = Button(text="Удалить", width="12", command=delete_block)
save_btn = Button(text="Сохранить", width="12", command=save_changes)
add_btn.grid(row=0, column=3, padx="20")
del_btn.grid(row=1, column=3)
save_btn.grid(row=2, column=3)

# кнопка упаковать (ЛР3)
pack_btn = Button(text="Упаковать", width="12", state=DISABLED, command=pack_data)
pack_btn.grid(row=3, column=3)

# кнопка искать (ЛР4)
search_btn = Button(text="Искать...", width="12", command=search_window)
search_btn.grid(row=6, column=3)

# секция фильтр (ЛР5):
# - рамка для фильтра и выборки
filter_wig = LabelFrame(root, text="Условие", height="60")
filter_wig.grid(row=7, columnspan=4, sticky="nsew")

# - кнопки и окна фильтра и выборки
f_surname_var = StringVar()
f_surname_lbl = Label(filter_wig, text="Фамилия", justify=LEFT, width="16", anchor="w")
f_surname_lbl.grid(row=0, column=0, pady="2")
f_surname_ent = Entry(filter_wig, textvariable=f_surname_var, width="40")
f_surname_ent.grid(row=0, column=1)

f_name_var = StringVar()
f_name_lbl = Label(filter_wig, text="Имя", justify=LEFT, width="16", anchor="w")
f_name_lbl.grid(row=1, column=0)
f_name_ent = Entry(filter_wig, textvariable=f_name_var, width="40")
f_name_ent.grid(row=1, column=1)

apply_filter_btn = Button(filter_wig, text="Фильтр", width="14", command=apply_filter)
apply_filter_btn.grid(row=0, column=3, padx="20")
select_btn = Button(filter_wig, text="Выборка", width="14", command=selection_window)
select_btn.grid(row=1, column=3)

# блок вызова программы
data = read_file()                      # чтение файла
if data:
    fill_entry_fields()                 # заполняет поля первым блоком
else:
    data = ['']                         # если файл пустой
set_filters(data)                       # установка
check_position()                        # проверяет, куда можно двигаться

root.mainloop()
