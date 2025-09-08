"""
계좌 엔티티 클래스
Java의 Account 클래스를 Python으로 변환
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Account:
    """계좌 정보를 담는 클래스"""
    
    account_id: str                 # 계좌번호
    account_name: str               # 계좌명
    account_type: str               # 계좌종류 (보통예금, 정기예금, 적금)
    account_password: str           # 계좌 비밀번호
    balance: float                  # 계좌 잔액
    user_id: str                    # 계좌 소유자 ID
    create_date: Optional[datetime] = None      # 계좌 개설일
    interest_rate: float = 0.0      # 연 이자율
    last_interest_date: Optional[datetime] = None  # 마지막 이자 지급일
    
    def __post_init__(self):
        """객체 생성 후 초기화"""
        if self.create_date is None:
            self.create_date = datetime.now()
        if self.last_interest_date is None:
            self.last_interest_date = datetime.now()
    
    def __str__(self) -> str:
        """계좌 정보를 문자열로 반환"""
        return f"Account(id={self.account_id}, name={self.account_name}, balance={self.balance:,.0f}원)"
    
    def to_dict(self) -> dict:
        """계좌 정보를 딕셔너리로 변환 (DB 저장용)"""
        return {
            'account_id': self.account_id,
            'account_name': self.account_name,
            'account_type': self.account_type,
            'account_password': self.account_password,
            'balance': self.balance,
            'user_id': self.user_id,
            'create_date': self.create_date,
            'interest_rate': self.interest_rate,
            'last_interest_date': self.last_interest_date
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Account':
        """딕셔너리에서 Account 객체 생성 (DB 조회용)"""
        return cls(
            account_id=data.get('ACCOUNT_ID', data.get('account_id', '')),
            account_name=data.get('ACCOUNT_NAME', data.get('account_name', '')),
            account_type=data.get('ACCOUNT_TYPE', data.get('account_type', '')),
            account_password=data.get('ACCOUNT_PASSWORD', data.get('account_password', '')),
            balance=data.get('BALANCE', data.get('balance', 0.0)),
            user_id=data.get('USER_ID', data.get('user_id', '')),
            create_date=data.get('CREATE_DATE', data.get('create_date', None)),
            interest_rate=data.get('INTEREST_RATE', data.get('interest_rate', 0.0)),
            last_interest_date=data.get('LAST_INTEREST_DATE', data.get('last_interest_date', None))
        )
    
    @classmethod
    def create_basic_account(cls, account_id: str, account_name: str, 
                           account_type: str, account_password: str, 
                           balance: float, user_id: str) -> 'Account':
        """기본 계좌 생성 (Java의 첫 번째 생성자와 동일)"""
        return cls(
            account_id=account_id,
            account_name=account_name,
            account_type=account_type,
            account_password=account_password,
            balance=balance,
            user_id=user_id
        )
    
    @classmethod
    def create_account_with_interest(cls, account_id: str, account_name: str,
                                   account_type: str, account_password: str,
                                   balance: float, user_id: str, 
                                   interest_rate: float) -> 'Account':
        """이자율 포함 계좌 생성 (Java의 두 번째 생성자와 동일)"""
        return cls(
            account_id=account_id,
            account_name=account_name,
            account_type=account_type,
            account_password=account_password,
            balance=balance,
            user_id=user_id,
            interest_rate=interest_rate
        )
