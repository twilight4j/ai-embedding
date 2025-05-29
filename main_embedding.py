from dotenv import load_dotenv
import os
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# API 키 정보 로드
load_dotenv()

####################################
# 1. Oracle 데이터베이스 연결 및 조회(선택)
####################################
# import oracledb
# SQL 파일 읽기
# sql_path = './.db/oracle/product.sql'
# with open(sql_path, 'r', encoding='utf-8') as f:
#     sql = f.read().strip()

# # Oracle 데이터베이스 연결 정보
# connection = oracledb.connect(
#     user=os.getenv("ORACLE_USER"),
#     password=os.getenv("ORACLE_PASSWORD"),
#     host=os.getenv("ORACLE_HOST"),
#     port=os.getenv("ORACLE_PORT"),
#     sid=os.getenv("ORACLE_SID")
#     )

# cursor = connection.cursor()
# cursor.execute(sql)
# rows = cursor.fetchall()

# # 연결 종료
# cursor.close()
# connection.close()

####################################
# 1. sqlite 데이터베이스 연결 및 조회(선택)
####################################
import sqlite3

sql = "SELECT * FROM PRODUCT"
# SQLite 데이터베이스 연결
conn = sqlite3.connect('./.db/sqlite/my_database.db')
cursor = conn.cursor()

# SQL 쿼리 실행
cursor.execute(sql)
rows = cursor.fetchall()

# 연결 종료
cursor.close()
conn.close()


####################################
# 2. 주어진 컬럼들을 바탕으로 ML 검색에 용이하도록 문맥에 맞게 병합
####################################
# 주어진 컬럼들을 바탕으로 ML 검색에 용이하도록 문맥에 맞게 병합

# 컬럼 인덱스 정의 (실제 CSV 파일의 컬럼 순서에 맞게 조정해야 합니다)
# 이 부분은 실제 데이터의 컬럼 순서와 일치해야 합니다.
COLUMN_INDICES = {
    "GOODS_NO": 0,
    "GOODS_NM": 1,
    "GOODS_STAT_SCT_NM": 2,
    "BRND_NM": 3,
    "ARTC_INFO": 4,
    "OPT_DISP_NM": 5,
    "OPT_VAL_DESC": 6,
    "CATEGORY_NMS": 7,
    "SALE_PRC": 8,
    "DSCNT_SALE_PRC": 9,
    "CARD_DC_RATE": 10,
    "CARD_DC_NAME": 11,
    "CARD_DC_NAME_LIST": 12,
    "MAX_BENEFIT_PRICE": 13
}

def generate_search_text_from_tuple(product_data_tuple):
    """
    주어진 상품 정보 튜플에서 검색에 최적화된 통합 텍스트 문자열을 생성합니다.
    머신러닝 기반의 의미론적 검색에 유리하도록 문맥을 구성합니다.

    Args:
        product_data_tuple (tuple): 상품 정보를 담고 있는 튜플.
                                  COLUMNS_INDICES에 정의된 순서와 일치해야 합니다.

    Returns:
        str: 검색 인덱싱을 위한 상품 정보를 결합한 문자열.
    """

    search_components = []

    # 튜플에서 데이터 추출 (COLUMN_INDICES를 활용하여 가독성을 높입니다)
    goods_nm = product_data_tuple[COLUMN_INDICES["GOODS_NM"]].strip()
    goods_stat_sct_nm = product_data_tuple[COLUMN_INDICES["GOODS_STAT_SCT_NM"]].strip()
    brnd_nm = product_data_tuple[COLUMN_INDICES["BRND_NM"]].strip()
    artc_info = product_data_tuple[COLUMN_INDICES["ARTC_INFO"]].strip()
    opt_disp_nm = product_data_tuple[COLUMN_INDICES["OPT_DISP_NM"]].strip()
    opt_val_desc = product_data_tuple[COLUMN_INDICES["OPT_VAL_DESC"]].strip()
    category_nms = product_data_tuple[COLUMN_INDICES["CATEGORY_NMS"]].strip()
    
    # 숫자 값은 형 변환 시 에러 방지를 위해 get 대신 직접 접근 후 try-except 처리
    sale_prc_str = product_data_tuple[COLUMN_INDICES["SALE_PRC"]]
    dscnt_sale_prc_str = product_data_tuple[COLUMN_INDICES["DSCNT_SALE_PRC"]]
    card_dc_rate_str = product_data_tuple[COLUMN_INDICES["CARD_DC_RATE"]]
    max_benefit_price_str = product_data_tuple[COLUMN_INDICES["MAX_BENEFIT_PRICE"]]
    
    sale_prc = int(sale_prc_str) if sale_prc_str else None
    dscnt_sale_prc = int(dscnt_sale_prc_str) if dscnt_sale_prc_str else None
    card_dc_rate = int(card_dc_rate_str) if card_dc_rate_str else None
    max_benefit_price = int(max_benefit_price_str) if max_benefit_price_str else None

    card_dc_name = product_data_tuple[COLUMN_INDICES["CARD_DC_NAME"]].strip()


    # 1. 브랜드명 + 품목 정보 (카테고리/ARTC_INFO) + 상품명 조합
    # 상품의 핵심적인 정체성을 명확히 합니다.
    if brnd_nm and goods_nm:
        # ARTC_INFO에서 품목의 구체적인 타입을 추론하여 문맥에 더합니다.
        item_type = ''
        if artc_info:
            # '>' 기호로 구분된 품목 정보 중 가장 마지막 부분을 가져와 특정 품목 타입을 얻습니다.
            item_type_parts = [part.strip() for part in artc_info.split('>') if part.strip()]
            if item_type_parts:
                item_type = item_type_parts[-1]
                # 'TV 기타'와 같은 모호한 표현을 'TV 거치대' 등으로 명확히 합니다.
                if item_type == 'TV 기타':
                    item_type = 'TV 거치대'
                elif item_type.endswith('TV'): # 'UHD TV' 등 TV 종류를 유지합니다.
                    item_type = item_type
                elif item_type == '기타': # A/V 기타 > 기타와 같은 경우를 처리합니다.
                    item_type = '기타 가전제품' # 좀 더 명확한 표현을 사용합니다.
                elif '스탠드' in item_type or '거치대' in item_type: # 예: 이젤형 TV스탠드, 모니터암
                    item_type = item_type
                else: # ARTC_INFO가 너무 일반적인 경우, 품목명이나 카테고리에서 가져올 수도 있습니다.
                    if category_nms:
                        main_category_parts = [part.strip() for part in category_nms.split('>')]
                        if main_category_parts and main_category_parts[0] != 'TV·영상가전': # 이미 TV인 경우 제외
                            item_type = main_category_parts[0]


        # 품목 타입이 있고, 상품명에 이미 품목 타입이 포함되어 있지 않다면 추가합니다.
        if item_type and item_type not in goods_nm:
            search_components.append(f"{brnd_nm}의 {item_type}, {goods_nm}.")
        else: # 품목 타입이 없거나 상품명에 이미 포함되어 있다면 브랜드명과 상품명만 사용합니다.
            search_components.append(f"{brnd_nm}의 {goods_nm}.")
    elif goods_nm: # 브랜드명이 없는 경우 상품명만 사용합니다.
        search_components.append(f"{goods_nm}.")


    # 2. 제품의 주요 특성 (OPT_DISP_NM 및 OPT_VAL_DESC) 조합
    if opt_disp_nm and opt_val_desc:
        display_names = [name.strip() for name in opt_disp_nm.split(',') if name.strip()]
        values = [val.strip() for val in opt_val_desc.split(',') if val.strip()]

        # 각 특성 항목과 값을 '항목: 값' 형태로 결합합니다.
        characteristics = []
        for i in range(min(len(display_names), len(values))):
            # 비어있는 항목이나 '스마트기능'처럼 반복되는 용어는 건너뜁니다.
            # '스마트기능'이 반복되는 경우, 첫 번째 '스마트기능' 뒤에 모든 스마트기능 값을 나열합니다.
            if display_names[i] == '스마트기능':
                if i > 0 and display_names[i-1] == '스마트기능':
                    continue # 이미 처리되었으므로 건너뜁니다.
                
                # 모든 스마트기능 값을 모아서 처리
                all_smart_features = []
                for j in range(i, len(display_names)):
                    if display_names[j] == '스마트기능' and j < len(values):
                        all_smart_features.append(values[j])
                    else:
                        break # 스마트기능이 끝나면 반복 중단

                if all_smart_features:
                    characteristics.append(f"스마트기능: {', '.join(all_smart_features)}")
            else: # 일반적인 특성
                if display_names[i] and values[i]:
                    characteristics.append(f"{display_names[i]}: {values[i]}")

        if characteristics:
            search_components.append("주요 특징: " + ", ".join(characteristics) + ".")

    # 3. 카테고리명 추가
    if category_nms:
        # '|' 기호를 ', '로, '>' 기호를 ' > '로 바꾸어 카테고리 계층 및 다중 카테고리를 표현합니다.
        formatted_categories = category_nms.replace('|', ', ').replace('>', ' > ')
        search_components.append(f"카테고리: {formatted_categories}.")

    # 4. 상품 상태 추가
    if goods_stat_sct_nm and goods_stat_sct_nm != '정상상품': # '정상상품'이 아닌 경우에만 추가합니다.
        search_components.append(f"상품 상태: {goods_stat_sct_nm}.")

    # 5. 가격 및 할인 정보 추가
    price_info_components = []
    if sale_prc is not None:
        price_info_components.append(f"판매가 {sale_prc:,}원") # 천단위 콤마 추가
    if dscnt_sale_prc is not None and sale_prc is not None and dscnt_sale_prc < sale_prc:
        price_info_components.append(f"할인가 {dscnt_sale_prc:,}원") # 천단위 콤마 추가
    if card_dc_rate is not None and card_dc_rate > 0 and card_dc_name:
        if max_benefit_price is not None:
            price_info_components.append(f"{card_dc_name} 카드 사용 시 {card_dc_rate}% 할인되어 최대 {max_benefit_price:,}원") # 천단위 콤마 추가
        else:
            price_info_components.append(f"{card_dc_name} 카드 사용 시 {card_dc_rate}% 할인")

    if price_info_components:
        search_components.append("가격 정보: " + ", ".join(price_info_components) + ".")

    # 모든 구성 요소를 하나의 문자열로 결합하고 앞뒤 공백을 제거합니다.
    return " ".join(search_components).strip()

# documents 리스트 생성
documents = []
metadatas = []
ids = []

"""
- 예시: 삼성전자의 UHD TV, 125.7cm 4K UHD 비즈니스 TV LH50BEAHLGFXKR (설치유형 선택가능). 카테고리: TV·영상가전 > TV. 가격 정보: 판매가 559,000원.
"""
for row in rows:
    GOODS_NO = row
    metadatas.append({"GOODS_NO": GOODS_NO})
    search_text = generate_search_text_from_tuple(row)
    documents.append(search_text)
    ids.append(str(GOODS_NO))

####################################
# 3. OpenAI 임베딩 객체 생성 (model 지정)
####################################
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")  # 1536 차원

####################################
# 4. 벡터스토어를 생성합니다.
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