"""
거래 엔티티 클래스
Java의 Transaction 클래스를 Python으로 변환
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Transaction:
    """거래 내역을 담는 클래스"""
    
    transaction_id: str             # 거래번호
    account_id: str                 # 거래 계좌번호
    transaction_type: str           # 거래 유형 (입금/출금/이체입금/이체출금)
    amount: float                   # 거래 금액
    balance_after: float            # 거래 후 잔액
    counterpart_account: Optional[str] = None    # 상대방 계좌번호
    counterpart_name: Optional[str] = None       # 상대방 이름
    depositor_name: Optional[str] = None         # 입금자명
    transaction_memo: Optional[str] = None       # 거래 메모
    transaction_date: Optional[datetime] = None  # 거래 발생 시각
    
    def __post_init__(self):
        """객체 생성 후 초기화"""
        if self.transaction_date is None:
            self.transaction_date = datetime.now()
    
    def __str__(self) -> str:
        """거래 정보를 문자열로 반환"""
        return f"Transaction(id={self.transaction_id}, type={self.transaction_type}, amount={self.amount:,.0f}원)"
    
    def to_dict(self) -> dict:
        """거래 정보를 딕셔너리로 변환 (DB 저장용)"""
        return {
            'transaction_id': self.transaction_id,
            'account_id': self.account_id,
            'transaction_type': self.transaction_type,
            'amount': self.amount,
            'balance_after': self.balance_after,
            'counterpart_account': self.counterpart_account,
            'counterpart_name': self.counterpart_name,
            'depositor_name': self.depositor_name,
            'transaction_memo': self.transaction_memo,
            'transaction_date': self.transaction_date
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Transaction':
        """딕셔너리에서 Transaction 객체 생성 (DB 조회용)"""
        return cls(
            transaction_id=data.get('TRANSACTION_ID', data.get('transaction_id', '')),
            account_id=data.get('ACCOUNT_ID', data.get('account_id', '')),
            transaction_type=data.get('TRANSACTION_TYPE', data.get('transaction_type', '')),
            amount=data.get('AMOUNT', data.get('amount', 0.0)),
            balance_after=data.get('BALANCE_AFTER', data.get('balance_after', 0.0)),
            counterpart_account=data.get('COUNTERPART_ACCOUNT', data.get('counterpart_account')),
            counterpart_name=data.get('COUNTERPART_NAME', data.get('counterpart_name')),
            depositor_name=data.get('DEPOSITOR_NAME', data.get('depositor_name')),
            transaction_memo=data.get('TRANSACTION_MEMO', data.get('transaction_memo')),
            transaction_date=data.get('TRANSACTION_DATE', data.get('transaction_date', None))
        )
    
    @classmethod
    def create_deposit_withdrawal(cls, transaction_id: str, account_id: str,
                                transaction_type: str, amount: float, 
                                balance_after: float) -> 'Transaction':
        """입금/출금용 거래 생성 (Java의 첫 번째 생성자와 동일)"""
        return cls(
            transaction_id=transaction_id,
            account_id=account_id,
            transaction_type=transaction_type,
            amount=amount,
            balance_after=balance_after
        )
    
    @classmethod
    def create_transfer(cls, transaction_id: str, account_id: str,
                       transaction_type: str, amount: float, 
                       balance_after: float, counterpart_account: str) -> 'Transaction':
        """이체용 거래 생성 (Java의 두 번째 생성자와 동일)"""
        return cls(
            transaction_id=transaction_id,
            account_id=account_id,
            transaction_type=transaction_type,
            amount=amount,
            balance_after=balance_after,
            counterpart_account=counterpart_account
        )
    
    @classmethod
    def create_full_transaction(cls, transaction_id: str, account_id: str,
                              transaction_type: str, amount: float, 
                              balance_after: float, counterpart_account: str,
                              counterpart_name: str, depositor_name: str, 
                              transaction_memo: str) -> 'Transaction':
        """전체 정보 포함 거래 생성 (Java의 세 번째 생성자와 동일)"""
        return cls(
            transaction_id=transaction_id,
            account_id=account_id,
            transaction_type=transaction_type,
            amount=amount,
            balance_after=balance_after,
            counterpart_account=counterpart_account,
            counterpart_name=counterpart_name,
            depositor_name=depositor_name,
            transaction_memo=transaction_memo
        )
