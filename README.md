# AI Embedding Project

## 개요

가전상품 이커머스 플랫폼 내에 AI를 활용한 검색서비스 개발 PoC

## 목적

- 자연어 검색
- 자사 내부에 가지고 있는 상품정보를 활용하여 사용자가 원하는 적절한 상품을 AI로 검색

## 프로세스

1. RDB에 저장되어 있는 상품정보를 임베딩하여 주기적으로 VectorDB에 저장
2. 사용자 쿼리를 받아 프롬프트 엔지니어링 수행
3. 프롬프트를 LLM에 전달하여 VectorDB 검색
4. 검색결과를 json 데이터로 파싱하여 API로 제공
5. 프론트엔드는 별도로 구현되어 있음

## 기술스펙

- Langchain
- 원천데이터: Oracle RDB
- Embedding: OpenAIEmbedding
- VectorDB: ChromaDB
- LLM: openai
    - LLM은 쉽게 변경할 수 있도록 Langchain 으로 개발

## 참고

1. Langchain 의 최신 API Reference  [https://python.langchain.com/api_reference/](https://python.langchain.com/api_reference/)
2. 프로젝트의 개발 일정
    1. 개발자1명, 2개월

## 질의응답 데이터셋

|사용자 검색어|검색 결과|
|---|---|
|소음이 적은 키보드||
|자동급수 가능한 로봇청소기||