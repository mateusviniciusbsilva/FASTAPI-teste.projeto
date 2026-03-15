from fastapi import FastAPI
from datetime import datetime
import sqlite3
app = FastAPI()
conn = sqlite3.connect("tarefas.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tarefa TEXT,
    descricao TEXT,
    data TEXT
)
""")
@app.post("/tarefas")
def adicionar_tarefa(tarefa: str, descricao: str = "sem descrição"):
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO tarefas (tarefa, descricao, data) VALUES (?, ?, ?)",
        (tarefa, descricao, data)
    )
    conn.commit()
    return {"mensagem": "tarefa adicionada com sucesso"}
@app.get("/tarefas")
def listar_tarefas():
    cursor.execute("SELECT * FROM tarefas")
    dados = cursor.fetchall()
    tarefas = []
    for t in dados:
        tarefas.append({
            "id": t[0],
            "tarefa": t[1],
            "descricao": t[2],
            "data": t[3]
        })
    return tarefas
@app.get("/tarefas/{id}")
def buscar_tarefa(id: int):
    cursor.execute("SELECT * FROM tarefas WHERE id = ?", (id,))
    tarefa = cursor.fetchone()
    if tarefa:
        return {
            "id": tarefa[0],
            "tarefa": tarefa[1],
            "descricao": tarefa[2],
            "data": tarefa[3]
        }
    return {"erro": "tarefa não encontrada"}