from dotenv import load_dotenv
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate

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

import re

def intent_based_filtering(query):
    """사용자 의도 분석을 통한 필터링"""

    filter_dict = {}

    # 가격 필터링을 위한 정규표현식 패턴
    # 1) N만원 이상 | N만원 부터
    price_pattern = r'(\d+)만원\s*(이상|부터)'
    price_match = re.search(price_pattern, query)
    
    if price_match:
        # SALE_PRC 키가 없으면 생성
        if "SALE_PRC" not in filter_dict:
            filter_dict["SALE_PRC"] = {}
        # 만원 단위를 원 단위로 변환 (예: 120만원 -> 1200000원)
        filter_dict["SALE_PRC"]["$gte"] = int(price_match.group(1)) * 10000
    
    # 2) N만원 이하 | N만원 까지
    price_pattern_lte = r'(\d+)만원\s*(이하|까지)'
    price_match_lte = re.search(price_pattern_lte, query)
    
    if price_match_lte:
        if "SALE_PRC" not in filter_dict:
            filter_dict["SALE_PRC"] = {}
        filter_dict["SALE_PRC"]["$lte"] = int(price_match_lte.group(1)) * 10000

    # 3) N만원 대
    price_pattern_range = r'(\d+)만원\s*대'
    price_match_range = re.search(price_pattern_range, query)
    
    if price_match_range:
        if "SALE_PRC" not in filter_dict:
            filter_dict["SALE_PRC"] = {}
        base_price = int(price_match_range.group(1)) * 10000
        filter_dict["SALE_PRC"]["$gte"] = base_price
        filter_dict["SALE_PRC"]["$lt"] = base_price * 2

    return filter_dict

####################################
# 3-1. Vectorstore 검색
####################################
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
    filter_dict = intent_based_filtering(query)

    print(f"filter_dict: {filter_dict}")

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
            print(f"[결과 {i}] 유사도: {score}") # 낮을수록 더 유사함
            print(f"{doc.page_content}")
            # print(f"메타데이터: {doc.metadata}")  # 모든 메타데이터 출력
            try:
                print(f"- 상품상태: {doc.metadata.get('GOODS_STAT_SCT_NM', '정보 없음')}")
                print(f"- 브랜드명: {doc.metadata.get('BRND_NM', '정보 없음')}")
                print(f"- 상품명: {doc.metadata.get('GOODS_NM', '정보 없음')}")
                print(f"- 품목정보: {doc.metadata.get('ARTC_INFO', '정보 없음')}")
                print(f"- 카테고리: {doc.metadata.get('CATEGORY_NMS', '정보 없음')}")
                print(f"- 판매가: {format(int(doc.metadata.get('SALE_PRC', 0)), ',')}원")
                print(f"- 할인가: {format(int(doc.metadata.get('DSCNT_SALE_PRC', 0)), ',')}원")
                print(f"- 최대혜택가: {format(int(doc.metadata.get('MAX_BENEFIT_PRICE', 0)), ',')}원")
                print(f"- 카드할인율: {doc.metadata.get('CARD_DC_RATE', '0')}%")
                print(f"- 할인카드: {doc.metadata.get('CARD_DC_NAME_LIST', '정보 없음')}")
                print(f"- 주요 특징 및 기능:")
                feature_values = doc.metadata['OPT_VAL_DESC'].split(',')
                feature_titles = doc.metadata['OPT_DISP_NM'].split(',')
                for i, (title, value) in enumerate(zip(feature_titles, feature_values)):
                    print(f"  - {title} : {value}")
                    if i == 3: break
                print(f"🔗 상품보러가기 : https://www.e-himart.co.kr/app/goods/goodsDetail?goodsNo={doc.metadata.get('GOODS_NO', '정보 없음')}")
            except Exception as e:
                print(f"메타데이터 처리 중 오류 발생: {str(e)}")
            print("-" * 60)
    else:
        print("검색 결과가 없습니다.")
        print("다른 검색어로 다시 시도해보시거나, 검색어를 더 구체적으로 입력해주세요.")

###################################
# 3-2. Vectorstore + LLM 검색
###################################
# 검색기(Retriever) 생성
# retriever = vectorstore.as_retriever(
#     search_kwargs={
#         "k": 5  # 반환할 결과 수
#     }
# )

# # 프롬프트를 생성합니다.
# prompt = PromptTemplate.from_template(
#     """You are a product search assistant for an electronics e-commerce platform. 
# Use the following pieces of retrieved context to answer the question. 
# Search up to 5 products.
# Kindly explain why you've been searching for the product.
# And be sure to include the following meta information:
# 상품명
# - 상품상태
# - 브랜드명
# - 판매가
# - 할인가
# - 최대혜택가
# - 할인카드
# - 주요 특징 및 기능(질문의 내용과 부합하는 사항을 포함하여 최대 3개)
# 🔗 상품보러가기 : https://www.e-himart.co.kr/app/goods/goodsDetail?goodsNo=상품번호
# Answer in Korean.

# #Context: 
# {context}

# #Question:
# {question}

# #Answer:"""
# )

# # 모델(LLM) 을 생성합니다.
# llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

# # 체인(Chain) 생성
# chain = (
#     {"context": retriever, "question": RunnablePassthrough()}
#     | prompt
#     | llm
#     | StrOutputParser()
# )

# while True:
#     # 검색할 쿼리 입력 받기
#     query = input("\n검색어를 입력하세요 (종료하려면 'q' 또는 'quit' 입력): ").strip()
    
#     # 종료 조건 확인
#     if query.lower() in ['q', 'quit']:
#         print("검색을 종료합니다.")
#         break
    
#     if not query:
#         print("검색어를 입력해주세요.")
#         continue

#    # 체인 실행(Run Chain)
#     # 문서에 대한 질의를 입력하고, 답변을 출력합니다.
#     response = chain.invoke(query)
#     print(response)

####################################
# 3-3. Vectorstore + LLM 검색(가벼운 버전)
####################################
# 검색기(Retriever) 생성
# retriever = vectorstore.as_retriever(
#     search_kwargs={
#         "k": 5  # 반환할 결과 수
#     }
# )

# # 프롬프트를 생성합니다.
# prompt = PromptTemplate.from_template(
#     """You are a product search assistant for an electronics e-commerce platform. 
# Use the following pieces of retrieved context to answer the question. 
# 🔗 상품보러가기 : https://www.e-himart.co.kr/app/goods/goodsDetail?goodsNo=상품번호
# Answer in Korean.

# #Context: 
# {context}

# #Question:
# {question}

# #Answer:"""
# )

# # 모델(LLM) 을 생성합니다.
# llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

# # 체인(Chain) 생성
# chain = (
#     {"context": retriever, "question": RunnablePassthrough()}
#     | prompt
#     | llm
#     | StrOutputParser()
# )

# while True:
#     # 검색할 쿼리 입력 받기
#     query = input("\n검색어를 입력하세요 (종료하려면 'q' 또는 'quit' 입력): ").strip()
    
#     # 종료 조건 확인
#     if query.lower() in ['q', 'quit']:
#         print("검색을 종료합니다.")
#         break
    
#     if not query:
#         print("검색어를 입력해주세요.")
#         continue

#    # 체인 실행(Run Chain)
#     # 문서에 대한 질의를 입력하고, 답변을 출력합니다.
#     response = chain.invoke(query)
#     print(response)