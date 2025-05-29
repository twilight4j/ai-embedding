# 개발 환경 설정 방법(Windows)

## PowerShell Policy 적용
먼저, Windows PowerShell 을 "관리자 권한으로 실행" 합니다.
다음의 명령어를 입력하여 Policy 를 적용합니다.

```bash
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

적용이 완료된 후 Windows PowerShell 을 껐다가 켭니다. 아래의 진행을 위하여 Windows PowerShell 실행시 "관리자 권한으로 실행" 합니다.

## pyenv 설치
```bash
git clone https://github.com/pyenv-win/pyenv-win.git "$env:USERPROFILE\.pyenv"
```

환경변수 추가
아래의 내용을 복사하여 붙혀넣기 후 실행
```bash
[System.Environment]::SetEnvironmentVariable('PYENV', $env:USERPROFILE + "\.pyenv\pyenv-win\", "User")
[System.Environment]::SetEnvironmentVariable('PYENV_ROOT', $env:USERPROFILE + "\.pyenv\pyenv-win\", "User")
[System.Environment]::SetEnvironmentVariable('PYENV_HOME', $env:USERPROFILE + "\.pyenv\pyenv-win\", "User")
```

아래의 내용을 복사하여 붙혀넣기 후 실행
```bash
[System.Environment]::SetEnvironmentVariable('PATH', $env:USERPROFILE + "\.pyenv\pyenv-win\bin;" + $env:USERPROFILE + "\.pyenv\pyenv-win\shims;" + [System.Environment]::GetEnvironmentVariable('PATH', "User"), "User")
```

현재의 Windows PowerShell 을 종료 후 다시 실행합니다.
다음의 명령어를 입력하여 정상 동작하는지 확인합니다.
```bash
pyenv
```

## Python 설치

파이썬 3.11 버전 설치
```bash
pyenv install 3.11
```

3.11 버전의 python 설정
```bash
pyenv global 3.11
```

파이썬 버전 확인
```bash
python --version
```

## 소스코드 다운로드
```bash
git clone http://10.154.6.210:8081/ai-poc/ai-embedding
```

아래의 명령어를 실행하여 ai-embedding 디렉토리로 이동합니다.
```bash
cd ai-embedding
```

## Poetry 설치

아래의 명령어를 실행하여 Poetry 패키지 관리 도구를 설치합니다.
```bash
pip3 install poetry==1.8.5
```

소스코드 받은 폴더로 이동
```bash
cd ai-embedding
```

파이썬 가상환경 설정
```bash
poetry shell
```

파이썬 패키지 일괄 업데이트
```bash
poetry update
```

## Cursor AI 설치
다운로드 및 설치
[https://www.cursor.com/downloads]

익스텐션 설치
- Python
- Jupyter

Cursor AI 를 종료 후 재실행

커널 선택
- `*.ipynb` 파일 열기
- 우측 상단 `select kernel` 확인
- `python environment` 클릭
- `embedding-{해시값}-py3.11 (Python 3.11.9)` 클릭
- 설치한 가상환경이 안뜬다면 Cursor AI 껏다가 재실행

## 참고
- Poetry는 자동으로 가상환경을 관리합니다.
- 가상환경을 비활성화하려면 `exit` 명령어를 사용하면 됩니다.