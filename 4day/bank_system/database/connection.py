"""
데이터베이스 연결 관리 클래스
Java의 Oracle JDBC 연결을 Python으로 변환
"""

import oracledb
from typing import Optional, Dict, Any, List
from contextlib import contextmanager
import logging


class DatabaseConnection:
    """Oracle 데이터베이스 연결을 관리하는 클래스"""
    
    def __init__(self, host: str = "localhost", port: int = 1521, 
                 service_name: str = "orcl", username: str = "jhw1", 
                 password: str = "1234"):
        """
        데이터베이스 연결 정보 초기화
        
        Args:
            host: 데이터베이스 호스트
            port: 데이터베이스 포트
            service_name: 서비스 이름
            username: 사용자명
            password: 비밀번호
        """
        self.host = host
        self.port = port
        self.service_name = service_name
        self.username = username
        self.password = password
        self.connection: Optional[oracledb.Connection] = None
        
        # 로깅 설정
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def connect(self) -> bool:
        """
        데이터베이스에 연결
        
        Returns:
            bool: 연결 성공 여부
        """
        try:
            # Oracle 연결 문자열 생성
            dsn = f"{self.host}:{self.port}/{self.service_name}"
            
            # 데이터베이스 연결
            self.connection = oracledb.connect(
                user=self.username,
                password=self.password,
                dsn=dsn
            )
            
            # 자동 커밋 설정 (Java의 setAutoCommit(true)와 동일)
            self.connection.autocommit = True
            
            self.logger.info("은행 계좌 시스템 DB 연결 성공!")
            return True
            
        except oracledb.DatabaseError as e:
            self.logger.error(f"데이터베이스 연결 실패: {e}")
            return False
        except Exception as e:
            self.logger.error(f"예상치 못한 오류: {e}")
            return False
    
    def disconnect(self):
        """데이터베이스 연결 종료"""
        try:
            if self.connection:
                self.connection.close()
                self.connection = None
                self.logger.info("데이터베이스 연결이 정상적으로 종료되었습니다.")
        except oracledb.DatabaseError as e:
            self.logger.error(f"DB 연결 종료 중 오류: {e}")
    
    def is_connected(self) -> bool:
        """연결 상태 확인"""
        try:
            if self.connection:
                # 간단한 쿼리로 연결 상태 확인
                cursor = self.connection.cursor()
                cursor.execute("SELECT 1 FROM DUAL")
                cursor.close()
                return True
        except:
            pass
        return False
    
    @contextmanager
    def get_cursor(self):
        """
        컨텍스트 매니저를 사용한 커서 관리
        
        Usage:
            with db.get_cursor() as cursor:
                cursor.execute("SELECT * FROM users")
                result = cursor.fetchall()
        """
        if not self.connection:
            raise Exception("데이터베이스에 연결되지 않았습니다.")
        
        cursor = self.connection.cursor()
        try:
            yield cursor
        finally:
            cursor.close()
    
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        SELECT 쿼리 실행
        
        Args:
            query: SQL 쿼리
            params: 쿼리 매개변수
            
        Returns:
            List[Dict]: 쿼리 결과
        """
        try:
            with self.get_cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                # 컬럼명 가져오기
                columns = [desc[0] for desc in cursor.description]
                
                # 결과를 딕셔너리 리스트로 변환
                results = []
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                
                return results
                
        except oracledb.DatabaseError as e:
            self.logger.error(f"쿼리 실행 실패: {e}")
            raise
    
    def execute_update(self, query: str, params: Optional[Dict[str, Any]] = None) -> int:
        """
        INSERT, UPDATE, DELETE 쿼리 실행
        
        Args:
            query: SQL 쿼리
            params: 쿼리 매개변수
            
        Returns:
            int: 영향받은 행 수
        """
        try:
            with self.get_cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                return cursor.rowcount
                
        except oracledb.DatabaseError as e:
            self.logger.error(f"업데이트 실행 실패: {e}")
            raise
    
    def execute_many(self, query: str, params_list: List[Dict[str, Any]]) -> int:
        """
        여러 행을 한 번에 처리하는 쿼리 실행
        
        Args:
            query: SQL 쿼리
            params_list: 매개변수 리스트
            
        Returns:
            int: 처리된 행 수
        """
        try:
            with self.get_cursor() as cursor:
                cursor.executemany(query, params_list)
                return cursor.rowcount
                
        except oracledb.DatabaseError as e:
            self.logger.error(f"배치 실행 실패: {e}")
            raise
    
    def commit(self):
        """트랜잭션 커밋"""
        if self.connection:
            self.connection.commit()
    
    def rollback(self):
        """트랜잭션 롤백"""
        if self.connection:
            self.connection.rollback()
    
    def __enter__(self):
        """컨텍스트 매니저 진입"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """컨텍스트 매니저 종료"""
        self.disconnect()
    
    def __del__(self):
        """소멸자에서 연결 정리"""
        self.disconnect()


# 전역 데이터베이스 연결 인스턴스 (Java의 BankSystem 클래스와 동일한 방식)
_db_connection: Optional[DatabaseConnection] = None


def get_database_connection() -> DatabaseConnection:
    """
    전역 데이터베이스 연결 인스턴스 반환
    
    Returns:
        DatabaseConnection: 데이터베이스 연결 객체
    """
    global _db_connection
    if _db_connection is None:
        _db_connection = DatabaseConnection()
        if not _db_connection.connect():
            raise Exception("데이터베이스 연결에 실패했습니다.")
    return _db_connection


def close_database_connection():
    """전역 데이터베이스 연결 종료"""
    global _db_connection
    if _db_connection:
        _db_connection.disconnect()
        _db_connection = None
