# 🌐 AI 기반 콘텐츠 큐레이션 백엔드(AI Multi-Source Content Curation Backend)  
본 프로젝트는 사용자 지정 키워드에 따라 다중 외부 API에서 데이터를 비동기로 수집하고, LLM(Large Language Model)을 이용해 요약 및 가공하여 최종 결과를 제공하는 백엔드 시스템의 구축을 목표로 하고 있습니다.  

## 개발 기간  
2025.12.07~

## 🌟 핵심 기능(MVP)  
1. 키워드 등록/관리(CRUD)  
2. 2개 이상의 이종 API 연동(예: 뉴스 API, 소셜 미디어 API).  
3. 비동기 작업 요청 API 및 작업 상태 조회 기능.  
4. LLM을 사용한 수집된 콘텐츠의 자동 요약 및 키워드 추출.  
5. 최종 큐레이션 결과 조회 API.

## 현재 버전  
**v0.0.7** | **핵심 도메인 모델 정의 및 MVP API 기초 구현.**  

---
### ⚙️ 진행 히스토리 (2025.12.09)  
**v0.0.7** | **핵심 도메인 모델 정의 및 MVP API 기초 구현.**  
* **전체 DB 스키마 확정:**  `user`, `tasklog`, `rawcontent`, `curatedcontent` ORM 모델 정의 및 Alembic 마이그레이션을 통해 DB 스키마 최종 적용 완료.  
* **키워드 관리 API 구현:**  키워드 등록/조회 (`Post /api/v1/keywords`, `Get api/v1/keywords`) API 구현.  
* **비동기 Task 시스템 연동:**  Celery Task 요청 (`Post /api/v1/curation-tasks`) 및 상태 조회 (`GET /api/v1/curation-task/{task_id}`) API 구현.  
* **라우터 설정:**  `app/main/py`에 `keywords` 및 `curation_task` 라우터 포함 완료.

### ⚙️ 진행 히스토리 (2025.12.08)  
**v0.0.6** | **DB 환경 설정 최종 안정화 및 마이그레이션 시스템 도입**  
* **DB 연결 안정화:**  Root 및 일반 사용자 비밀번호 불일치 문제 해결 및 환경 변수 일치.  
* **권한 스크립트 수정:**  grant_remote_access.sh 스크립트가 root 비밀번호를 올바르게 사용하도록 보장.  
* **Alembic 초기화:**  비동기 MySQL 드라이버(aiomysql)를 사용하는 Alembic 마이그레이션 시스템 초기화 및 첫 마이그레이션 스크립트 생성.  
* **첫 테이블 적용:**  `keyword` 테이블에 대한 첫 마이그레이션 스크립트 생성 및 DB에 성공적으로 적용 확인.  

### ⚙️ 진행 히스토리 (2025.12.08)  
**v0.0.5** | **초기 인프라 및 Celery 구성 완료**  
* **Docker Compose:** MySQL, Redis, FastAPI Web, Celery Worker 4개 서비스 구성 완료.  
* **환경 변수:** `.env` 파일에 모든 서비스(DB, Redis, Celery, API Keys) 설정값 정의 및 Pydantic `Settings` 클래스를 통해 로드.  
* **Celery 연동:** `app/core/celery_app.py`를 정의하여 Celery Worker가 Redis Broker/Backend에 연결.    
* **FastAPI 구동:** `app/main.py`에 FastAPI 인스턴스(`app`)를 정의하여 Uvicorn이 웹 서버를 로드. (http://localhost:8000/docs 접속 가능 상태)  
* **구조 정리:** 설정(`config.py`, `settings.py`)과 비동기(`celery.py`) 모듈 분리 및 역할 정립.  

## 아키텍처 및 기술 스택
|컴포넌트|기술 스택|사용 목적|
|---|---|---|
|**Web Server(API Gateway)**|**Fast API**|빠르고 비동기적인 API 엔드포인트 제공 및 Task Queue에 작업 전달 역할.|
|**Database(Data Storage)**|**MySQL**|사용자 설정, 수집된 원본 데이터, 최종 가공된 큐레이션 결과 저장.|
|**Asynchronous Task Queue**|**Redis**|Celery Worker와 Web Server간의 메시지 중계 및 빠른 캐싱 저장소 역할.|
|**Task Worker(Processer)**|**Celery**|시간이 오래 걸리는 외부 API 호출 및 LLM 처리 작업을 비동기로 실행.|
|**HTTP Client**|**Httpx**|외부 API 통신에 사용되는 비동기 HTTP 클라이언트.|

## 핵심 데이터 모델 설계

**User(사용자 관리)**  

|필드|타입|설명|
|---|---|---|
|id|Integer(PK)|사용자 ID|
|username|String|사용자 이름|
|password|String|사용자 비밀번호|

**Keyword(사용자 키워드)**  

|필드|타입|설명|
|---|---|---|
|id|Integer(PK)|키워드 ID|
|user_id|Integer(FK)|키워드를 사용한 등록자|
|keyword_text|String|실제 검색에 사용할 키워드|

**TaskLog(비동기 작업 로그)**  

|필드|타입|설명|
|---|---|---|
|id|Integer(PK)|작업 로그 ID|
|keyword_id|Integer(FK)|대상 키워드 ID|
|celery_task_id|String|Celery가 부여한 고유 작업 ID(상태조회용)|
|status|String|Pending, Running, Completed, Failed|
|requested_at|DateTime|작업 요청 시각|
|completed_at|DateTime|작업 완료 시작|

**RawContent(수집된 원본 데이터)**  

|필드|타입|설명|
|---|---|---|
|id|Integer(PK)|작업 로그 ID|
|keyword_id|Integer(FK)|대상 키워드 ID|
|source_type|String|수집된 API 종류|
|original_url|String|원본 콘텐츠 URL|
|raw_text|Text|LLM에게 전달할 원본 텍스트 내용|
|collected_at|DateTime|수집 시각|

**CuratedContent(LLM이 가공한 최종 결과)**  

|필드|타입|설명|
|---|---|---|
|id|Integer(PK)|큐레이션 결과 ID|
|raw_content_id|Integer(FK)|원본 콘텐츠 ID|
|summary_text|Text|LLM이 요약한 내용|
|extracted_keywords|Json/String|LLM이 추출한 주요 키워드 목록|
|curated_at|DateTime|가공 완료 시각|

## 핵심 API 엔드포인트 (FastAPI)  
FastAPI 서버에서 처리할 주요 API 엔드포인트 정의  

|순서|HTTP 메서드|경로|설명|주요 로직|
|---|---|---|---|---|
|1|POST|/api/v1/keywords|새로운 키워드 등록|DB Keyword 테이블에 저장|
|2|GET|/api/v1/keywords|등록된 키워드 목록 조회|DB Keyword 테이블 조회|
|3|POST|/api/v1/curation-tasks|키워드 기반 큐레이션 작업 요청|Celery에 Task를 전달하고 TaskLog에 Pending 상태로 기록, celery_task_id 반환|
|4|GET|/api/v1/curation-task/{task_id}|비동기 작업 상태 조회|Celery/Redis에서 task_id의 상태를 확인하고 TaskLog 테이블에서 상태 업데이트 및 반환|
|5|GET|/api/v1/curated-content|최종 큐레이션 결과 목록 조회|DB CuratedContent 테이블 조회(필터링, 페이징 적용)|

## 파일 구조 (도메인형 파일 구조, DDS)  
msc-cb/  
├── app/  
│   ├── core/    
│   │   ├── database.py              # DB 세션 및 Engine  
│   │   ├── security.py              # 비밀번호 해싱 및 API Key 암호화/복호화 함수  
│   │   ├── celery_app.py            # Celery Worker의 Redis Broker/Backend 연결 설정
│   │   ├── config.py                # 전역 변수 설정  
│   │   └── settings.py              # 환경 변수 Pydantic 설정  
│   │  
│   ├── modules/                     # 핵심 도메인 모듈  
│   │   ├── __init__.py  
│   │   ├── user/                    # 1. 사용자 관리 도메인 (비밀번호 해싱 적용)  
│   │   │   ├── api.py               # 유저 인증/CRUD 라우터  
│   │   │   ├── models.py            # User ORM 모델  
│   │   │   ├── schemas.py           # User Pydantic 스키마  
│   │   │   └── service.py           # 유저 생성 시 security.get_password_hash() 사용  
│   │   │  
│   │   ├── keywords/                # 2. 키워드 관리 도메인 (API Key 직접 노출 없음)  
│   │   │   ├── __init__.py  
│   │   │   ├── api.py               # 키워드 CRUD 및 큐레이션 요청 API  
│   │   │   ├── models.py            # Keyword ORM 모델 (API Keys는 여기에 저장될 수 있음 - 암호화된 상태)  
│   │   │   ├── schemas.py           # Keyword Pydantic 스키마  
│   │   │   └── service.py           # 큐레이션 작업 트리거 및 암호화된 API Key 관리  
│   │   │  
│   │   ├── curation_task/           # 3. 큐레이션 작업 도메인 (비동기 처리 로직)  
│   │   │   ├── api.py               # Task 요청 및 상태 조회 라우터  
│   │   │   ├── models.py            # TaskLog ORM 모델  
│   │   │   ├── service.py           # Celery 상태 조회 및 TaskLog 업데이트
│   │   │   ├── schemas.py           # Task 요청/응답 스키마  
│   │   │   └── worker.py            # Celery Task 정의 및 실행 (Service에서 받은 암호화된 키를 worker 내에서 복호화 후 사용)  
│   │   │  
│   │   ├── content/                 # 4. 큐레이션 결과 도메인 (최종 콘텐츠 관리)  
│   │   │   ├── api.py               # 최종 콘텐츠 조회 라우터  
│   │   │   ├── models.py            # RawContent, CuratedContent ORM 모델  
│   │   │   └── service.py           # 데이터 조회 및 필터링 로직  
│   │   │  
│   │   └── external/                # 5. 외부 연동 도메인 (Collector 및 LLM)  
│   │       ├── collector/           # 외부 데이터 수집 (Raw Data)  
│   │       │   ├── base_collector.py  
│   │       │   └── news_collector.py  
│   │       └── processor/           # LLM 기반 데이터 처리 (요약/추출)  
│   │           └── llm_processor.py  
│   │  
│   └── main.py                      # FastAPI 애플리케이션 엔트리 포인트  
│  
├── alembic/  
│    ├── versions/  
│    │   ├── c93021f4e1bc_create_remaining_core_tables.cpython-314.pyc  
│    │   └── f697008bd951_create_initial_keyword_table.py    
│    └── env.py  
│   
├── alembic.ini  
├── grant_remote_access.sh  
├── docker-compose.yml  
├── Dockerfile  
├── .env    
└── requirements.txt  

## 🤝 기여자 및 라이선스  
| 백진명 | 프로젝트 리드 개발 및 설계 | [Mikang87] https://github.com/Mikang87 |  
License: MIT License
