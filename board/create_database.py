import pymysql
from datetime import datetime


# pymysql을 이용해 MySQL connection을 생성한다.
conn = pymysql.connect(
    user="root",
    password="1234",
    host="localhost",
    db="basicboard",
    charset="utf8",
)

# 쿼리 결과를 딕셔너리로 변환해주는 옵션 'pymysql.cursors.DictCursor'
# https://yurimkoo.github.io/python/2019/09/14/connect-db-with-python.html
cursor = conn.cursor(pymysql.cursors.DictCursor)

# create user table
create_user_table = "CREATE TABLE IF NOT EXISTS user \
                    (id INT AUTO_INCREMENT PRIMARY KEY, \
                    name VARCHAR(128) NOT NULL, \
                    email VARCHAR(256) NOT NULL, \
                    password VARCHAR(512) NOT NULL, \
                    created_at DATETIME NOT NULL, \
                    UNIQUE(name, email));"

# create article table
create_article_table = "CREATE TABLE IF NOT EXISTS article (\
                        id INT AUTO_INCREMENT PRIMARY KEY, \
                        title VARCHAR(1024) NOT NULL, \
                        content TEXT NOT NULL, \
                        created_at DATE NOT NULL, \
                        user_id INT NOT NULL, \
                        FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE); "


# query 실행
cursor.execute(create_user_table)
cursor.execute(create_article_table)
conn.commit()

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# admin 유저 생성
sql = 'INSERT INTO user (name, email, password, created_at) \
        VALUES ("admin", "admin@naver.com", "1234", %s); '

# query 실행
cursor.execute(sql, now)
cursor.execute("SELECT * FROM user;")
conn.commit()

# select * from user;의 결과를 하나만 가져옴
# cursor.fetchall()을 사용하면 select * from user;의 결과를 모두 가져 올 수 있음.
user = cursor.fetchone()
print(user)

# connection은 항상 닫아줘야 한다.
conn.close()