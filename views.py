from utils import load_data, load_template, write_on_file, build_response, extract_route
import urllib.parse
from database import Database
from database import Note


def index(request):

    db = Database('data/banco')

    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    if 'delete' in extract_route(request):
        del_request, id_card = extract_route(request).split('/')
        db.delete(id_card)
        print('deletado')
        return build_response(code=303, reason='See Other', headers='Location: /')

    elif request.startswith('POST'):
        print("Entrou no post")
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[-1]
        params = {}
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus
        titulo = ''
        conteudo = ''
        for chave_valor in corpo.split('&'):
            chave, valor = chave_valor.split('=')
            params[chave] = urllib.parse.unquote_plus(valor)
            if chave == 'titulo':
                titulo = urllib.parse.unquote_plus(valor)
            elif chave == 'conteudo':
                conteudo = urllib.parse.unquote_plus(valor)

        lista = db.get_all()
        for notes in lista:
            if notes.title == titulo or notes.content == conteudo:
                db.delete(notes.id)
                print('removido')

        db.add(Note(title=titulo, content=params[chave]))

        return build_response(code=303, reason='See Other', headers='Location: /')

    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(
            title=dados.title, details=dados.content, id=dados.id)
        for dados in db.get_all()
    ]

    notes = '\n'.join(notes_li)

    return build_response(body=load_template('index.html').format(notes=notes))


def edit(request):

    db = Database('data/banco')

    edit_request, id_card = extract_route(request).split('/')
    print(type(id_card))

    if request.startswith('POST'):
        print('Fazendo o update')
        request = request.replace('\r', '')
        partes = request.split('\n\n')
        corpo = partes[-1]
        params = {}
        titulo = ''
        conteudo = ''
        for chave_valor in corpo.split('&'):
            print(chave_valor.split('='))
            chave, valor = chave_valor.split('=')
            params[chave] = urllib.parse.unquote_plus(valor)
            if chave == 'titulo':
                titulo = urllib.parse.unquote_plus(valor)
                print(titulo)
            elif chave == 'detalhes':
                conteudo = urllib.parse.unquote_plus(valor)
                print(conteudo)

        note = db.get(int(id_card))

        if(titulo == '' and conteudo == ''):
            titulo = note.title
            conteudo = note.content
        elif(titulo == ''):
            titulo = note.title
        elif(conteudo == ''):
            conteudo = note.content

        db.update(Note(title=titulo, content=conteudo, id=id_card))
        print(db.update(Note(title=titulo, content=conteudo, id=id_card)))
        return build_response(code=303, reason='See Other', headers='Location: /')

    id_card = int(id_card)
    print(type(id_card))
    note = db.get(id_card)
    print(note)

    return build_response(body=load_template('edit.html').format(note_title=note.title, note_details=note.content, note_id=note.id))


def erro():
    return build_response(body=load_template('error.html'))
