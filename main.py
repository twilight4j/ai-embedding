from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate

# API 키 정보 로드
load_dotenv()

# 1. 데이터베이스 연결 및 조회

# 2. 상품정보를 문맥에 맞게 병합한 `search_text` 를 포함하여 documents 리스트 생성

# 3. 임베딩(Embedding) 생성

# 4. DB 생성(Create DB) 및 저장