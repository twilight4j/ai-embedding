from dotenv import load_dotenv
import oracledb
import os
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# API 키 정보 로드
load_dotenv()

####################################
# 1. Database 연결 및 조회
####################################
# SQL 파일 읽기
sql_path = './.db/oracle/product.sql'
with open(sql_path, 'r', encoding='utf-8') as f:
    sql = f.read().strip()

# Oracle 데이터베이스 연결 정보
connection = oracledb.connect(
    user=os.getenv("ORACLE_USER"),
    password=os.getenv("ORACLE_PASSWORD"),
    host=os.getenv("ORACLE_HOST"),
    port=os.getenv("ORACLE_PORT"),
    sid=os.getenv("ORACLE_SID")
    )

cursor = connection.cursor()
cursor.execute(sql)
rows = cursor.fetchall()

# 연결 종료
cursor.close()
connection.close()

# documents 리스트 생성
documents = []
metadatas = []
ids = []

"""
- 포맷: {BRND_NM}의 {ARTC_INFO}, {GOODS_NM}.
- 예시: 삼성전자의 TV, QLED 8K 스마트TV.
"""
for row in rows:
    GOODS_NO, GOODS_NM, BRND_NM, ARTC_INFO = row
    metadatas.append({"GOODS_NO": GOODS_NO})
    documents.append(f"{BRND_NM}의 {ARTC_INFO}, {GOODS_NM}")
    ids.append(str(GOODS_NO))

####################################
# 2. OpenAI 임베딩 객체 생성 (model 지정)
####################################
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")  # 1536 차원

####################################
# 3. 벡터스토어를 생성합니다.
####################################
# DB 경로 설정
persist_directory = "./.db/faiss"

vectorstore = FAISS.from_texts(
    texts=documents,
    embedding=embeddings,
    metadatas=metadatas,
    ids=ids
)

# 로컬에 저장
vectorstore.save_local(persist_directory)

print(f"총 {len(documents)}개의 상품 정보가 FAISS에 저장되었습니다.")