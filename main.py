import re
from pprint import pprint
import csv


def parse_row(f_item, f_pattern_data, f_pattern_phone, f_pattern_email):
    """
    Function get a list and patterns and returns list with parsed values
    :param f_item:
    :param f_pattern_data:
    :param f_pattern_phone:
    :param f_pattern_email:
    :return:
    """
    phone_prefix = ''
    phone_add = ''
    check_str = ','.join(f_item)
    data = re.search(f_pattern_data, check_str)
    phone = re.search(f_pattern_phone, check_str)
    email = re.search(f_pattern_email, check_str)
    # Check phone and create +7 prefix and additional number
    if phone:
        phone_prefix = phone.group(1) if phone.group(1) == '+7' else '+7'
        phone_add = ' доб.' + phone.group(7) + '.' if phone.group(7) else ''
    if data:
        return [data.group(1),
                data.group(2),
                data.group(3) if data.group(3) else '',
                data.group(4).replace(',', '') if data.group(4) else '',
                data.group(5).replace(',', '') if data.group(5) else '',
                phone_prefix + '(' + phone.group(2) + ')' + phone.group(3) + phone.group(4) + phone.group(5) + phone_add
                if phone else '',
                email.group(1) + '@' + email.group(2) if email else '']
    else:
        return []


def rebuild_address_book(contact_list, fn_pattern_data, fn_pattern_phone, fn_pattern_email):
    """
    Function gets list of contacts and patterns and returns normalized address book
    :param contact_list:
    :param fn_pattern_data:
    :param fn_pattern_phone:
    :param fn_pattern_email:
    :return:
    """
    contact_list_rebuild = []
    index = None
    for item in contact_list:
        check_list = parse_row(item, fn_pattern_data, fn_pattern_phone, fn_pattern_email)
        if check_list:
            for ind, elem in enumerate(contact_list_rebuild):
                if check_list[0] == elem[0] and check_list[1] == elem[1]:
                    index = ind
            if index:
                for ind, data_position in enumerate(contact_list_rebuild[index]):
                    if not data_position:
                        contact_list_rebuild[index][ind] = check_list[ind]
                index = None
            else:
                contact_list_rebuild.append(check_list)
    return contact_list_rebuild


if __name__ == '__main__':
    pattern_phone = r"(\+?[7|8])[ |(]*(\d{3})[)| |(|-]*(\d{3})[ |-]?(\d{2})[ |-]?(\d{2})([ ]?[(]?доб\. (\d*))?"
    pattern_email = r"([\w|\.]+)@([\w|\.]+)"
    pattern_data = r"([а-яА-Я]+)[ ,]([а-яА-Я]+)[ ,]([а-яА-Я]*),,?,?([а-яА-Я]*),([\D]*),"

    with open("phonebook_raw.csv", encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    contacts_list_rebuild = rebuild_address_book(contacts_list, pattern_data, pattern_phone, pattern_email)

    pprint(contacts_list_rebuild)

    with open("output_phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list_rebuild)
