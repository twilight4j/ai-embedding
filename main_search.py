from dotenv import load_dotenv
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# API 키 정보 로드
load_dotenv()

####################################
# 1. OpenAI 임베딩 객체 생성 (model 지정)
####################################
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")  # 1536 차원

####################################
# 2. Vectorstore 검색
####################################
persist_directory = "./.db/faiss"

vectorstore = FAISS.load_local(
    persist_directory, 
    embeddings, 
    allow_dangerous_deserialization=True)

while True:
    # 검색할 쿼리 입력 받기
    query = input("\n검색어를 입력하세요 (종료하려면 'q' 또는 'quit' 입력): ").strip()
    
    # 종료 조건 확인
    if query.lower() in ['q', 'quit']:
        print("검색을 종료합니다.")
        break
    
    if not query:
        print("검색어를 입력해주세요.")
        continue

    # 쿼리와 유사한 상품 5개 검색
    results_with_score = vectorstore.similarity_search_with_score(
        query=query, k=5  # 반환할 결과 수
    )

    # 결과 출력
    print(f"\n'{query}'와 유사한 상품 검색 결과 (최대 5개):")
    print("-" * 60)

    if results_with_score:
        for i, (doc, score) in enumerate(results_with_score, 1):
            print(f"[결과 {i}] score: {score}") # 낮을수록 더 유사함
            print(f"상품정보: {doc.page_content}")
            # print(f"상품번호: {doc.metadata['GOODS_NO']}")
            print("-" * 60)
    else:
        print("검색 결과가 없습니다.")
