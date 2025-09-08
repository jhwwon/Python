"""
은행 유틸리티 클래스
Java의 BankUtils 클래스를 Python으로 변환
"""

from datetime import datetime
from typing import Optional
from ..database import get_database_connection


class BankUtils:
    """은행 관련 유틸리티 메서드들을 제공하는 클래스"""
    
    @staticmethod
    def format_currency(amount: float) -> str:
        """
        금액을 통화 형식으로 포맷팅
        
        Args:
            amount: 포맷팅할 금액
            
        Returns:
            str: 포맷팅된 금액 문자열 (예: "1,000원")
        """
        return f"{amount:,.0f}원"
    
    @staticmethod
    def format_date(date: datetime) -> str:
        """
        날짜를 문자열로 포맷팅
        
        Args:
            date: 포맷팅할 날짜
            
        Returns:
            str: 포맷팅된 날짜 문자열 (예: "2024-01-01 12:00:00")
        """
        return date.strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def generate_account_number() -> Optional[str]:
        """
        새로운 계좌번호 생성 (기본 형식: 110-234-000001)
        
        Returns:
            str: 생성된 계좌번호 또는 None (오류 시)
        """
        try:
            db = get_database_connection()
            with db.get_cursor() as cursor:
                cursor.execute("SELECT '110-234-' || LPAD(SEQ_ACCOUNT.NEXTVAL, 6, '0') FROM DUAL")
                result = cursor.fetchone()
                if result:
                    return result[0]
        except Exception as e:
            print(f"계좌번호 생성 오류: {e}")
        return None
    
    @staticmethod
    def generate_transaction_id() -> Optional[str]:
        """
        새로운 거래번호 생성 (기본 형식: T00000001)
        
        Returns:
            str: 생성된 거래번호 또는 None (오류 시)
        """
        try:
            db = get_database_connection()
            with db.get_cursor() as cursor:
                cursor.execute("SELECT 'T' || LPAD(SEQ_TRANSACTION.NEXTVAL, 8, '0') FROM DUAL")
                result = cursor.fetchone()
                if result:
                    return result[0]
        except Exception as e:
            print(f"거래번호 생성 오류: {e}")
        return None
    
    @staticmethod
    def generate_payment_id() -> str:
        """
        새로운 이자 지급 ID 생성 (기본 형식: PAY00000001)
        
        Returns:
            str: 생성된 이자 지급 ID
        """
        try:
            db = get_database_connection()
            with db.get_cursor() as cursor:
                cursor.execute("SELECT COUNT(*) + 1 FROM interest_payments")
                result = cursor.fetchone()
                if result:
                    next_number = result[0]
                    return f"PAY{next_number:08d}"
        except Exception as e:
            print(f"이자 지급 ID 생성 오류: {e}")
        
        # 오류 시 기본값
        return "PAY00000001"
    
    @staticmethod
    def get_counterpart_display(transaction_type: str, counterpart_name: Optional[str] = None,
                              depositor_name: Optional[str] = None, 
                              counterpart_account: Optional[str] = None) -> str:
        """
        거래 유형에 따른 상대방 정보 표시 형식 결정
        
        Args:
            transaction_type: 거래 유형
            counterpart_name: 상대방 이름
            depositor_name: 입금자명
            counterpart_account: 상대방 계좌번호
            
        Returns:
            str: 포맷팅된 상대방 정보
        """
        if transaction_type == "이체입금":
            if counterpart_name:
                return f"보낸사람: {counterpart_name}"
            elif counterpart_account:
                return f"보낸계좌: {counterpart_account}"
            else:
                return "-"
        elif transaction_type == "이체출금":
            if counterpart_name:
                return f"받는사람: {counterpart_name}"
            elif counterpart_account:
                return f"받는계좌: {counterpart_account}"
            else:
                return "-"
        elif transaction_type == "입금":
            if depositor_name:
                return f"입금자: {depositor_name}"
            else:
                return "-"
        else:
            return "-"
    
    @staticmethod
    def validate_account_number(account_number: str) -> bool:
        """
        계좌번호 형식 유효성 검사
        
        Args:
            account_number: 검사할 계좌번호
            
        Returns:
            bool: 유효한 형식인지 여부
        """
        if not account_number:
            return False
        
        # 110-234-000001 형식 검사
        parts = account_number.split('-')
        if len(parts) != 3:
            return False
        
        try:
            # 각 부분이 숫자인지 확인
            int(parts[0])  # 110
            int(parts[1])  # 234
            int(parts[2])  # 000001
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_transaction_id(transaction_id: str) -> bool:
        """
        거래번호 형식 유효성 검사
        
        Args:
            transaction_id: 검사할 거래번호
            
        Returns:
            bool: 유효한 형식인지 여부
        """
        if not transaction_id:
            return False
        
        # T00000001 형식 검사
        if not transaction_id.startswith('T'):
            return False
        
        try:
            int(transaction_id[1:])  # T 이후 부분이 숫자인지 확인
            return len(transaction_id) == 9  # T + 8자리 숫자
        except ValueError:
            return False
    
    @staticmethod
    def format_balance(balance: float) -> str:
        """
        잔액을 보기 좋게 포맷팅
        
        Args:
            balance: 잔액
            
        Returns:
            str: 포맷팅된 잔액
        """
        if balance >= 0:
            return f"{balance:,.0f}원"
        else:
            return f"-{abs(balance):,.0f}원"
