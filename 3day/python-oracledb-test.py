#oracleDB 접속 테스트
import oracledb

try:
    # 데이터베이스 연결 정보 (사용자 이름, 비밀번호, 연결할 데이터베이스의 주소)
    # DNS(Data Source Name) 또는 사용자명/비밀번호@호스트:포트/서비스명 형식으로 접속
    conn = oracledb.connect(user="jhw1", password="1234", dsn="localhost:1521/orcl")

    print("데이터베이스에 성공적으로 연결되었습니다.")

    # 커서 객체 생성
    cursor = conn.cursor()
    # SQL 쿼리 실행
    cursor.execute("INSERT INTO admins(admin_id, admin_name, admin_password) VALUES ('admin1', '관리자1', '비밀번호1')")
    conn.commit()  # 변경사항 커밋

    cursor.execute("SELECT admin_id, admin_name, admin_password FROM admins")

    # 결과 출력
    for row in cursor: # 각 행(row)은 튜플 형태로 반환됨
        print("관리자 ID:", row[0], "관리자 이름:", row[1], "관리자 비밀번호:", row[2])

except oracledb.DatabaseError as e:
    print("데이터베이스 연결 오류:", e)
finally:
    if 'conn' in locals() and conn:
        conn.close()