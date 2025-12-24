import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings

DOCUMENTS_DIR = "/home/vika/Рабочий стол/MyPythonProjects/wikipedia_articles"
PERSIST_DIR = "/home/vika/Рабочий стол/MyPythonProjects/chroma_db"

def main():
    print("Проверка и создание векторной базы")
    
    #  есть ли база
    if os.path.exists(PERSIST_DIR):
        try:
            #  загрузка существующей базы
            embeddings = OllamaEmbeddings(model="nomic-embed-text")
            db = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
            count = db._collection.count()
            print(f" База уже существует. Чанков: {count}")
            return db
        except:
            print("База повреждена, создаем новую")
            import shutil
            shutil.rmtree(PERSIST_DIR)
    
    #  есть ли документы
    if not os.path.exists(DOCUMENTS_DIR):
        print(f" Папка с документами не найдена: {DOCUMENTS_DIR}")
        return None
    
    # Загрузка  документов
    loader = DirectoryLoader(
        DOCUMENTS_DIR,
        glob="**/*.txt",
        loader_cls=TextLoader
    )
    documents = loader.load()
    
    if len(documents) == 0:
        print(" Нет документов для обработки")
        return None
    
    print(f"Документов: {len(documents)}")
    
    # Разделение на чанки
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)
    print(f"Чанков: {len(chunks)}")
    
    # Создание эмбеддингов в базу
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )
    
    print(f" База создана. Чанков: {db._collection.count()}")
    return db

if __name__ == "__main__":
    main()