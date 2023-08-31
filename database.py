import sqlite3

from dataclasses import dataclass


@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''


class Database():
    def __init__(self, name):
        self.conn = sqlite3.connect(name + '.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS note (id INTEGER PRIMARY KEY, title TEXT, content TEXT NOT NULL);')

    def add(self, note):
        self.cursor.execute(
            'INSERT INTO note (title, content) VALUES (?, ?)', (note.title, note.content))
        self.conn.commit()

    def get_all(self):
        cursor = self.conn.execute(
            "SELECT id, title, content FROM note")
        lista = []
        for linha in cursor:
            id = linha[0]
            title = linha[1]
            content = linha[2]
            lista.append(Note(id, title, content))

        return lista

    def get(self, index):
        cursor = self.conn.execute(
            "SELECT id, title, content FROM note")
        for linha in cursor:
            id = linha[0]
            title = linha[1]
            content = linha[2]
            if id == index:
                return Note(title=title, content=content, id=id)
        return None

    def update(self, entry):
        self.cursor.execute(
            'UPDATE note SET title = ?, content = ? WHERE id = ?', (entry.title, entry.content, entry.id))
        self.conn.commit()

    def delete(self, note_id):
        self.cursor.execute('DELETE FROM note WHERE id = ?', (note_id,))
        self.conn.commit()
