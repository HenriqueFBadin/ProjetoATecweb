import json

dict = {"title": "Teste", "descricao": "Teste"}

with open("data/" + "notes.json", 'r') as archive:
    texto = archive.read()
dicionario = json.loads(texto)
dicionario.append(dict)

print(dicionario)
