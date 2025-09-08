"""
이자 관련 엔티티 클래스들
Java의 InterestInfo와 InterestPayment 클래스를 Python으로 변환
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class InterestInfo:
    """이자 계산 정보를 담는 클래스"""
    
    account_id: str                 # 이자를 계산할 계좌번호
    principal: float                # 원금
    interest_rate: float            # 연 이자율
    last_interest_date: datetime    # 마지막 이자 지급일(이자 계산 시작점)
    current_date: datetime          # 현재 날짜
    days: int                       # 경과 일수
    interest_amount: float          # 계산된 이자 금액
    account_type: str               # 계좌 종류
    
    def __str__(self) -> str:
        """이자 정보를 문자열로 반환"""
        return f"InterestInfo(account={self.account_id}, amount={self.interest_amount:,.0f}원)"
    
    def format_info(self) -> str:
        """이자 정보를 문자열로 포맷팅 (Java의 formatInfo() 메서드와 동일)"""
        return (
            f"계좌: {self.account_id} | 원금: {self.principal:,.0f}원 | "
            f"이자율: {self.interest_rate * 100:.1f}% | 경과일: {self.days}일 | "
            f"이자: {self.interest_amount:,.0f}원"
        )
    
    def to_dict(self) -> dict:
        """이자 정보를 딕셔너리로 변환"""
        return {
            'account_id': self.account_id,
            'principal': self.principal,
            'interest_rate': self.interest_rate,
            'last_interest_date': self.last_interest_date,
            'current_date': self.current_date,
            'days': self.days,
            'interest_amount': self.interest_amount,
            'account_type': self.account_type
        }


@dataclass
class InterestPayment:
    """이자 지급 내역을 담는 클래스"""
    
    payment_id: str                 # 이자 지급 고유 번호
    account_id: str                 # 이자를 받는 계좌
    payment_date: Optional[datetime] = None  # 이자 지급일
    interest_amount: float = 0.0    # 지급된 이자 금액
    admin_id: str = ""              # 이자 지급을 실행한 관리자
    
    def __post_init__(self):
        """객체 생성 후 초기화"""
        if self.payment_date is None:
            self.payment_date = datetime.now()
    
    def __str__(self) -> str:
        """이자 지급 정보를 문자열로 반환"""
        return f"InterestPayment(id={self.payment_id}, account={self.account_id}, amount={self.interest_amount:,.0f}원)"
    
    def to_dict(self) -> dict:
        """이자 지급 정보를 딕셔너리로 변환 (DB 저장용)"""
        return {
            'payment_id': self.payment_id,
            'account_id': self.account_id,
            'payment_date': self.payment_date,
            'interest_amount': self.interest_amount,
            'admin_id': self.admin_id
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'InterestPayment':
        """딕셔너리에서 InterestPayment 객체 생성 (DB 조회용)"""
        return cls(
            payment_id=data.get('PAYMENT_ID', data.get('payment_id', '')),
            account_id=data.get('ACCOUNT_ID', data.get('account_id', '')),
            payment_date=data.get('PAYMENT_DATE', data.get('payment_date', None)),
            interest_amount=data.get('INTEREST_AMOUNT', data.get('interest_amount', 0.0)),
            admin_id=data.get('ADMIN_ID', data.get('admin_id', ''))
        )
    
    @classmethod
    def create_payment(cls, payment_id: str, account_id: str, 
                      interest_amount: float, admin_id: str) -> 'InterestPayment':
        """이자 지급용 객체 생성 (Java의 생성자와 동일)"""
        return cls(
            payment_id=payment_id,
            account_id=account_id,
            interest_amount=interest_amount,
            admin_id=admin_id
        )
