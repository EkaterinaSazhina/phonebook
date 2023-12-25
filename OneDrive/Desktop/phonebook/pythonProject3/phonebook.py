#Создать телефонный справочник с
#возможностью импорта и экспорта данных в
#формате .txt. Фамилия, имя, отчество, номер
#телефона - данные, которые должны находиться
#в файле.
#1. Программа должна выводить данные
#2. Программа должна сохранять данные в
#текстовом файле
#3. Пользователь может ввести одну из
#характеристик для поиска определенной
#записи(Например имя или фамилию
#человека)
#4. Использование функций. Ваша программа
#не должна быть линейной


def choose_action(phonebook):
    while True:
        print('Меню:')
        user_choice = input('1 - Открыть справочник\n2 - Просмотреть все контакты\n3 - Найти контакт\n4 - Добавить контакт\n\
5 - Изменить контакт\n6 - Удалить контакт\n0 - Выйти из приложения\n')
        print()
        if user_choice == '1':
            file_to_add = input('Введите название импортируемого файла: ')
            import_data(file_to_add, phonebook)
        elif user_choice == '2':
            show_phonebook(phonebook)
        elif user_choice == '3':
            contact_list = read_file_to_dict(phonebook)
            find_number(contact_list)
        elif user_choice == '4':
            add_phone_number(phonebook)
        elif user_choice == '5':
            change_phone_number(phonebook)
        elif user_choice == '6':
            delete_contact(phonebook)
        elif user_choice == '0':
            print('До свидания!')
            break
        else:
            print('Неправильно выбрана команда!')
            print()
            continue


def import_data(file_to_add, phonebook):
    try:
        with open(file_to_add, 'r', encoding='utf-8') as new_contacts, open(phonebook, 'a', encoding='utf-8') as file:
            contacts_to_add = new_contacts.readlines()
            file.writelines(contacts_to_add)
    except FileNotFoundError:
        print(f'{file_to_add} не найден')


def read_file_to_dict(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    headers = ['Имя', 'Фамилия', 'Номер телефона', 'Комментарий']
    contact_list = []
    for line in lines:
        line = line.strip().split()
        contact_list.append(dict(zip(headers, line)))
    return contact_list


def read_file_to_list(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        contact_list = []
        for line in file.readlines():
            contact_list.append(line.split())
    return contact_list


def search_parameters():
    print('По какому полю выполнить поиск?')
    search_field = input('1 - по имени\n2 - по фамилии\n3 - по номеру телефона\n4 - по комментарию\n')
    print()
    search_value = None
    if search_field == '1':
        search_value = input('Введите имя для поиска: ')
        print()
    elif search_field == '2':
        search_value = input('Введите фамилию для поиска: ')
        print()
    elif search_field == '3':
        search_value = input('Введите номер телефона для поиска: ')
        print()
    if search_field == '4':
        search_value = input('Введите комментарий для поиска: ')
        print()
    return search_field, search_value


def find_number(contact_list):
    search_field, search_value = search_parameters()
    search_value_dict = {'1': 'Имя', '2': 'Фамилия', '3': 'Номер телефона', '4': 'Комментарий' }
    found_contacts = []
    for contact in contact_list:
        if contact[search_value_dict[search_field]] == search_value:
            found_contacts.append(contact)
    if len(found_contacts) == 0:
        print('Контакт не найден!')
    else:
        print_contacts(found_contacts)
    print()


def get_new_number():
    first_name = input('Введите Имя: ')
    last_name = input('Введите Фамилию: ')
    phone_number = input('Введите номер телефона: ')
    comment = input('Введите комментарий: ')
    return first_name,last_name, phone_number, comment


def add_phone_number(file_name):
    info = ' '.join(get_new_number())
    with open(file_name, 'a', encoding='utf-8') as file:
        file.write(f'{info}\n')


def show_phonebook(file_name):
    list_of_contacts = sorted(read_file_to_dict(file_name), key=lambda x: x['Имя' ])
    print_contacts(list_of_contacts)
    print()
    return list_of_contacts


def search_to_modify(contact_list: list):
    search_field, search_value = search_parameters()
    search_result = []
    for contact in contact_list:
        if contact[int(search_field) - 1] == search_value:
            search_result.append(contact)
    if len(search_result) == 1:
        return search_result[0]
    elif len(search_result) > 1:
        print('Найдено несколько контактов')
        for i in range(len(search_result)):
            print(f'{i + 1} - {search_result[i]}')
        num_count = int(input('Выберите номер контакта, который нужно изменить/удалить: '))
        return search_result[num_count - 1]
    else:
        print('Контакт не найден')
    print()


def change_phone_number(file_name):
    contact_list = read_file_to_list(file_name)
    number_to_change = search_to_modify(contact_list)
    contact_list.remove(number_to_change)
    print('Какое поле вы хотите изменить? ')
    field = input('1 - Имя\n2 - Фамилия\n3 - Номер телефона\n4 - Комментарий\n')
    if field == '1':
        number_to_change[0] = input('Введите имя: ')
    elif field == '2':
        number_to_change[1] = input('Введите фамилию: ')
    elif field == '3':
        number_to_change[2] = input('Введите номер телефона: ')
    elif field == '4':
        number_to_change[3] = input('Введите комментарий: ')
    contact_list.append(number_to_change)
    with open(file_name, 'w', encoding='utf-8') as file:
        for contact in contact_list:
            line = ' '.join(contact) + '\n'
            file.write(line)


def delete_contact(file_name):
    contact_list = read_file_to_list(file_name)
    number_to_change = search_to_modify(contact_list)
    contact_list.remove(number_to_change)
    with open(file_name, 'w', encoding='utf-8') as file:
        for contact in contact_list:
            line = ' '.join(contact) + '\n'
            file.write(line)


def print_contacts(contact_list: list):
    for contact in contact_list:
        for key, value in contact.items():
            print(f'{key}: {value:12}', end='')
        print()


if __name__ == '__main__':
    file = 'Phonebook.txt'
    choose_action(file)
