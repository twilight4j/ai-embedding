# FAISS 기반 벡터스토어 생성 애플리케이션

Langchain, FAISS를 활용한 AI 기반 임베딩

## 주요 기능

- SQLite RDB 통합
- FAISS를 활용한 벡터스토어 저장
- OpenAI 기반 임베딩

## 설치 방법
1. 가상환경 설치:
가상환경이 설치되어 있지 않다면 아래 문서를 참고하여 poetry 환경을 구성합니다.
- Mac 사용자: [SETUP(Mac).md](/doc/SETUP(MAC).md)
- Windows 사용자: [SETUP(windows).md](/doc/SETUP(windows).md)

2. 가상환경 시작:
```bash
poetry shell
```

3. 개발 모드로 프로젝트 설치:
```bash
poetry update
```

4. `.env.example`을 기반으로 `.env` 파일을 생성하고 설정값을 입력하세요.

5. 애플리케이션 실행:
```bash
python main.py
```

## 프로젝트 구조

```
.
├── main.py             # 임베딩 애플리케이션
├── pyproject.toml      # 프로젝트 메타데이터 및 의존성
├── .env                # 환경 변수 (.env.example에서 생성)
└── README.md           # 본 파일
```

## notebook 사용법

1. ipynb 파일을 열고 오른쪽 상단 커널을 선택합니다.
- `embedding-{해시값}-py3.11 (Python 3.11.9)` 클릭

2. 파일구조

```
/notebook
├── 00_csv_to_sqlite.ipynb     # CSV 파일 SQLite database로 변환합니다.
├── 01_rdb_to_faiss.ipynb      # RDB(SQLite) 의 데이터를 임베딩하여 faiss index 에 저장합니다.
└── 02_search_from_faiss.ipynb # Vectore store 기반 검색을 테스트합니다.
```

## 개발 스택

- Langchain: AI/ML 파이프라인
- FAISS: 벡터 유사도 검색
- OpenAI: 임베딩 및 LLM