#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import sys
import json
import jsonschema


def add(list_man):
    # Запросить данные .
    name = input("Имя:  ")
    number = input("Номер телефона ")
    date_ = input("Дата рождения: ")

    # Создать словарь.
    man = {
        "name": name,
        "number": number,
        "date": date_,
    }

    # Добавить словарь в список.
    list_man.append(man)
    # Отсортировать список.
    if len(list_man) > 1:
        list_man.sort(key=lambda item: item.get("date", ""))
    return list_man


def list_d(list_man):
    if list_man:
        # Заголовок таблицы.
        line = "+-{}-+-{}-+-{}-+-{}-+".format("-" * 4, "-" * 30, "-" * 20, "-" * 20)
        print(line)
        print(
            "| {:^4} | {:^30} | {:^20} | {:^20} |".format(
                "No", "Имя", "Номер телефона", "Дата рождения"
            )
        )
        print(line)

        # Вывести данные о человеке.
        for idx, man in enumerate(list_man, 1):
            print(
                "| {:>4} | {:<30} | {:<20} | {:<20}  |".format(
                    idx, man.get("name", ""), man.get("number", ""), man.get("date", "")
                )
            )

        print(line)
    else:
        print("Список работников пуст: ")


def select(command_d, mans_list):
    parts_ = command_d.split(" ", maxsplit=1)
    sel = parts_[1]
    count = 0
    for man in mans_list:
        if man.get("number") == sel:
            count += 1
            print("{:>4}: {}".format(count, man.get("name", "")))
            print("Номер телефона:", man.get("number", ""))
            print("Дата рождения:", man.get("date", ""))

    # Если счетчик равен 0, то человек не найден.
    if count == 0:
        print("Человек не найден.")


def save_workers(file_name_1, staff):
    with open(file_name_1, "w", encoding="utf-8") as fout:
        json.dump(staff, fout, ensure_ascii=False, indent=4, default=str)


def load_workers(file_name_2):
    schema = {
        "type": "array",
        "items": [
            {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "number": {"type": "string"},
                    "date": {"type": "string"},
                },
                "required": ["name", "number", "date"],
            },
            {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "number": {"type": "string"},
                    "date": {"type": "string"},
                },
                "required": ["name", "number", "date"],
            },
        ],
    }

    with open(file_name_2, "r", encoding="utf-8") as fin:
        loadf = json.load(fin)
        validator = jsonschema.Draft7Validator(schema)
        try:
            if not validator.validate(loadf):
                print("Валидация прошла успешно")
        except jsonschema.exceptions.ValidationError:
            print("Ошибка валидации", file=sys.stderr)
            exit()
        return loadf


def help_d():
    # Вывести справку о работе с программой.
    print("Список команд:\n")
    print("add - добавить человека;")
    print("list - вывести список людей;")
    print("select <товар> - информация о человеке;")
    print("save <имя файла> - сохранение данных в файл")
    print("losd <имя файла> - загрузка даннных из файла")
    print("help - отобразить справку;")
    print("exit - завершить работу с программой.")


if __name__ == "__main__":
    manlist = []
    while True:
        # Запросить команду
        command = input(">>> ").lower()
        if command == "exit":
            break
        elif command == "add":
            manlist = add(manlist)
        elif command == "list":
            list_d(manlist)
        elif command.startswith("select "):
            select(command, manlist)
        elif command.startswith("save "):
            parts = command.split(maxsplit=1)
            file_name = parts[1]
            save_workers(file_name, manlist)
        elif command.startswith("load "):
            parts = command.split(maxsplit=1)
            file_name = parts[1]
            manlist = load_workers(file_name)
        elif command == "help":
            help_d()
        else:
            print("неизвестная команда {command}", file=sys.stderr)
