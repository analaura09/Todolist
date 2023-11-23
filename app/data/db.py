from flask import Flask, render_template, request
from google.cloud import firestore


app = Flask(__name__)

# Configurar o Firestore
db = firestore.Client.from_service_account_json(config)

tarefas_ref = db.collection('tarefas')

def add_tarefa(titulo, descricao):
    titulo = titulo
    descricao = descricao

    db.collection('tarefas').add({
        'titulo': titulo,
        'descricao': descricao
    })

add_tarefa('aaa', 'aaa')
