import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


PERSIST_DIR = "/home/vika/Рабочий стол/MyPythonProjects/chroma_db"
LLM_MODEL = "llama3.2:3b"


app = FastAPI(title="Permian RAG Assistant")

HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>RAG-помощник по Пермскому периоду</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
        }
        input, button {
            padding: 10px;
            font-size: 16px;
        }
        button {
            cursor: pointer;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
        }
        button:hover {
            background: #45a049;
        }
        #answer {
            margin-top: 20px;
            padding: 15px;
            background-color: #f4f4f4;
            border-left: 4px solid #4CAF50;
            min-height: 100px;
        }
    </style>
</head>
<body>
    <h1>RAG-помощник по Пермскому периоду</h1>
    <form id="questionForm">
        <input type="text" id="question" placeholder="Введите ваш вопрос..." size="50" required>
        <button type="submit">Получить ответ</button>
    </form>
    <div id="answer"></div>

    <script>
        const questionForm = document.getElementById("questionForm");
        questionForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const question = document.getElementById("question").value;
            const response = await fetch("/ask", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({question})
            });
            const data = await response.json();
            document.getElementById("answer").innerText = data.answer;
        });
    </script>
</body>
</html>
"""

# объд. чанков в один текст
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# RAG
class PermianRAGSystem:
    def __init__(self, persist_dir: str):
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        
        self.vectorstore = Chroma(
            persist_directory=persist_dir,
            embedding_function=embeddings
        )
        
        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 3}
        )
        
        self.llm = Ollama(
            model=LLM_MODEL,
            temperature=0.05,
            num_predict=100,
            num_thread=4
        )
        
        self.prompt = PromptTemplate(
            template="""
Вопрос: {question}
Данные: {context}
Ответ:""",
            input_variables=["context", "question"]
        )
        # цепочка rag
        self.chain = (
            {
                "context": self.retriever | format_docs,
                "question": RunnablePassthrough()
            }
            | self.prompt # формирование промта
            | self.llm # генерация ответа
            | StrOutputParser() # рез-т в строку
        )
    
    def answer_question(self, question: str) -> str: # метод получения ответа 
        return self.chain.invoke(question)


rag_system = None # синглтон


def get_rag():  
    global rag_system
    if rag_system is None:
        if not os.path.exists(PERSIST_DIR):
            raise RuntimeError(f"База не найдена: {PERSIST_DIR}")
        rag_system = PermianRAGSystem(PERSIST_DIR)
    return rag_system

# маршруты fastapi
@app.get("/")
async def index():
    return HTMLResponse(HTML)


@app.post("/ask") # обработка вопросов, json
async def ask_question(data: dict):
    try:
        rag = get_rag()  # получение rag
        answer = rag.answer_question(data["question"])
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    print("-" * 60)
    print("ПЕРМСКИЙ RAG АССИСТЕНТ")
    print("-" * 60)
    print(f"Модель: {LLM_MODEL}")
    print("http://127.0.0.1:7000")
    print("-" * 60)
    
    uvicorn.run(app, host="127.0.0.1", port=12000)
