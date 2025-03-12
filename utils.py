import requests
from bs4 import BeautifulSoup #html 등 다른 데이터 형식을 파이썬이 이해하기 쉽게 만들어줌(parsing파싱)
from openai import OpenAI #오픈 ai의 기능을 사용하겠숩니다.
from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def kospi():
    KOSPI_URL = 'https://finance.naver.com/sise/'
    res = requests.get(KOSPI_URL)
    #print(res.text)
    #KOSPI_now

    selector = '#KOSPI_now'
    soup = BeautifulSoup(res.text, 'html.parser')
    kospi = soup.select_one(selector)
    return kospi.text
#kospi 함수


def openai(api_key, user_input):
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {'role': 'system', 'content': '다요미 챗봇이야 너는 다욤어를 활용하는 거야.'}, #system prompting 적절한 세팅 조절 하는 과정
            {'role': 'user', 'content': user_input},
        ]
    )   
    return completion.choices[0].message.content
#openai 함수

def langchain(user_input):
    llm = init_chat_model("gpt-4o-mini", model_provider='openai')
    embeddings = OpenAIEmbeddings(model='text-embedding-3-large')
    vector_store = InMemoryVectorStore(embeddings)

    # 1. load document
    loader = WebBaseLoader(
        web_paths=(
            'https://www.yna.co.kr/view/AKR20250312059000007?input=1195m',
        )
    )
    docs = loader.load()

    #2.split
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    all_splits = text_splitter.split_documents(docs)

    #3.store
    _ = vector_store.add_documents(documents=all_splits)

    #4.retrieve
    prompt = hub.pull('rlm/rag-prompt')
    retrieved_docs = vector_store.similarity_search(user_input)
    docs_content = '\n\n'.join(doc.page_content for doc in retrieved_docs)
    prompt = prompt.invoke({'question': user_input, 'context': docs_content})
    answer = llm.invoke(prompt).content

    return answer

    #langchain 함수설정

