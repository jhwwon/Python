"""
계좌 관리 매니저 클래스
Java의 AccountManager 클래스를 Python으로 변환
"""

from datetime import datetime
from typing import Optional, List
from ..database import get_database_connection, SQLQueries
from ..entities.account import Account
from ..entities.transaction import Transaction
from ..helpers.input_helper import InputHelper
from ..helpers.validation_helper import ValidationHelper
from ..utils.bank_utils import BankUtils
from ..utils.interest_calculator import InterestCalculator


class AccountManager:
    """계좌 관련 기능을 관리하는 클래스"""
    
    def __init__(self, user_manager=None, transaction_manager=None):
        """AccountManager 초기화"""
        self.db = get_database_connection()
        self.validator = ValidationHelper()
        self.input_helper = InputHelper()
        self.user_manager = user_manager
        self.transaction_manager = transaction_manager
        
        # InputHelper에 AccountManager 설정
        self.input_helper.set_account_manager(self)
    
    def set_transaction_manager(self, transaction_manager):
        """TransactionManager 설정"""
        self.transaction_manager = transaction_manager
    
    def account_exists(self, account_id: str) -> bool:
        """
        계좌 존재 여부 확인
        
        Args:
            account_id: 확인할 계좌번호
            
        Returns:
            bool: 계좌 존재 여부
        """
        try:
            results = self.db.execute_query(
                "SELECT COUNT(*) as count FROM accounts WHERE account_id = :account_id",
                {'account_id': account_id}
            )
            
            if results and len(results) > 0:
                count = results[0].get('COUNT', results[0].get('count', 0))
                return count > 0
            return False
            
        except Exception as e:
            print(f"계좌 존재 확인 오류: {e}")
            return False
    
    def is_my_account(self, account_id: str, user_id: str) -> bool:
        """
        본인 계좌 여부 확인
        
        Args:
            account_id: 확인할 계좌번호
            user_id: 사용자 ID
            
        Returns:
            bool: 본인 계좌 여부
        """
        try:
            results = self.db.execute_query(
                "SELECT COUNT(*) as count FROM accounts WHERE account_id = :account_id AND user_id = :user_id",
                {'account_id': account_id, 'user_id': user_id}
            )
            
            if results and len(results) > 0:
                count = results[0].get('COUNT', results[0].get('count', 0))
                return count > 0
            return False
            
        except Exception as e:
            print(f"계좌 소유권 확인 오류: {e}")
            return False
    
    def create_account(self, user_id: str) -> bool:
        """
        계좌 생성
        
        Args:
            user_id: 계좌 소유자 ID
            
        Returns:
            bool: 계좌 생성 성공 여부
        """
        try:
            print("\n[계좌 생성]")
            print("=" * 50)
            
            # 계좌 정보 입력
            account_name = self.input_helper.input("계좌명: ")
            account_type = self.input_helper.input_menu_choice(
                "계좌 종류 (1.보통예금 2.정기예금 3.적금): ",
                ['1', '2', '3']
            )
            
            # 계좌 종류 매핑
            type_map = {'1': '보통예금', '2': '정기예금', '3': '적금'}
            account_type = type_map[account_type]
            
            account_password = self.input_helper.input_account_password()
            initial_balance = self.input_helper.input_amount("초기 입금액: ")
            
            # 계좌번호 생성
            account_id = BankUtils.generate_account_number()
            if not account_id:
                print("계좌번호 생성에 실패했습니다.")
                return False
            
            # 이자율 설정
            interest_rate = InterestCalculator.get_interest_rate_by_type(account_type)
            
            # 계좌 객체 생성
            account = Account.create_account_with_interest(
                account_id=account_id,
                account_name=account_name,
                account_type=account_type,
                account_password=account_password,
                balance=initial_balance,
                user_id=user_id,
                interest_rate=interest_rate
            )
            
            # DB에 저장
            if self.save_account(account):
                print(f"✅ 계좌가 생성되었습니다!")
                print(f"계좌번호: {account_id}")
                print(f"계좌명: {account_name}")
                print(f"계좌종류: {account_type}")
                print(f"이자율: {InterestCalculator.format_interest_rate(interest_rate)}")
                print(f"초기잔액: {BankUtils.format_currency(initial_balance)}")
                
                # 초기 입금 거래 기록
                if initial_balance > 0 and self.transaction_manager:
                    self.transaction_manager.record_deposit(
                        account_id, initial_balance, "계좌 개설", user_id
                    )
                
                return True
            else:
                print("❌ 계좌 생성에 실패했습니다.")
                return False
                
        except Exception as e:
            print(f"계좌 생성 오류: {e}")
            return False
    
    def save_account(self, account: Account) -> bool:
        """
        계좌 정보를 DB에 저장
        
        Args:
            account: 저장할 계좌 객체
            
        Returns:
            bool: 저장 성공 여부
        """
        try:
            result = self.db.execute_update(
                SQLQueries.INSERT_ACCOUNT,
                account.to_dict()
            )
            return result > 0
            
        except Exception as e:
            print(f"계좌 저장 오류: {e}")
            return False
    
    def list_accounts(self, user_id: str):
        """
        사용자의 계좌 목록 조회
        
        Args:
            user_id: 사용자 ID
        """
        try:
            print(f"\n[{self.user_manager.get_user_name(user_id)}님의 계좌 목록]")
            print("=" * 80)
            
            results = self.db.execute_query(
                SQLQueries.SELECT_ACCOUNTS_BY_USER,
                {'user_id': user_id}
            )
            
            if not results:
                print("등록된 계좌가 없습니다.")
                return
            
            print(f"{'계좌번호':<15} {'계좌명':<15} {'계좌종류':<10} {'잔액':<15} {'이자율':<10} {'개설일':<12}")
            print("-" * 80)
            
            for data in results:
                account = Account.from_dict(data)
                print(f"{account.account_id:<15} {account.account_name:<15} "
                      f"{account.account_type:<10} {BankUtils.format_currency(account.balance):<15} "
                      f"{InterestCalculator.format_interest_rate(account.interest_rate):<10} "
                      f"{account.create_date.strftime('%Y-%m-%d'):<12}")
            
            print("=" * 80)
            
        except Exception as e:
            print(f"계좌 목록 조회 오류: {e}")
    
    def read_account(self, user_id: str):
        """
        계좌 상세 조회
        
        Args:
            user_id: 사용자 ID
        """
        try:
            print("\n[계좌 상세 조회]")
            print("=" * 50)
            
            account_id = self.input_helper.input_account_id(
                "조회할 계좌번호: ", own_only=True, login_id=user_id
            )
            
            account = self.get_account_by_id(account_id)
            if not account:
                print("계좌를 찾을 수 없습니다.")
                return
            
            print(f"\n계좌번호: {account.account_id}")
            print(f"계좌명: {account.account_name}")
            print(f"계좌종류: {account.account_type}")
            print(f"잔액: {BankUtils.format_currency(account.balance)}")
            print(f"이자율: {InterestCalculator.format_interest_rate(account.interest_rate)}")
            print(f"개설일: {account.create_date.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"마지막 이자지급일: {account.last_interest_date.strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            print(f"계좌 조회 오류: {e}")
    
    def get_account_by_id(self, account_id: str) -> Optional[Account]:
        """
        계좌번호로 계좌 정보 조회
        
        Args:
            account_id: 계좌번호
            
        Returns:
            Optional[Account]: 계좌 객체 또는 None
        """
        try:
            results = self.db.execute_query(
                SQLQueries.SELECT_ACCOUNT_BY_ID,
                {'account_id': account_id}
            )
            
            if results:
                return Account.from_dict(results[0])
            
            return None
            
        except Exception as e:
            print(f"계좌 조회 오류: {e}")
            return None
    
    def delete_account_menu(self, user_id: str, account_id: Optional[str] = None):
        """
        계좌 해지 메뉴
        
        Args:
            user_id: 사용자 ID
            account_id: 해지할 계좌번호 (None이면 입력받음)
        """
        try:
            print("\n[계좌 해지]")
            print("=" * 50)
            
            if not account_id:
                account_id = self.input_helper.input_account_id(
                    "해지할 계좌번호: ", own_only=True, login_id=user_id
                )
            
            account = self.get_account_by_id(account_id)
            if not account:
                print("계좌를 찾을 수 없습니다.")
                return
            
            # 계좌 비밀번호 확인
            password = self.input_helper.input("계좌 비밀번호: ")
            if password != account.account_password:
                print("계좌 비밀번호가 일치하지 않습니다.")
                return
            
            # 잔액 확인
            if account.balance > 0:
                print(f"잔액이 {BankUtils.format_currency(account.balance)} 있습니다.")
                if not self.input_helper.confirm_action():
                    print("계좌 해지가 취소되었습니다.")
                    return
            
            # 계좌 해지 확인
            print(f"정말로 {account.account_name} 계좌를 해지하시겠습니까?")
            if not self.input_helper.confirm_action():
                print("계좌 해지가 취소되었습니다.")
                return
            
            # 계좌 해지 처리
            if self.delete_account(account_id):
                print("✅ 계좌가 해지되었습니다.")
            else:
                print("❌ 계좌 해지에 실패했습니다.")
                
        except Exception as e:
            print(f"계좌 해지 오류: {e}")
    
    def delete_account(self, account_id: str) -> bool:
        """
        계좌 삭제
        
        Args:
            account_id: 삭제할 계좌번호
            
        Returns:
            bool: 삭제 성공 여부
        """
        try:
            result = self.db.execute_update(
                SQLQueries.DELETE_ACCOUNT,
                {'account_id': account_id}
            )
            return result > 0
            
        except Exception as e:
            print(f"계좌 삭제 오류: {e}")
            return False
    
    def change_password(self, user_id: str):
        """
        계좌 비밀번호 변경
        
        Args:
            user_id: 사용자 ID
        """
        try:
            print("\n[계좌 비밀번호 변경]")
            print("=" * 50)
            
            account_id = self.input_helper.input_account_id(
                "비밀번호를 변경할 계좌번호: ", own_only=True, login_id=user_id
            )
            
            account = self.get_account_by_id(account_id)
            if not account:
                print("계좌를 찾을 수 없습니다.")
                return
            
            # 현재 비밀번호 확인
            current_password = self.input_helper.input("현재 계좌 비밀번호: ")
            if current_password != account.account_password:
                print("현재 비밀번호가 일치하지 않습니다.")
                return
            
            # 새 비밀번호 입력
            new_password = self.input_helper.input_account_password()
            
            # 비밀번호 변경 확인
            print("계좌 비밀번호를 변경하시겠습니까?")
            if not self.input_helper.confirm_action():
                print("비밀번호 변경이 취소되었습니다.")
                return
            
            # 비밀번호 업데이트
            if self.update_account_password(account_id, new_password):
                print("✅ 계좌 비밀번호가 변경되었습니다.")
            else:
                print("❌ 계좌 비밀번호 변경에 실패했습니다.")
                
        except Exception as e:
            print(f"계좌 비밀번호 변경 오류: {e}")
    
    def update_account_password(self, account_id: str, new_password: str) -> bool:
        """
        계좌 비밀번호 업데이트
        
        Args:
            account_id: 계좌번호
            new_password: 새 비밀번호
            
        Returns:
            bool: 업데이트 성공 여부
        """
        try:
            result = self.db.execute_update(
                SQLQueries.UPDATE_ACCOUNT_PASSWORD,
                {'account_id': account_id, 'account_password': new_password}
            )
            return result > 0
            
        except Exception as e:
            print(f"계좌 비밀번호 업데이트 오류: {e}")
            return False
    
    def update_account_balance(self, account_id: str, new_balance: float, 
                             last_interest_date: Optional[datetime] = None) -> bool:
        """
        계좌 잔액 업데이트
        
        Args:
            account_id: 계좌번호
            new_balance: 새 잔액
            last_interest_date: 마지막 이자 지급일
            
        Returns:
            bool: 업데이트 성공 여부
        """
        try:
            update_data = {
                'account_id': account_id,
                'balance': new_balance,
                'last_interest_date': last_interest_date or datetime.now()
            }
            
            result = self.db.execute_update(
                SQLQueries.UPDATE_ACCOUNT_BALANCE,
                update_data
            )
            return result > 0
            
        except Exception as e:
            print(f"계좌 잔액 업데이트 오류: {e}")
            return False
