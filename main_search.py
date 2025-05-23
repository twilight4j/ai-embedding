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

    # 필터링 옵션 입력 받기
    filter_option = input("필터링을 사용하시겠습니까? (y/n): ").strip().lower()
    filter_dict = None
    
    if filter_option == 'y':
        print("\n필터링 옵션:")
        print("1. 상품번호로 필터링")
        print("2. 카테고리로 필터링")
        filter_choice = input("선택하세요 (1/2): ").strip()
        
        if filter_choice == '1':
            goods_no = input("상품번호를 입력하세요: ").strip()
            filter_dict = {"GOODS_NO": goods_no}
        elif filter_choice == '2':
            category = input("카테고리를 입력하세요: ").strip()
            filter_dict = {"CATEGORY": category}

    # 쿼리와 유사한 상품 5개 검색 (필터 적용)
    results_with_score = vectorstore.similarity_search_with_score(
        query=query, 
        k=5,  # 반환할 결과 수
        filter=filter_dict  # 메타데이터 필터 적용
    )

    # 결과 출력
    print(f"\n'{query}'와 유사한 상품 검색 결과 (최대 5개):")
    print("-" * 60)

    if results_with_score:
        for i, (doc, score) in enumerate(results_with_score, 1):
            print(f"[결과 {i}] score: {score}") # 낮을수록 더 유사함
            print(f"상품정보: {doc.page_content}")
            print(f"메타데이터: {doc.metadata}")  # 모든 메타데이터 출력
            print("-" * 60)
    else:
        print("검색 결과가 없습니다.")
