# 1. sqlite3 라이브러리 불러오기
import sqlite3

# 2. 데이터베이스 파일에 연결 (없으면 자동 생성)
# 'database.db'라는 이름의 파일과 연결을 시도합니다.
# 이 시점에 파일이 없으면, 파이썬이 자동으로 해당 파일을 생성해 줍니다.
# conn 객체는 이 데이터베이스와의 통신 채널 역할을 합니다.
conn = sqlite3.connect('database.db')
print("Opened database successfully")

# 3. 'User' 테이블 생성
# conn.execute()는 SQL 명령을 실행하는 함수입니다.
# """..."""는 여러 줄의 문자열을 쓸 수 있게 해줍니다.
conn.execute('''
CREATE TABLE User (
    /* 
     id: 고유 번호, 정수(INTEGER), 기본 키(PRIMARY KEY)이며,
         데이터가 추가될 때마다 1씩 자동 증가(AUTOINCREMENT)
    */
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    /* 
     user_id: 사용자가 입력하는 아이디, 문자열(TEXT), 
              값이 중복될 수 없으며(UNIQUE), 비어 있을 수 없음(NOT NULL)
    */
    user_id TEXT UNIQUE NOT NULL,

    /* 
     password_hash: 암호화된 비밀번호가 저장될 곳, 문자열(TEXT),
                    비어 있을 수 없음(NOT NULL)
    */
    password_hash TEXT NOT NULL,

    /*
     user_name: 사용자의 실제 이름, 문자열(TEXT), 비어 있을 수 없음(NOT NULL)
    */
    user_name TEXT NOT NULL
);
''')
print("Table 'User' created successfully")

# 4. 'Comment' 테이블 생성
conn.execute('''
CREATE TABLE Comment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    /*
     user_id: 댓글을 쓴 사용자의 고유 번호(User 테이블의 id와 연결됨)
    */
    user_id INTEGER NOT NULL,

    content TEXT NOT NULL,
    
    /*
     timestamp: 댓글 작성 시간, 날짜/시간(DATETIME),
                데이터 추가 시 현재 시간이 자동으로 기록됨(DEFAULT CURRENT_TIMESTAMP)
    */
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

    /*
     외래 키(FOREIGN KEY) 설정:
     Comment 테이블의 user_id가 User 테이블의 id를 참조한다는 관계를 명시.
     이로써 어떤 사용자가 어떤 댓글을 썼는지 연결됩니다.
    */
    FOREIGN KEY(user_id) REFERENCES User(id)
);
''')
print("Table 'Comment' created successfully")

# 5. 데이터베이스 연결 종료
# 모든 작업을 마친 후에는 연결을 닫아주는 것이 안전합니다.
conn.close()