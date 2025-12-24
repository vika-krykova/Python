import os
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma

class FastPhi3RAG:
    def __init__(self, vectorstore, model: str = "llama3.2:3b"):
        self.vectorstore = vectorstore
        self.llm = Ollama(
            model=model,
            base_url="http://localhost:11434",
            temperature=0.05,
            num_predict=100,
            num_thread=4
        )
    
    def _get_context(self, question: str) -> str:
        docs = self.vectorstore.similarity_search(question, k=3)
        if not docs:
            return "нет данных"
        
        text = docs[0].page_content
        if len(text) > 120:
            text = text[:120] + "..."
        return text
    
    def answer_question(self, question: str) -> Dict:
        context = self._get_context(question)
        prompt = f"Вопрос: {question}\nДанные: {context}\nОтвет:"
        answer = self.llm.invoke(prompt)
        
        return {
            "question": question,
            "answer": answer,
            "context_used": context
        }

class RAGEvaluator:
    def __init__(self):
        self.vectorizer = CountVectorizer()
    
    def get_test_questions(self) -> List[Dict]:
        return [
            {
                "question": "сколько продолжался пермский период", 
                "keywords": ["47", "миллионов", "лет", "299", "252"]
            },
            {
                "question": "Дата начала пермского периода", 
                "keywords": ["299", "миллионов", "лет", "начало"]
            },
            {
                "question": "каким был климат в пермский период", 
                "keywords": ["сухой", "засушливый", "пустынный"]
            },
            {
                "question": "что вызвало вымирание", 
                "keywords": ["вулканизм", "сибирские", "траппы"]
            },
            {
                "question": "какие животные были доминирующими", 
                "keywords": ["терапсиды", "пеликозавры", "рептилии"]
            },
        ]
    
    def evaluate_answer(self, answer: str, keywords: List[str]) -> float:
        if not answer or "нет данных" in answer.lower():
            return 0.0
        
        answer_lower = answer.lower()
        found = sum(1 for kw in keywords if kw.lower() in answer_lower)
        return found / len(keywords) if keywords else 0.0
    
    def evaluate_cosine(self, answer: str, keywords: List[str]) -> float:
        if not answer:
            return 0.0
        
        ideal = " ".join(keywords)
        try:
            matrix = self.vectorizer.fit_transform([ideal, answer])
            return cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
        except:
            return 0.0

# оценка с выводом ответов
def evaluate_systems(chroma_db: Chroma):
    evaluator = RAGEvaluator()
    questions = evaluator.get_test_questions()
    
    # RAG система
    rag = FastPhi3RAG(chroma_db, "llama3.2:3b")
    
    # Обычный LLM
    llm = Ollama(model="llama3.2:3b", temperature=0.05, num_predict=100, num_thread=4)
    
    rag_scores = []
    llm_scores = []
    
    print("\n" + "-"*60)
    print("Оценка систем")
    print("-"*60)
    
    for i, q in enumerate(questions):
        print(f"\n{'═'*50}")
        print(f"Вопрос {i+1}: {q['question']}")
        print(f"Ключевые слова: {', '.join(q['keywords'])}")
        print(f"{'─'*50}")
        
        # RAG ответ
        rag_result = rag.answer_question(q["question"])
        rag_answer = rag_result["answer"]
        print(f" RAG ответ:")
        print(f"   {rag_answer}")
        
        # LLM ответ
        llm_answer = llm.invoke(q["question"])
        print(f" LLM без RAG ответ:")
        print(f"   {llm_answer}")
        
        # Оценки
        rag_keyword_score = evaluator.evaluate_answer(rag_answer, q["keywords"])
        rag_cosine_score = evaluator.evaluate_cosine(rag_answer, q["keywords"])
        rag_combined = (rag_keyword_score + rag_cosine_score) / 2
        rag_scores.append(rag_combined)
        
        llm_keyword_score = evaluator.evaluate_answer(llm_answer, q["keywords"])
        llm_cosine_score = evaluator.evaluate_cosine(llm_answer, q["keywords"])
        llm_combined = (llm_keyword_score + llm_cosine_score) / 2
        llm_scores.append(llm_combined)
        
        print(f"\n Оценки:")
        print(f"   RAG: {rag_combined:.3f} (ключ.слова: {rag_keyword_score:.3f}, косинус: {rag_cosine_score:.3f})")
        print(f"   LLM: {llm_combined:.3f} (ключ.слова: {llm_keyword_score:.3f}, косинус: {llm_cosine_score:.3f})")
    
    # Визуализация
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(questions))
    width = 0.35
    
    ax.bar(x - width/2, rag_scores, width, label='RAG система', color='skyblue')
    ax.bar(x + width/2, llm_scores, width, label='LLM без RAG', color='lightcoral')
    
    ax.set_xlabel('Вопросы')
    ax.set_ylabel('Оценка (ключ.слова + косинус)')
    ax.set_title('Сравнение качества RAG и обычного LLM')
    ax.set_xticks(x)
    ax.set_xticklabels([f'Q{i+1}' for i in range(len(questions))])
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Средние значения
    rag_avg = np.mean(rag_scores)
    llm_avg = np.mean(llm_scores)
    
    ax.axhline(y=rag_avg, color='blue', linestyle='--', alpha=0.5, label=f'RAG среднее: {rag_avg:.3f}')
    ax.axhline(y=llm_avg, color='red', linestyle='--', alpha=0.5, label=f'LLM среднее: {llm_avg:.3f}')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('rag_vs_llm.png', dpi=100)
    
    print(f"\n{'-'*60}")
    print("ИТОГОВЫЕ РЕЗУЛЬТАТЫ:")
    print(f"Средняя оценка RAG: {rag_avg:.3f}")
    print(f"Средняя оценка LLM: {llm_avg:.3f}")
    print(f"График сохранен как 'rag_vs_llm.png'")
    print(f"{'-'*60}")
    
    return rag_scores, llm_scores, rag_avg, llm_avg

def main():
    PERSIST_DIR = "/home/vika/Рабочий стол/MyPythonProjects/chroma_db"
    
    if not os.path.exists(PERSIST_DIR):
        print(f"База не найдена: {PERSIST_DIR}")
        return
    
    print("-" * 50)
    print("RAG система")
    print("-" * 50)
    
    # Загрузка базы
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    chroma_db = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    print(f" Чанков в базе: {chroma_db._collection.count()}")
    
    # Проверка что база работает
    print("\n🔍 Проверка поиска в базе:")
    test_docs = chroma_db.similarity_search("пермский период", k=2)
    if test_docs:
        source = test_docs[0].metadata.get('source', 'Unknown')
        print(f"Найден документ: {source}")
        print(f"Первые 150 символов: {test_docs[0].page_content[:150]}...")
    else:
        print(" Поиск ничего не дал")
        return
    
    # Создание RAG
    rag = FastPhi3RAG(chroma_db, "llama3.2:3b")
    
    # Тестовый вопрос
    print("\n" + "="*50)
    print("Вопрос для теста")
    print("="*50)
    test_result = rag.answer_question("Что такое Пермский период??")
    print(f"Вопрос: {test_result['question']}")
    print(f"Ответ: {test_result['answer']}")
    print(f"Использованный контекст: {test_result['context_used']}")
    
    # Оценка систем
    evaluate_systems(chroma_db)
    
    # Дополнительные вопросы
    print("\n" + "-"*50)
    print("Вопросы")
    print("-"*50)
    
    extra_questions = [
        "Какие растения были в Пермском периоде?",
        "Какая была атмосфера?",
        "Как Пермский период повлиял на эволюцию?"
    ]
    
    for q in extra_questions:
        print(f"\n {q}")
        result = rag.answer_question(q)
        print(f" {result['answer']}")
        print("-" * 40)

if __name__ == "__main__":
    main()