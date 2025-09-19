"""
Oracle 데이터베이스 연동을 통한 노트북 데이터 저장
DB 연동 프로세스 구현
"""

import oracledb
import pandas as pd
import sys

class OracleDataManager:
    """Oracle 데이터베이스 관리 클래스"""
    
    def __init__(self):
        """초기화"""
        self.connection = None
        self.cursor = None
        
        # 데이터베이스 연결 정보
        self.db_config = {
            'user': 'jhw1',
            'password': '1234',
            'dsn': 'localhost:1521/orcl'
        }
        
        # 저장할 데이터 (리스트 형태)
        self.laptop_data = [
            ['삼성쇼핑몰', '노트북 플러스2 NT550XDA-K14A 최종43만 가성비노트북 윈11탑재 대학생추천 인강용 교육용 사무용 재택용', 469000],
            ['컴퓨터전문판매점', 'V15 GEN2-82KD000WKR 단하루 49만구매 AMD 라이젠 R5-5500U 4GB NVMe256GB 윈도우10탑재', 527000],
            ['코인비엠에스', '갤럭시북3 NT750XFT-A71A 최종119만/최신 인텔 13세대 i7 FHD 고성능 업무용 대학생노트북', 1348000],
            ['코인비엠에스', '갤럭시북2 NT550XED-K78A 최종:99만/인텔 i7 윈도우11 탑재 즉시사용 대학생 인강용 노트북', 1099000],
            ['삼성전자몰엔씨디지텍', '갤럭시북3 프로 NT940XFT-A51A 최종가154만 13세대i5 /16G/256G/14인치 WQXGA+ 사무용 인강용 삼성노트북', 1699000]
        ]
    
    def step1_create_database(self):
        """1단계: Oracle 데이터베이스 생성 후 선택"""
        print("=" * 50)
        print("1단계: Oracle 데이터베이스 선택")
        print("=" * 50)
        print(f"데이터베이스: ORCL ({self.db_config['dsn']})")
        print(f"사용자: {self.db_config['user']}")
        print()
    
    def step2_create_table(self):
        """2단계: 테이블 생성 후 구조 확인"""
        print("=" * 50)
        print("2단계: 테이블 생성")
        print("=" * 50)
        
        try:
            # 테이블 생성 SQL
            create_table_sql = """
            CREATE TABLE top5List (
                seller VARCHAR2(100) NOT NULL,
                item VARCHAR2(500) NOT NULL,
                price NUMBER(10) NOT NULL
            )
            """
            
            # 기존 테이블 삭제 (있다면)
            drop_table_sql = "DROP TABLE top5List CASCADE CONSTRAINTS"
            
            try:
                self.cursor.execute(drop_table_sql)
                print("기존 테이블 삭제 완료")
            except:
                print("기존 테이블이 없습니다")
            
            # 테이블 생성
            self.cursor.execute(create_table_sql)
            self.connection.commit()
            print("top5List 테이블 생성 완료")
            print("테이블 구조: seller, item, price")
            
        except Exception as e:
            print(f"테이블 생성 오류: {e}")
            raise
    
    def step3_check_libraries(self):
        """3단계: 파이썬에서 필요한 라이브러리 확인"""
        print("=" * 50)
        print("3단계: 라이브러리 확인")
        print("=" * 50)
        
        required_libraries = ['oracledb', 'pandas']
        
        print("필요한 라이브러리:")
        for lib in required_libraries:
            try:
                if lib == 'oracledb':
                    import oracledb
                    print(f"- {lib}: 설치됨")
                elif lib == 'pandas':
                    import pandas
                    print(f"- {lib}: 설치됨")
            except ImportError:
                print(f"- {lib}: 설치 필요")
        print()
    
    def step4_connection(self):
        """4단계: 파이썬에서 connection 자원 할당 받기"""
        print("=" * 50)
        print("4단계: 데이터베이스 연결")
        print("=" * 50)
        
        try:
            # Oracle 데이터베이스 연결
            self.connection = oracledb.connect(
                user=self.db_config['user'],
                password=self.db_config['password'],
                dsn=self.db_config['dsn']
            )
            
            # 커서 생성
            self.cursor = self.connection.cursor()
            
            print("데이터베이스 연결 성공")
            print(f"연결 정보: {self.db_config['dsn']}")
            print(f"사용자: {self.db_config['user']}")
            
            # 연결 테스트
            self.cursor.execute("SELECT 1 FROM DUAL")
            result = self.cursor.fetchone()
            print(f"연결 테스트: {result[0]}")
            
        except Exception as e:
            print(f"데이터베이스 연결 오류: {e}")
            raise
    
    def step5_create_query(self):
        """5단계: 쿼리 만들기"""
        print("=" * 50)
        print("5단계: 쿼리 생성")
        print("=" * 50)
        
        # INSERT 쿼리
        self.insert_query = """
        INSERT INTO top5List (seller, item, price)
        VALUES (:seller, :item, :price)
        """
        
        # SELECT 쿼리 (확인용)
        self.select_query = """
        SELECT seller, item, price
        FROM top5List
        ORDER BY seller
        """
        
        print("INSERT 쿼리 생성 완료")
        print("SELECT 쿼리 생성 완료")
        print()
    
    def step6_execute_query(self):
        """6단계: 쿼리 실행하기"""
        print("=" * 50)
        print("6단계: 쿼리 실행")
        print("=" * 50)
        
        try:
            # 데이터 삽입
            print("데이터 삽입 중...")
            for i, data in enumerate(self.laptop_data, 1):
                # 리스트를 딕셔너리로 변환
                data_dict = {
                    'seller': data[0],
                    'item': data[1], 
                    'price': data[2]
                }
                self.cursor.execute(self.insert_query, data_dict)
                print(f"{i}. {data[0]} - {data[1][:30]}... 삽입 완료")
            
            # 커밋
            self.connection.commit()
            print(f"총 {len(self.laptop_data)}개 데이터 삽입 완료")
            print("트랜잭션 커밋 완료")
            
        except Exception as e:
            print(f"쿼리 실행 오류: {e}")
            self.connection.rollback()
            raise
    
    def step7_verify_data(self):
        """7단계: 데이터베이스에 저장이 되었는지 확인"""
        print("=" * 50)
        print("7단계: 데이터 확인")
        print("=" * 50)
        
        try:
            # 저장된 데이터 조회
            self.cursor.execute(self.select_query)
            results = self.cursor.fetchall()
            
            print(f"저장된 데이터 수: {len(results)}개")
            print("\n저장된 데이터 목록:")
            print("┌" + "─" * 15 + "┬" + "─" * 40 + "┬" + "─" * 10 + "┐")
            print("│" + f"{'seller':<15}" + "│" + f"{'item':<40}" + "│" + f"{'price':<10}" + "│")
            print("├" + "─" * 15 + "┼" + "─" * 40 + "┼" + "─" * 10 + "┤")
            
            for row in results:
                seller, item, price = row
                # item이 40자를 넘으면 잘라서 표시
                item_display = item[:37] + "..." if len(item) > 40 else item
                print("│" + f"{seller:<15}" + "│" + f"{item_display:<40}" + "│" + f"{price:>10,}" + "│")
            
            print("└" + "─" * 15 + "┴" + "─" * 40 + "┴" + "─" * 10 + "┘")
            
        except Exception as e:
            print(f"데이터 확인 오류: {e}")
            raise
    
    def cleanup(self):
        """리소스 정리"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            print("\n데이터베이스 연결 종료")
        except:
            pass
    
    def run_all_steps(self):
        """모든 단계 실행"""
        try:
            print("Oracle 데이터베이스 연동 프로세스 시작")
            print("=" * 50)
            
            # 1단계: 데이터베이스 선택
            self.step1_create_database()
            
            # 4단계: 연결 (테이블 생성 전에 연결 필요)
            self.step4_connection()
            
            # 2단계: 테이블 생성
            self.step2_create_table()
            
            # 3단계: 라이브러리 확인
            self.step3_check_libraries()
            
            # 5단계: 쿼리 생성
            self.step5_create_query()
            
            # 6단계: 쿼리 실행
            self.step6_execute_query()
            
            # 7단계: 데이터 확인
            self.step7_verify_data()
            
            print("\n모든 단계가 성공적으로 완료되었습니다!")
            
        except Exception as e:
            print(f"\n오류 발생: {e}")
            raise
        finally:
            self.cleanup()


def main():
    """메인 함수"""
    print("Oracle 데이터베이스 연동을 통한 노트북 데이터 저장")
    print("과제: 7단계 DB 연동 프로세스 구현")
    print("=" * 60)
    
    db_manager = OracleDataManager()
    
    try:
        db_manager.run_all_steps()
    except Exception as e:
        print(f"프로그램 실행 중 오류: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
