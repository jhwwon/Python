"""
이자 계산기 클래스
Java의 InterestCalculator 클래스를 Python으로 변환
"""

from datetime import datetime, date
from typing import Optional
from ..database import get_database_connection
from ..entities.interest import InterestInfo


class InterestCalculator:
    """이자 계산 관련 유틸리티 메서드들을 제공하는 클래스"""
    
    # 계좌 종류별 연이자율 상수
    SAVINGS_RATE = 0.001      # 보통예금 0.1%
    FIXED_RATE = 0.015        # 정기예금 1.5%
    INSTALLMENT_RATE = 0.020  # 적금 2.0%
    
    @classmethod
    def get_interest_rate_by_type(cls, account_type: str) -> float:
        """
        계좌 종류에 따른 이자율 반환
        
        Args:
            account_type: 계좌 종류
            
        Returns:
            float: 이자율
        """
        rate_map = {
            "보통예금": cls.SAVINGS_RATE,
            "정기예금": cls.FIXED_RATE,
            "적금": cls.INSTALLMENT_RATE
        }
        return rate_map.get(account_type, 0.0)
    
    @staticmethod
    def calculate_days_between(start_date: datetime, end_date: datetime) -> int:
        """
        두 날짜 사이의 일수 계산
        
        Args:
            start_date: 시작 날짜
            end_date: 종료 날짜
            
        Returns:
            int: 경과 일수
        """
        if isinstance(start_date, datetime):
            start_date = start_date.date()
        if isinstance(end_date, datetime):
            end_date = end_date.date()
        
        return (end_date - start_date).days
    
    @staticmethod
    def calculate_interest(principal: float, annual_rate: float, days: int) -> float:
        """
        이자 계산 (일괄 계산)
        공식: (원금 × 연이자율 × 경과일수) ÷ 365
        
        Args:
            principal: 원금
            annual_rate: 연이자율
            days: 경과 일수
            
        Returns:
            float: 계산된 이자 금액 (원 단위 이하 반올림)
        """
        if principal <= 0 or annual_rate <= 0 or days <= 0:
            return 0.0
        
        interest = (principal * annual_rate * days) / 365.0
        
        # 원 단위 이하 반올림
        return round(interest)
    
    @staticmethod
    def calculate_account_interest(account_id: str) -> Optional[InterestInfo]:
        """
        특정 계좌의 이자 계산 (DB 조회 포함)
        
        Args:
            account_id: 계좌번호
            
        Returns:
            InterestInfo: 이자 정보 객체 또는 None (이자 지급 대상이 아닌 경우)
        """
        try:
            db = get_database_connection()
            query = """
                SELECT balance, interest_rate, last_interest_date, account_type 
                FROM accounts WHERE account_id = :account_id
            """
            
            results = db.execute_query(query, {'account_id': account_id})
            
            if results:
                data = results[0]
                balance = data['balance']
                interest_rate = data['interest_rate']
                last_interest_date = data['last_interest_date']
                account_type = data['account_type']
                
                # 현재 날짜
                current_date = datetime.now()
                
                # 경과 일수 계산
                days = InterestCalculator.calculate_days_between(last_interest_date, current_date)
                
                # 이자 계산 (최소 1일 이상일 때만)
                if days >= 1:
                    interest_amount = InterestCalculator.calculate_interest(
                        balance, interest_rate, days
                    )
                    
                    return InterestInfo(
                        account_id=account_id,
                        principal=balance,
                        interest_rate=interest_rate,
                        last_interest_date=last_interest_date,
                        current_date=current_date,
                        days=days,
                        interest_amount=interest_amount,
                        account_type=account_type
                    )
            
        except Exception as e:
            print(f"이자 계산 오류: {e}")
        
        return None  # 이자 지급 대상이 아님
    
    @staticmethod
    def format_interest_rate(rate: float) -> str:
        """
        이자율을 퍼센트 문자열로 반환
        
        Args:
            rate: 이자율 (소수)
            
        Returns:
            str: 퍼센트 형식의 이자율 (예: "1.5%")
        """
        return f"{rate * 100:.1f}%"
    
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
    
    @classmethod
    def get_all_interest_eligible_accounts(cls) -> list:
        """
        이자 지급 대상인 모든 계좌 조회
        
        Returns:
            list: 이자 지급 대상 계좌 리스트
        """
        try:
            db = get_database_connection()
            query = """
                SELECT account_id, balance, interest_rate, last_interest_date, account_type
                FROM accounts 
                WHERE balance > 0 AND interest_rate > 0
                ORDER BY account_id
            """
            
            results = db.execute_query(query)
            eligible_accounts = []
            
            for data in results:
                account_id = data['account_id']
                interest_info = cls.calculate_account_interest(account_id)
                
                if interest_info and interest_info.interest_amount > 0:
                    eligible_accounts.append(interest_info)
            
            return eligible_accounts
            
        except Exception as e:
            print(f"이자 지급 대상 계좌 조회 오류: {e}")
            return []
    
    @staticmethod
    def calculate_total_interest_amount(interest_list: list) -> float:
        """
        이자 리스트의 총 이자 금액 계산
        
        Args:
            interest_list: InterestInfo 객체 리스트
            
        Returns:
            float: 총 이자 금액
        """
        return sum(interest.interest_amount for interest in interest_list)
    
    @staticmethod
    def get_interest_summary(interest_list: list) -> dict:
        """
        이자 지급 요약 정보 생성
        
        Args:
            interest_list: InterestInfo 객체 리스트
            
        Returns:
            dict: 이자 지급 요약 정보
        """
        if not interest_list:
            return {
                'total_accounts': 0,
                'total_amount': 0,
                'by_type': {}
            }
        
        summary = {
            'total_accounts': len(interest_list),
            'total_amount': InterestCalculator.calculate_total_interest_amount(interest_list),
            'by_type': {}
        }
        
        # 계좌 종류별 집계
        for interest in interest_list:
            account_type = interest.account_type
            if account_type not in summary['by_type']:
                summary['by_type'][account_type] = {
                    'count': 0,
                    'amount': 0
                }
            
            summary['by_type'][account_type]['count'] += 1
            summary['by_type'][account_type]['amount'] += interest.interest_amount
        
        return summary
