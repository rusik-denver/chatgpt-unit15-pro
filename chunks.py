from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from dotenv import load_dotenv
from openai import OpenAI
import os
import re
import requests


# получим переменные окружения из .env
load_dotenv()

# API-key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# задаем system
default_system = "Ты-консультант в компании Simble, ответь на вопрос клиента на основе документа с информацией. Не придумывай ничего от себя, отвечай максимально по документу. Не упоминай Документ с информацией для ответа клиенту. Клиент ничего не должен знать про Документ с информацией для ответа клиенту"


class Chunk():

    def __init__(self, file_url:str, sep:str=" ", ch_size:int=1024):

        match_ = re.search('/document/d/([a-zA-Z0-9-_]+)', file_url)
        if match_ is None:
            raise ValueError('Invalid Google Docs URL')
        doc_id = match_.group(1)

        # Download the document as plain text
        response = requests.get(f'https://docs.google.com/document/d/{doc_id}/export?format=txt')
        response.raise_for_status()
        document = response.text

        # создаем список чанков
        source_chunks = []
        splitter = RecursiveCharacterTextSplitter(chunk_size=ch_size, chunk_overlap=0)
        for chunk in splitter.split_text(document):
            source_chunks.append(Document(page_content=chunk, metadata={}))

        # создаем индексную базу
        embeddings = OpenAIEmbeddings()
        self.db = FAISS.from_documents(source_chunks, embeddings)

    def get_answer(self, system:str = default_system, query:str = None):
        '''Функция получения ответа от chatgpt
        '''
        # релевантные отрезки из базы
        docs = self.db.similarity_search(query, k=4)
        message_content = '\n'.join([f'{doc.page_content}' for doc in docs])
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": f"Ответь на вопрос клиента на основании предоставленной информации. Не упоминай документ с информацией для ответа клиенту в ответе. Документ с информацией для ответа клиенту: {message_content}\n\nВопрос клиента: \n{query}"}
        ]

        # получение ответа от chatgpt
        completion = client.chat.completions.create(model="gpt-3.5-turbo",
                                                  messages=messages,
                                                  temperature=0)

        return completion.choices[0].message.content