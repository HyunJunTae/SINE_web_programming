import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, g
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'super_secret_key')  # 배포 시에는 PythonAnywhere 환경 변수로 설정하세요.
DATABASE = os.path.join(app.root_path, 'database.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        content = request.form['content']
        if not content:
            return "댓글 내용이 없습니다.", 400
            
        cursor.execute(
            "INSERT INTO Comment (user_id, content) VALUES (?, ?)",
            (session['user_id'], content)
        )
        db.commit()
        return redirect(url_for('index'))

    # GET 요청: 로그인한 사용자만 댓글 목록 조회
    comments = []
    logged_in = 'user_id' in session
    if logged_in:
        cursor.execute('''
            SELECT Comment.content, Comment.timestamp, User.user_name 
            FROM Comment 
            JOIN User ON Comment.user_id = User.id
            ORDER BY Comment.timestamp DESC
        ''')
        comments = cursor.fetchall()
    
    return render_template('index.html', comments=comments, logged_in=logged_in)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        user_name = request.form['user_name']

        if not user_id or not password or not user_name:
            # 간단한 유효성 검사
            return "모든 필드를 입력해주세요.", 400

        db = get_db()
        cursor = db.cursor()
        
        # 아이디 중복 확인
        cursor.execute("SELECT * FROM User WHERE user_id = ?", (user_id,))
        if cursor.fetchone():
            return "이미 존재하는 아이디입니다.", 400

        # 비밀번호 해시 처리 및 사용자 추가
        password_hash = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO User (user_id, password_hash, user_name) VALUES (?, ?, ?)",
            (user_id, password_hash, user_name)
        )
        db.commit()

        return redirect(url_for('login'))
    
    # GET 요청 시 회원가입 페이지 렌더링
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM User WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session['user_id'] = user['id']
            session['user_name'] = user['user_name']
            return redirect(url_for('index'))
        
        return "아이디 또는 비밀번호가 잘못되었습니다.", 401
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    # 로그인하지 않은 사용자는 로그인 페이지로 리디렉션
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    cursor = db.cursor()
    
    # 세션에 저장된 user_id를 이용해 사용자 정보 조회
    cursor.execute("SELECT * FROM User WHERE id = ?", (session['user_id'],))
    user = cursor.fetchone()
    
    if user is None:
        # 혹시 모를 오류 처리 (세션에 ID는 있는데 DB에 사용자가 없는 경우)
        session.clear()
        return redirect(url_for('login'))

    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=False)

"""
    
(상단) import ...: Flask 자체와 웹 개발에 필요한 여러 기능들(render_template, request 등)을 불러옵니다.
app = Flask(__name__): Flask 애플리케이션 객체를 생성하여 app 변수에 저장합니다. 모든 Flask 웹의 시작점입니다.
app.secret_key = ...: 세션 관리에 사용될 비밀 키입니다. Flask가 브라우저에 보내는 세션 데이터를 암호화하고 위변조를 방지하기 위해 사용합니다.
DATABASE = 'database.db': 데이터베이스 파일 이름을 변수로 저장해두어 나중에 관리하기 편하게 합니다.
get_db()와 close_connection(): 데이터베이스에 효율적으로 연결하고 연결을 해제하는 도우미 함수들입니다. 요청이 시작될 때 DB에 연결하고, 요청이 끝날 때 자동으로 연결을 닫아 리소스를 아낍니다.
@app.route('/'): 메인 페이지 라우트. 사용자가 웹사이트의 가장 기본 주소(http://127.0.0.1:5000/)에 접속했을 때 index() 함수를 실행하라고 Flask에게 알려줍니다.
@app.route('/register', ...): 회원가입 페이지 라우트. /register 주소로 접속했을 때 register() 함수를 실행합니다. methods=['GET', 'POST']는 GET(페이지 보여줘) 요청과 POST(데이터 제출할게) 요청을 모두 처리하겠다는 의미입니다.
@app.route('/login', ...): 로그인 페이지 라우트. /login 주소와 login() 함수를 연결합니다.
@app.route('/logout'): 로그아웃 라우트. /logout 주소와 logout() 함수를 연결합니다.
if __name__ == '__main__': ...: 이 파이썬 파일이 직접 실행되었을 때만 app.run(debug=True)를 실행하라는 의미입니다. app.run()은 실제로 웹 서버를 가동시키는 명령입니다. debug=True는 개발 중에 코드를 수정하면 서버가 자동으로 재시작되게 하는 편리한 옵션입니다.
    
"""