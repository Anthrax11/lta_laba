
def read_file() -> list:
    """Чтение файла в оперативную память"""
    with open("data.txt", "r", encoding="utf-8") as f:
        data = [row.strip("\n") for row in f.readlines()] # удаление \n с краев строки
    return data

def parse_line(line: str) -> dict:
    """Парсинг строки из файла,
    удаление пробелов (см. условия)
    """
    return {
        "surname": line[0:30].rstrip(),
        "name": line[30:50].rstrip(),
        "midname": line[50:70].rstrip(),
        "dob": line[70:78].rstrip(),
        "phone": line[78:128].rstrip()
    }

def format_input(ndata: tuple) -> str:
    """Форматирует пользовательский ввод
    в строку для хранения в памяти
    и записи в файл
    """
    new_str = (
        f"{ndata[0]:<30}" +
        f"{ndata[1]:<20}" +
        f"{ndata[2]:<20}" +
        f"{ndata[3]:<8}" +
        f"{ndata[4]:<50}"
    )
    return new_str

