import pymysql
from datetime import datetime
from logger import logger

# mysql과의 connection을 만드는 함수
def set_connection():
    conn = pymysql.connect(
        user="root",
        password="1234",
        host="localhost",
        db="basicboard",
        charset="utf8",
    )
    return conn


# 쿼리를 실행하는 함수
def execute_query(sql):
    print(sql)
    conn = set_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    conn.commit()
    conn.close()


def execute_get_query(sql, manny=False):
    print(sql)
    conn = set_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if manny:
        cursor.execute(sql)
        result = cursor.fetchall()
    else:
        cursor.execute(sql)
        result = cursor.fetchone()
    conn.commit()
    conn.close()
    return result


"""
유저 CRUD 코드
CRUD에 해당하는 코드들은 쿼리문만 만들고, 위에 정의한 함수로 쿼리를 실행한다.
리턴 값이 있는 경우(R)도 있다.
"""
# 유저 생성 C
def create_user(name, email, password, created_at):
    sql = f"INSERT INTO user (name, email, password, created_at) \
            VALUES('{name}', '{email}', '{password}', '{created_at}'); "
    execute_query(sql)


# 유저 정보 읽기 R
def get_user(pk):
    sql = f"SELECT * FROM user WHERE id = {pk};"
    result = execute_get_query(sql)
    return result


def get_users():
    sql = "SELECT * FROM user;"
    result = execute_get_query(sql, manny=True)
    return result


# 유저 정보 수정 U
def update_user(id, update_name):
    sql = f"UPDATE user SET name = '{update_name}' WHERE id = {id};"
    execute_query(sql)


# 유저 삭제 D
def delete_user(id):
    sql = f"DELETE FROM user WHERE id = {id};"
    execute_query(sql)


"""
게시글 CRUD 코드
CRUD에 해당하는 코드들은 쿼리문만 만들고, 위에 정의한 함수로 쿼리를 실행한다.
게시글은 유저와 외래키를 통해 관계를 맺고 있다.
리턴 값이 있는 경우(R)도 있다.
"""
# 게시글 생성
def create_article(user_id, title, content, created_at):
    sql = f"INSERT INTO article (title, content, user_id, created_at) \
            VALUES ('{title}', '{content}', '{user_id}', '{created_at}'); "
    execute_query(sql)


# 모든 게시글 읽기
def get_articles():
    sql = f"SELECT a.id, a.title, a.content, a.created_at, a.user_id, u.name, u.email \
        FROM article AS a \
        LEFT JOIN user AS u \
        ON a.user_id = u.id;"
    result = execute_get_query(sql, manny=True)
    logger.debug(result)
    return result


# 하나의 게시글 읽기
def get_article():
    pass


# 게시글 수정
def update_article():
    pass


# 게시글 지우기
def delete_article():
    pass


# now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
