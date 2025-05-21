# 개발 환경 설정 방법(Mac)

## 터미널 열기
spotlight 검색에서 "terminal" 검색 후 열기

## Homebrew 설치
Homebrew 설치 명령어
1. 아래의 명령어를 실행하여 Homebrew 설치
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

계정의 비밀번호 입력

ENTER 키를 눌러서 진행

2. 아래의 명령어를 실행(<홈> 은 본인의 계정명으로 바꾸세요!!)
다음의 명령어를 실행하여 계정의 username 을 확인합니다.
```bash
whoami
```

brew의 위치를 확인합니다.
```bash
which brew
```

brew 가 설치된 경로를 확인합니다.

- Case 1
```
/opt/homebrew/bin/brew shellenv
```
- Case 2
```
/usr/local/bin/brew shellenv
```

Case 1 인 경우
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/<홈>/.zprofile
```
Case 2 인 경우
```bash
echo 'eval "$(/usr/local/bin/brew shellenv)"' >> /Users/<홈>/.zprofile
```
(아래는 참고용 예시 입니다)
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/ec2-user/.zprofile
```
```bash
echo 'eval "$(/usr/local/bin/brew shellenv)"' >> /Users/ec2-user/.zprofile
```

## xcode 설치 확인
아래의 코드를 실행하여 이미지 설치가 잘 되어 있는지 확인
```bash
xcode-select --install
```

## 소스코드 다운로드
```bash
git clone https://github.com/twilight4j/ai-embedding.git
```

아래의 명령어를 실행하여 ai-embedding 디렉토리로 이동합니다.
```bash
cd ai-embedding
```

## pyenv 설치
참고 링크: https://github.com/pyenv/pyenv?tab=readme-ov-file#understanding-python-version-selection

brew 를 통해 pyenv 를 업데이트 합니다.
```bash
brew update
brew install pyenv
```

아래의 내용을 터미널에 복사 + 붙혀넣기 합니다.
```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

(혹시 만약에 위의 코드 실행시 오류가 발생하는 경우만!!)
```bash
sudo chown $USER ~/.zshrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```bash

터미널 쉘을 재시작 합니다.
```bash
exec "$SHELL"
```

## python 설치
파이썬 3.11 버전 설치
```bash
pyenv install 3.11
```

3.11 버전의 python 설정
```bash
pyenv global 3.11
exec zsh
```

파이썬 버전 확인
```bash
python --version
```
3.11.9 버전이 설치되어 있나 확인합니다.

## poetry 설치
참고 링크: https://python-poetry.org/docs/#installing-with-the-official-installer

poetry 설치
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
Cursor AI 다운로드

다운로드 링크: https://www.cursor.com/downloads
다운로드 받은 Cursor AI 를 설치합니다 (Applications 폴더에 복사)

익스텐션 설치
- Python
- Jupyter

Cursor AI 를 종료 후 재실행

커널 선택
- `01_embedding.ipynb` 파일 열기
- 우측 상단 `select kernel` 확인
- `python environment` 클릭
- `embedding-{해시값}-py3.11 (Python 3.11.9)` 클릭
- 설치한 가상환경이 안뜬다면 Cursor AI 껏다가 재실행

## 참고
- Poetry는 자동으로 가상환경을 관리합니다.
- 가상환경을 비활성화하려면 `exit` 명령어를 사용하면 됩니다.