# 전기차 배터리 열폭주 방지필름 시장 조사 대시보드

Thermal Runaway Prevention Film Market Analysis Dashboard

## 프로젝트 개요

전기차 배터리 열폭주 방지필름(Thermal Runaway Prevention Film)에 대한 시장 조사 보고서를 대시보드 형태로 제공하고, 최신 뉴스를 실시간으로 수집하여 표시하는 웹 애플리케이션입니다.

## 주요 기능

- 📊 **시장 조사 대시보드**: 시장 개요, 기술 트렌드, 주요 플레이어 분석, 규제 및 표준 정보 제공
- 🔄 **실시간 뉴스 크롤링**: 구글 뉴스 RSS 피드와 웹 스크래핑을 통한 안정적인 뉴스 수집
- 🎨 **현대적인 UI**: Tailwind CSS 기반 다크 모드 디자인
- 📈 **시각적 다이어그램**: 열폭주 방지 방식별 SVG 다이어그램 제공
- 🌍 **국가 정보**: 주요 플레이어 기업의 국가 정보 병기

## 기술 스택

- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Backend**: Python Flask
- **크롤링**: RSS 피드 (feedparser) + BeautifulSoup (웹 스크래핑)
- **데이터 형식**: JSON

## 설치 방법

### 1. 저장소 클론 또는 파일 다운로드

```bash
# 프로젝트 디렉토리로 이동
cd 251229_Film
```

### 2. Python 가상환경 생성 및 활성화 (권장)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. (선택사항) 로컬에서 뉴스 크롤링 테스트

```bash
python crawler.py
```

## 사용 방법

### 1. 뉴스 크롤링 실행 (선택사항)

최신 뉴스를 수집하려면 크롤러를 먼저 실행합니다:

```bash
python crawler.py
```

이 명령은 `news_data.json` 파일을 생성/업데이트합니다.

### 2. Flask 서버 실행

```bash
python app.py
```

서버가 시작되면 브라우저에서 다음 주소로 접속합니다:

```
http://localhost:5000
```

### 3. 대시보드 사용

- 대시보드에서 시장 조사 정보를 확인할 수 있습니다.
- "🔄 뉴스 새로고침" 버튼을 클릭하면 최신 뉴스를 자동으로 크롤링합니다.
- 뉴스는 5분마다 자동으로 새로고침됩니다.

## 프로젝트 구조

```
251229_Film/
├── app.py                 # Flask 서버 (HTML 및 API 서빙)
├── crawler.py            # 뉴스 크롤링 스크립트
├── requirements.txt      # Python 패키지 목록
├── news_data.json        # 크롤링된 뉴스 데이터 (자동 생성)
├── templates/
│   └── index.html        # 대시보드 HTML 파일
└── README.md            # 프로젝트 설명서
```

## 크롤링 키워드

다음 키워드로 뉴스를 검색합니다:

- 전기차 배터리 열폭주 방지
- Battery Thermal Runaway Prevention
- Mica vs Aerogel EV Battery
- LG Chem Safety Reinforced Layer
- 배터리 화재 방지 필름

## 주요 기술 정보

### 소재별 특성

1. **Mica (운모)**
   - 내열온도: 1,000°C 이상
   - 장점: 저렴한 비용
   - 단점: 무게/부피가 커서 슬림화 추세에 불리

2. **Aerogel (에어로겔)**
   - 열전도율: ≤ 0.020 W/m·K (최강 단열재)
   - 두께: 0.5~3mm
   - 대표 제품: Aspen Aerogels의 PyroThin

3. **SRL (LG화학)**
   - Safety Reinforced Layer
   - 온도 감응형 전류 차단 기술
   - 발열 초기 단계에서 선제적 차단

### 주요 플레이어

- LG화학 (SRL 기술)
- 롯데케미칼 (난연성 폴리머)
- Aspen Aerogels (PyroThin)
- 3M (종합 소재)
- Morgan Advanced Materials (Mica 기반)

### 규제 및 표준

- **UL94 V-0**: 난연성 최고 등급
- **UL2596**: 열폭주 방지 테스트 표준

## 문제 해결

### CORS 오류

Flask-CORS가 자동으로 CORS 문제를 해결합니다. 별도 설정이 필요 없습니다.

### 크롤링 실패

- 인터넷 연결을 확인하세요.
- RSS 피드 방식이 기본으로 사용되며, 더 안정적입니다.
- 일부 사이트는 봇 차단을 사용할 수 있으므로, 필요시 User-Agent를 변경하거나 딜레이를 늘려보세요.
- 로컬에서 크롤링이 안 될 경우, 서버의 `/api/refresh` 엔드포인트를 직접 호출해보세요.

### 뉴스가 표시되지 않음

1. `crawler.py`를 먼저 실행하여 `news_data.json` 파일을 생성하세요.
2. 서버를 재시작하세요.
3. 브라우저 콘솔에서 오류 메시지를 확인하세요.

## 라이선스

이 프로젝트는 교육 및 연구 목적으로 제작되었습니다.

## Render.com 배포

이 프로젝트는 Render.com에서 배포할 수 있습니다.

### 배포 방법

1. GitHub 저장소에 코드를 푸시합니다.
2. Render.com에 로그인하고 "New Web Service"를 선택합니다.
3. GitHub 저장소를 연결합니다.
4. 다음 설정을 사용합니다:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment**: Python 3

또는 `render.yaml` 파일을 사용하여 자동 배포할 수 있습니다.

### 주의사항

- Render.com의 무료 플랜에서는 일정 시간 후 서비스가 슬립 모드로 전환될 수 있습니다.
- 크롤링 기능은 Render.com에서도 정상 작동합니다 (RSS 피드 방식 사용).
- `news_data.json` 파일은 서버 재시작 시 초기화될 수 있으므로, 필요시 외부 스토리지를 사용하세요.

### 배포 후 "Not Found" 오류 해결

배포 후 "Not Found" 오류가 발생하는 경우:

1. **로그 확인**: Render.com 대시보드에서 로그를 확인하세요.
2. **헬스 체크**: `/health` 엔드포인트로 서버 상태를 확인하세요.
3. **템플릿 경로**: `templates/index.html` 파일이 올바른 위치에 있는지 확인하세요.
4. **포트 설정**: `gunicorn_config.py`가 올바르게 설정되어 있는지 확인하세요.
5. **재배포**: 변경 사항을 커밋하고 다시 배포해보세요.

**디버깅 팁**:
- `/health` 엔드포인트로 템플릿 파일 존재 여부를 확인할 수 있습니다.
- Render.com 로그에서 정확한 오류 메시지를 확인하세요.

## 참고 사항

- 크롤링은 웹사이트의 이용약관을 준수해야 합니다.
- 과도한 크롤링 요청은 IP 차단을 유발할 수 있으므로 적절한 딜레이를 유지하세요.
- 뉴스 데이터는 참고용이며, 정확한 정보는 원문을 확인하세요.
- RSS 피드 방식은 Playwright보다 더 안정적이고 빠르며, 클라우드 환경에서도 잘 작동합니다.

