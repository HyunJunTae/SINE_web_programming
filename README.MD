
1. 어떤 기술 스택을 왜 선택했는지
    1. 프론트엔드
        - HTML/CSS
            - 웹의 뼈대와 디자인을 구성하는 가장 기초적인 표준 기술. 정적 화면 처리.
            - 외부 라이브러리사용을 최소화하여 
              브라우저가 HTML 태그와 스타일시트를 어떻게 렌더링하는지 직접 체감하기 위해 선택
        
        - Jinja2
            - Flask의 기본 템플릿 엔진. 동적 화면 처리.
            - 백엔드에서 처리한 데이터를 HTML에 동적으로 삽입하는 과정을 이해하기에 적합
            - 템플릿 상속 기능을 통해 코드의 중복을 줄이고 유지보수성을 높이기 위해 선택



    2. 백엔드
        - Python
            - 문법이 간결하여 로직 구현에만 집중할 수 있음.
            - 후에 공부할 웹해킹에서도 종종 사용될 언어이기에 선택.
        - Flask
            - Django와 같이 많은 기능이 자동화된 프레임워크와 달리, 
              라우팅, 요청(Request), 응답(Response) 과정을 개발자가 직접 컨트롤해야 하므로 웹의 동작 원리를 학습하기에 최적
        - Werkzeug
            - 비밀번호 해싱을 안전하게 처리하기 위해 선택



    3. DB
        - SQLite
            - 서버 설치가 필요 없는 파일 기반의 관계형 데이터베이스
            - 설정이 매우 간편하여 초기 개발 속도를 높일 수 있음.
            - 데이터가 database.db라는 단일 파일로 관리되므로 데이터의 물리적 저장 구조를 파악하기 쉬워 입문 단계에서 선택




    4. 프록시




2. 전체 구조 (프론트 / 백 / DB / 프록시)
    1. 프론트엔드
        - HTML
            - base.html
                - 공통 레이아웃(header, nav, footer)을 담고 있는 기본 템플릿
                - 아래 html 파일들은 base.html의 뼈대를 그대로 빌려 씀.
            - index.html
                - 메인 페이지
                - 댓글 목록 표시 및 댓글 작성 폼.
                - 로그인 아직 안했으면 댓글 작성 폼이 로그인 요청 폼으로 뜸.
            - login.html
                - 로그인 버튼 누르면 뜨는 화면.
                - 아이디, 비밀번호 입력 창과 로그인 버튼 보여줌.
            - register.html
                - 회원가입 버튼 누르면 뜨는 화면.
                - 아이디, 이름, 비밀번호 입력 창과 회원가입 버튼 보여줌.
            - profile 
                - 아이디와 유저 이름을 보여줌.

        - CSS
            - style.css
                - html 파일을 꾸며주는 기능
                - class를 지정해서 같은 이름(class)을 갖는 박스의 디자인을 통일함

        - Jinja2
            1) 뼈대 공유
                - 설명: 
                    웹사이트의 모든 페이지에 공통으로 들어가는 메뉴바, 푸터, 배경 설정 등을 한 곳에만 작성하고,
                    다른 페이지들이 이를 그대로 물려받아 사용하게 합니다. 코드 중복을 획기적으로 줄여줌.
            
                - 예시:
                    base.html: 전체 레이아웃을 잡고 알맹이가 들어갈 자리에 
                                {% block content %}{% endblock %} 표시.
                    index.html: 맨 상단에 {% extends "base.html" %}을 적어 뼈대를 가져옴.

            2) 빈칸 채우기
            
                - 설명: 
                    파이썬 서버(app.py)가 데이터베이스에서 꺼내온 실제 데이터(아이디, 이름, 댓글 내용 등)를 
                    HTML의 원하는 위치에 글자로 찍어내는 역할.

                - 예시:
                    app.py: render_template('profile.html', user=user)로 데이터 전송.
                            user라는 데이터 전송 
                            + profile.html 페이지의 {{ user.user_id }} 같은 빈 칸들을 받은 데이터로 채워서 완성시키기
                    profile.html: {{ user.user_id }}라고 적으면 화면에 실제 사용자의 아이디가 출력됨.


            3) 상황 판단
                - 설명: 
                    사용자의 현재 상태(예: 로그인 여부)를 확인하여, 그 상황에 맞는 화면만 골라서 보여줌. 
                    똑같은 페이지라도 사람마다 다르게 보이게 만드는 핵심 기능,

                - 예시:
                    base.html: {% if session.user_name %} 이면 '로그아웃' 버튼을 보여주고, 
                                {% else %} 이면 '로그인' 버튼을 보여줌.

            4) 반복 노가다
                - 설명: 
                    데이터가 여러 개 담긴 뭉치(리스트)를 받았을 때, 
                    개발자가 일일이 코드를 복사하지 않아도 데이터 개수만큼 HTML 줄을 자동으로 생성해 줌.

                - 예시:
                    index.html: {% for comment in comments %} 코드를 통해 DB에 저장된 모든 댓글을 하나씩 꺼내어 화면에 리스트 형태로 나열함.

            5) 자동 길 찾기
                - 설명: 복잡한 웹 주소(URL)를 직접 입력하는 대신, 파이썬 함수의 이름만 보고 
                        현재 접속 가능한 정확한 주소로 변환해 줌. 
                        나중에 주소가 바뀌어도 코드를 수정할 필요가 없게 만듭니다.

                - 예시:
                    base.html: <a href="{{ url_for('profile') }}">내 프로필</a>라고 적으면 
                                Jinja2가 profile()이라는 이름의 함수가 있는지 app.py에서 찾고,
                                해당 함수 찾으면 함수 바로 위에 route 내부의 이름인 /profile 이라는 링크를 붙여줌.
                                페이지를 완성시켜셔, 완성된 페이지를 app.py가 서버로 전달.


    2. 백엔드

        1. 백엔드 전체 구조
            1) DB 연결 관리 (get_db)
                사용자의 요청이 들어올 때마다 sqlite3.connect를 통해 DB 파일을 열어줌

                효율적인 관리를 위해 Flask의 전역 객체인 g를 활용하여 
                한 번의 요청 동안 동일한 연결을 유지하도록 설계됨

            2) 핵심 로직 실행 (SQL문 활용)
                데이터 읽기(SELECT): 메인 페이지(index)에서는 JOIN 문법을 사용해 Comment와 User 테이블을 합쳐서 
                                    "댓글 내용 + 작성자 이름"을 한꺼번에 가져옴.

                데이터 쓰기(INSERT): 회원가입(register)이나 댓글 등록(index POST) 시 
                                    사용자가 보낸 값을 DB의 해당 테이블에 새 Row로 추가합니다.

                최종 저장(commit): 데이터를 추가하거나 수정했을 때는 반드시 db.commit()을 실행하여 
                                    변경 사항을 확정 짓습니다.

        2. Python/Flask 의 구체적인 기능
            1) URL 요청에 기능 더하기
                - Python 함수 위에 Flask의 @app.route(...) 데코레이터를 붙여서
                  특정 주소로 요청이 오면 함수를 실행하여 처리할 수 있도록 함.
                
                - 예시 :
                    로그인 버튼을 누르면 Jinja2가 숨겨둔 /login 링크로 가는 버튼이 눌리게 된다.
                    -> Flask가 login() 함수를 호출한다.
                    -> Python이 GET인지 POST인지 구분한다.
                    -> 어느 쪽이냐에 따라 다른 동작을 실행한다.
            
            2) 폼 데이터 처리
                - Flask : 브라우저가 보낸 폼 데이터를 꺼내게 해줌. request.form으로 받음.
                - Python : Flask 가 받아준 데이터를 변수에 저장해서, 여러 가지 처리를 함.

                - 예시 :
                    register 함수에서
                    if request.method == 'POST': -> 브라우저가 보낸 요청이 POST인지 확인. POST가 맞다면?
                    user_id = request.form['user_id']
                    password = request.form['password']
                    user_name = request.form['user_name'] -> 이렇게 Flask가 가져온 데이터를 파이썬이 변수에 저장.

            3) 로그인 상태 유지
                - Flask가 Session을 이용하여, 로그인에 성공하면 session에 아이디와 이름을 저장해둠.
                - 예시 : 
                    session['user_id'] = user['id']
                    session['user_name'] = user['user_name']

                    session은 전역변수 같은 느낌이라 따로 지정 안해줘도 여기저기서 다 쓸 수 있음.
            
            4) 데이터베이스에 회원/댓글 저장하기

                - python : SQL문을 실행해서 데이터를 추가하고, commit()으로 실제 저장을 확정함.
                - flask : 요청 중에 DB 연결을 사용할 수 있게 하고, 요청이 끝나면 연결을 정리함.
                - 예시 :
                    cursor.execute("INSERT INTO Comment (user_id, content) VALUES (?, ?)", ...)
                    db.commit()
                    -> 댓글 내용을 DB에 저장함.

                    Flask는 사용자가 주소에 접속하면, 그 요청을 처리하기 위한 "요청 컨텍스트"를 만듬.
                    -> 요청 컨텍스트 안에서 request, session, g 같은 객체를 쓸 수 있게 해줌. 
                    -> 이 때 g는 "현재 요청 동안만 잠깐만 쓰는 저장 공간"
                    -> python이 get_db 호출하면 -> g 안에 DB 연결 이미 있는지 확인
                    -> 있으면 그대로 재사용, 없으면 sqlite3.connect(DATABASE) 로 새 연결 만들고 g._database에 저장.

            5) 데이터베이스에서 정보 조회하기

                - python : SQL 조회문을 실행하고, 결과를 변수에 담아서 이후 로직에 사용함.
                - flask : 조회한 결과를 HTML 템플릿으로 넘겨서 화면에 출력할 수 있게 함.
                    -> "Python 코드에서 만든 데이터(comments, user 같은 값)를 HTML 파일로 전달"

                - 예시 :
                    cursor.execute("SELECT * FROM User WHERE user_id = ?", (user_id,))
                    user = cursor.fetchone()
                    -> 입력한 아이디에 해당하는 사용자 정보를 찾음.

                    return render_template('index.html', comments=comments)
                    이 코드는

                    index.html 파일을 열고
                    Python 변수 comments를 같이 넘겨주고
                    HTML 안에서 그 값을 쓸 수 있게 만드는 것

                    "Python이 DB에서 데이터를 가져오고, 
                    Flask가 그 데이터를 Jinja2 템플릿에 전달하면, 
                    Jinja2가 HTML 안의 빈 자리를 채워서 최종 화면을 만든다."

            6) 비밀번호 암호화와 로그인 인증

                - python : 비밀번호를 해시로 바꾸고, 로그인 때 입력값과 저장된 해시를 비교함.
                - flask : 로그인 요청 흐름 안에서 인증 로직이 실행되도록 구조를 제공함.
                - 예시 :
                    register() -> password_hash = generate_password_hash(password)
                    login -> check_password_hash(user['password_hash'], password)
                    -> 비밀번호를 안전하게 저장하고 검사함.
                    
            7) 로그인한 사용자만 기능 사용 가능하게 하기

                - python : if 조건문으로 세션을 확인해서 로그인 여부를 판단함.
                - flask : redirect()와 url_for()로 로그인 페이지 같은 다른 주소로 이동시킴.
                - 예시 :
                    if 'user_id' not in session:
                    return redirect(url_for('login'))
                    -> 로그인하지 않으면 해당 기능을 못 쓰게 막음.

            8) HTML에 데이터 넣어서 동적으로 페이지 만들기

            - python : DB에서 가져온 데이터나 변수값을 템플릿에 넘겨줄 준비를 함.
            - flask : render_template()로 HTML 파일과 Python 데이터를 연결함.
            - 예시 :
                return render_template('index.html', comments=comments)
                -> Flask가 comments를 HTML로 넘기고, 템플릿이 이를 화면에 출력함.

            9) 잘못된 입력이나 오류 처리하기

            - python : 입력값이 비었는지, 중복인지, 올바른지 등을 조건문으로 검사함.
            - flask : 오류 메시지와 상태코드(400, 401 등)를 HTTP 응답으로 보내줌.
            - 예시 :
                if not content:
                return "댓글 내용이 없습니다.", 400
                -> 잘못된 입력이면 에러 응답을 반환함.

            10) 앱 실행과 전체 요청 흐름 관리

            - python : 프로그램 시작 조건을 확인하고, 서버 실행 코드를 호출함.
            - flask : app.run()으로 개발 서버를 실행해서 브라우저 요청을 받을 수 있게 함.
            - 예시 :
                if __name__ == '__main__':
                app.run(debug=True)
                -> 이 파일을 직접 실행하면 Flask 웹 서버가 시작됨.


    3. DB
        1) User 테이블
            역할: 가입한 회원들의 정보를 영구적으로 보관

            주요 Column:

            id: 시스템이 각 사용자를 구분하기 위해 자동으로 붙이는 고유 번호(PK)

            user_id: 사용자가 로그인할 때 쓰는 아이디

            password_hash: 보안을 위해 암호화된 비밀번호

            user_name: 화면에 표시될 실제 이름

        2) Comment 테이블
            역할: 사용자들이 작성한 댓글 내용을 저장

            주요 Column:

            user_id: 이 댓글을 누가 썼는지 나타내는 번호
                    이 번호는 User 테이블의 id와 연결됨 (User 테이블의 id를 참조하는 FK)

            content: 댓글의 실제 내용

            timestamp: 댓글이 작성된 시간이며, 작성 시 자동으로 기록됨


    4. 프록시



3. 배포 과정
    1. 서버 배포
        - PythonAnywhere 선택
            - Python 웹 애플리케이션 배포에 특화되어 있어 Flask 프로젝트를 쉽게 배포할 수 있음.
            - SQLite를 그대로 사용할 수 있어 SQL을 그대로 유지한 채로 프로젝트를 배포할 수 있음.
        
        - 기존 프로젝트에서 서버 배포를 위해 수정이 필요한 부분 탐색 및 수정
            - app.py
                - DATABASE 경로 변환. PythonAnywhere 에서는 작업 디렉터리가 다를 수 있음.
                    DATABASE = 'database.db' 
                    → DATABASE = os.path.join(app.root_path, 'database.db')
                - SECRET_KEY를 환경변수 기반으로 변경
                  배포 시에 웹 앱 환경변수에서 설정할 수 있도록 함
                    SECRET_KEY = os.environ.get('SECRET_KEY')

                
                


    2. 프록시


    3. 도메인


    4. HTTPS


4. 막혔던 부분과 해결 방법




