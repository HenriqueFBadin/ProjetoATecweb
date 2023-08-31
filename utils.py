import json
from database import Database
from database import Note

def extract_route(string):
    string_list = string.split(' ')
    route = string_list[1]
    new_string = route[1:]
    return new_string


def read_file(path):
    with open(path, 'rb') as f:
        return f.read()


def load_data(db):
    return db.get_all()


def load_template(template):
    with open("templates/" + template, 'r', encoding='utf-8') as archive:
        html = archive.read()
    return html


def write_on_file(path, dict):
    dicionario = load_data(path)
    dicionario.append(dict)
    with open("data/" + path, 'w', encoding='utf-8') as archive:
        return archive.write(json.dumps(dicionario, indent=4))


def build_response(body='', code=200, reason='OK', headers=''):
    response = ""
    if headers == '':
        response = "HTTP/1.1 " + str(code) + " " + \
            reason + headers + "\n\n" + body
    else:
        response = "HTTP/1.1 " + str(code) + " " + \
            reason + "\n" + headers + "\n\n" + body
    return str(response).encode()
