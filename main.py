from dotenv import load_dotenv

# API 키 정보 로드
load_dotenv()

import sqlite3

# 데이터베이스 연결 정보
db_path = "data/database.sqlite"
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Reviews 테이블에서 최대 1000개 행 조회 쿼리
cursor.execute("SELECT asin AS GOODS_NO, title AS GOODS_NM FROM Product LIMIT 1000")
rows = cursor.fetchall()

# 연결 종료
cursor.close()
connection.close()

# documents 리스트 생성
documents = []
metadatas = []
ids = []

for row in rows:
    GOODS_NO, GOODS_NM = row
    metadatas.append({"GOODS_NO": GOODS_NO})
    documents.append(GOODS_NM)
    ids.append(str(GOODS_NO))


from langchain_openai.embeddings import OpenAIEmbeddings

# OpenAI 임베딩 객체 생성 (model 지정)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")  # 1536 차원

# dimensions 파라미터 설정 (원하는 차원 수로 축소)
# embeddings = OpenAIEmbeddings(
#     model="text-embedding-3-small",
#     dimensions=512  # 512 차원으로 축소 (최대 1536까지 가능)
# )

from langchain_community.vectorstores import Chroma

# ChromaDB 경로 설정
persist_directory = "./.chroma_db"

# ChromaDB에 저장
# 기존 컬렉션이 있으면 불러오고, 없으면 새로 생성
vectorstore = Chroma.from_texts(
    texts=documents,
    embedding=embeddings,
    metadatas=metadatas,
    ids=ids,
    persist_directory=persist_directory,
    collection_name="product_collection",
)

# 변경사항 저장
vectorstore.persist()

print(f"총 {len(documents)}개의 상품 정보가 ChromaDB에 저장되었습니다.")

# 명시적으로 product_collection 컬렉션 불러오기
vectorstore = Chroma(
    persist_directory=persist_directory,
    embedding_function=embeddings,
    collection_name="product_collection",
)

# 검색할 쿼리 설정 (원하는 검색어로 변경 가능)
query = "Suitcase"  # 예시 쿼리: 원하는 검색어로 변경하세요

# 쿼리와 유사한 상품 5개 검색
results_with_score = vectorstore.similarity_search_with_score(
    query=query, k=5  # 반환할 결과 수
)

# 결과 출력
print(f"'{query}'와 유사한 상품 검색 결과 (최대 5개):")
print("-" * 60)

if results_with_score:
    for i, (doc, score) in enumerate(results_with_score, 1):
        print(f"[결과 {i}]")
        print(f"상품명: {doc.page_content}")
        print(f"상품번호: {doc.metadata['GOODS_NO']}")
        print(f"유사도 점수: {score}")  # 낮을수록 더 유사함
        print("-" * 60)
else:
    print("검색 결과가 없습니다.")
