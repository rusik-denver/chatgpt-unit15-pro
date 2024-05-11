from fastapi import FastAPI
from chunks import Chunk
from pydantic import BaseModel

# инициализация индексной базы
# chunk = Chunk(path_to_base="Simble.txt")
chunk = Chunk(file_url="https://docs.google.com/document/d/11MU3SnVbwL_rM-5fIC14Lc3XnbAV4rY1Zd_kpcMuH4Y")
counter = 0
system = 'Ты - нейро-консультант по правилам страхования ответственности аэропортов и авиационных товаропроизводителей. Тебе будет предоставлена следующая информация: актуальный вопрос клиента и документ с информацией для ответа клиенту. Твоя задача - давать клиенту исчерпывающий и точный ответ. В своих ответах основывайся только на предоставленной тебе информации из документа, но не сообщай клиенту о документе, клиент ничего не должен знать о документе с информацией для ответа. Ничего не придумывай от себя. Не должен присутствовать знак переноса строки, заменяй его пробелом. На вопросы, не связанные с информацией из предоставленного документа давай короткий ответ: "Извините, но этот вопрос вне моей компетенции."'

# класс с типами данных параметров 
class Item(BaseModel): 
    text: str

# создаем объект приложения
app = FastAPI()

# функция обработки get запроса + декоратор 
@app.get("/")
def read_root():
    return {"message": "answer"}

@app.get("/requests-counter/")
def requests_counter():
    return {'requests counter': counter}

@app.post("/api/get_answer")
def get_answer(question: Item):
    global counter
    counter += 1
    print(f'Запрос №{counter}')
    answer = chunk.get_answer(system=system, query=question.text)
    return {"message": answer}
