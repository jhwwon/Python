"""
거래 관리 매니저 클래스
Java의 TransactionManager 클래스를 Python으로 변환
"""

from datetime import datetime
from typing import Optional, List
from ..database import get_database_connection, SQLQueries
from ..entities.transaction import Transaction
from ..helpers.input_helper import InputHelper
from ..utils.bank_utils import BankUtils


class TransactionManager:
    """거래 관련 기능을 관리하는 클래스"""
    
    def __init__(self, account_manager=None):
        """TransactionManager 초기화"""
        self.db = get_database_connection()
        self.input_helper = InputHelper()
        self.account_manager = account_manager
    
    def set_account_manager(self, account_manager):
        """AccountManager 설정"""
        self.account_manager = account_manager
    
    def deposit(self, user_id: str):
        """
        입금 처리
        
        Args:
            user_id: 사용자 ID
        """
        try:
            print("\n[입금]")
            print("=" * 50)
            
            # 계좌번호 입력
            account_id = self.input_helper.input_account_id(
                "입금할 계좌번호: ", own_only=True, login_id=user_id
            )
            
            # 계좌 비밀번호 확인
            account = self.account_manager.get_account_by_id(account_id)
            if not account:
                print("계좌를 찾을 수 없습니다.")
                return
            
            password = self.input_helper.input("계좌 비밀번호: ")
            if password != account.account_password:
                print("계좌 비밀번호가 일치하지 않습니다.")
                return
            
            # 입금액 입력
            amount = self.input_helper.input_amount("입금액: ")
            
            # 입금자명 입력
            depositor_name = self.input_helper.input("입금자명: ")
            
            # 입금 처리
            if self.process_deposit(account_id, amount, depositor_name):
                print(f"✅ {BankUtils.format_currency(amount)}이 입금되었습니다.")
            else:
                print("❌ 입금 처리에 실패했습니다.")
                
        except Exception as e:
            print(f"입금 처리 오류: {e}")
    
    def process_deposit(self, account_id: str, amount: float, depositor_name: str) -> bool:
        """
        입금 처리 (내부 메서드)
        
        Args:
            account_id: 계좌번호
            amount: 입금액
            depositor_name: 입금자명
            
        Returns:
            bool: 입금 성공 여부
        """
        try:
            # 현재 잔액 조회
            account = self.account_manager.get_account_by_id(account_id)
            if not account:
                return False
            
            # 새 잔액 계산
            new_balance = account.balance + amount
            
            # 거래번호 생성
            transaction_id = BankUtils.generate_transaction_id()
            if not transaction_id:
                return False
            
            # 거래 기록 생성
            transaction = Transaction.create_deposit_withdrawal(
                transaction_id=transaction_id,
                account_id=account_id,
                transaction_type="입금",
                amount=amount,
                balance_after=new_balance
            )
            
            # 거래 메모 설정
            transaction.depositor_name = depositor_name
            transaction.transaction_memo = f"입금 - {depositor_name}"
            
            # DB 트랜잭션 시작
            self.db.connection.autocommit = False
            
            try:
                # 거래 기록 저장
                if not self.save_transaction(transaction):
                    raise Exception("거래 기록 저장 실패")
                
                # 계좌 잔액 업데이트
                if not self.account_manager.update_account_balance(account_id, new_balance):
                    raise Exception("계좌 잔액 업데이트 실패")
                
                # 트랜잭션 커밋
                self.db.commit()
                return True
                
            except Exception as e:
                # 트랜잭션 롤백
                self.db.rollback()
                raise e
            finally:
                # 자동 커밋 복원
                self.db.connection.autocommit = True
                
        except Exception as e:
            print(f"입금 처리 오류: {e}")
            return False
    
    def withdraw(self, user_id: str):
        """
        출금 처리
        
        Args:
            user_id: 사용자 ID
        """
        try:
            print("\n[출금]")
            print("=" * 50)
            
            # 계좌번호 입력
            account_id = self.input_helper.input_account_id(
                "출금할 계좌번호: ", own_only=True, login_id=user_id
            )
            
            # 계좌 비밀번호 확인
            account = self.account_manager.get_account_by_id(account_id)
            if not account:
                print("계좌를 찾을 수 없습니다.")
                return
            
            password = self.input_helper.input("계좌 비밀번호: ")
            if password != account.account_password:
                print("계좌 비밀번호가 일치하지 않습니다.")
                return
            
            # 출금액 입력
            amount = self.input_helper.input_amount("출금액: ")
            
            # 잔액 확인
            if amount > account.balance:
                print("잔액이 부족합니다.")
                return
            
            # 출금 처리
            if self.process_withdraw(account_id, amount):
                print(f"✅ {BankUtils.format_currency(amount)}이 출금되었습니다.")
            else:
                print("❌ 출금 처리에 실패했습니다.")
                
        except Exception as e:
            print(f"출금 처리 오류: {e}")
    
    def process_withdraw(self, account_id: str, amount: float) -> bool:
        """
        출금 처리 (내부 메서드)
        
        Args:
            account_id: 계좌번호
            amount: 출금액
            
        Returns:
            bool: 출금 성공 여부
        """
        try:
            # 현재 잔액 조회
            account = self.account_manager.get_account_by_id(account_id)
            if not account:
                return False
            
            # 새 잔액 계산
            new_balance = account.balance - amount
            
            # 거래번호 생성
            transaction_id = BankUtils.generate_transaction_id()
            if not transaction_id:
                return False
            
            # 거래 기록 생성
            transaction = Transaction.create_deposit_withdrawal(
                transaction_id=transaction_id,
                account_id=account_id,
                transaction_type="출금",
                amount=amount,
                balance_after=new_balance
            )
            
            # 거래 메모 설정
            transaction.transaction_memo = "출금"
            
            # DB 트랜잭션 시작
            self.db.connection.autocommit = False
            
            try:
                # 거래 기록 저장
                if not self.save_transaction(transaction):
                    raise Exception("거래 기록 저장 실패")
                
                # 계좌 잔액 업데이트
                if not self.account_manager.update_account_balance(account_id, new_balance):
                    raise Exception("계좌 잔액 업데이트 실패")
                
                # 트랜잭션 커밋
                self.db.commit()
                return True
                
            except Exception as e:
                # 트랜잭션 롤백
                self.db.rollback()
                raise e
            finally:
                # 자동 커밋 복원
                self.db.connection.autocommit = True
                
        except Exception as e:
            print(f"출금 처리 오류: {e}")
            return False
    
    def transfer(self, user_id: str):
        """
        이체 처리
        
        Args:
            user_id: 사용자 ID
        """
        try:
            print("\n[이체]")
            print("=" * 50)
            
            # 보내는 계좌 입력
            from_account_id = self.input_helper.input_account_id(
                "보내는 계좌번호: ", own_only=True, login_id=user_id
            )
            
            # 계좌 비밀번호 확인
            from_account = self.account_manager.get_account_by_id(from_account_id)
            if not from_account:
                print("계좌를 찾을 수 없습니다.")
                return
            
            password = self.input_helper.input("계좌 비밀번호: ")
            if password != from_account.account_password:
                print("계좌 비밀번호가 일치하지 않습니다.")
                return
            
            # 받는 계좌 입력
            to_account_id = self.input_helper.input("받는 계좌번호: ")
            if not self.account_manager.account_exists(to_account_id):
                print("받는 계좌가 존재하지 않습니다.")
                return
            
            if from_account_id == to_account_id:
                print("보내는 계좌와 받는 계좌가 같을 수 없습니다.")
                return
            
            # 이체액 입력
            amount = self.input_helper.input_amount("이체액: ")
            
            # 잔액 확인
            if amount > from_account.balance:
                print("잔액이 부족합니다.")
                return
            
            # 받는 계좌 정보 조회
            to_account = self.account_manager.get_account_by_id(to_account_id)
            if not to_account:
                print("받는 계좌 정보를 찾을 수 없습니다.")
                return
            
            # 이체 확인
            print(f"\n이체 정보:")
            print(f"보내는 계좌: {from_account_id} ({from_account.account_name})")
            print(f"받는 계좌: {to_account_id} ({to_account.account_name})")
            print(f"이체액: {BankUtils.format_currency(amount)}")
            
            if not self.input_helper.confirm_action():
                print("이체가 취소되었습니다.")
                return
            
            # 이체 처리
            if self.process_transfer(from_account_id, to_account_id, amount):
                print(f"✅ {BankUtils.format_currency(amount)}이 이체되었습니다.")
            else:
                print("❌ 이체 처리에 실패했습니다.")
                
        except Exception as e:
            print(f"이체 처리 오류: {e}")
    
    def process_transfer(self, from_account_id: str, to_account_id: str, amount: float) -> bool:
        """
        이체 처리 (내부 메서드)
        
        Args:
            from_account_id: 보내는 계좌번호
            to_account_id: 받는 계좌번호
            amount: 이체액
            
        Returns:
            bool: 이체 성공 여부
        """
        try:
            # 계좌 정보 조회
            from_account = self.account_manager.get_account_by_id(from_account_id)
            to_account = self.account_manager.get_account_by_id(to_account_id)
            
            if not from_account or not to_account:
                return False
            
            # 새 잔액 계산
            from_new_balance = from_account.balance - amount
            to_new_balance = to_account.balance + amount
            
            # 거래번호 생성
            from_transaction_id = BankUtils.generate_transaction_id()
            to_transaction_id = BankUtils.generate_transaction_id()
            
            if not from_transaction_id or not to_transaction_id:
                return False
            
            # 거래 기록 생성
            from_transaction = Transaction.create_transfer(
                transaction_id=from_transaction_id,
                account_id=from_account_id,
                transaction_type="이체출금",
                amount=amount,
                balance_after=from_new_balance,
                counterpart_account=to_account_id
            )
            
            to_transaction = Transaction.create_transfer(
                transaction_id=to_transaction_id,
                account_id=to_account_id,
                transaction_type="이체입금",
                amount=amount,
                balance_after=to_new_balance,
                counterpart_account=from_account_id
            )
            
            # 거래 메모 설정
            from_transaction.counterpart_name = to_account.account_name
            from_transaction.transaction_memo = f"이체출금 - {to_account.account_name}"
            
            to_transaction.counterpart_name = from_account.account_name
            to_transaction.transaction_memo = f"이체입금 - {from_account.account_name}"
            
            # DB 트랜잭션 시작
            self.db.connection.autocommit = False
            
            try:
                # 거래 기록 저장
                if not self.save_transaction(from_transaction):
                    raise Exception("보내는 계좌 거래 기록 저장 실패")
                
                if not self.save_transaction(to_transaction):
                    raise Exception("받는 계좌 거래 기록 저장 실패")
                
                # 계좌 잔액 업데이트
                if not self.account_manager.update_account_balance(from_account_id, from_new_balance):
                    raise Exception("보내는 계좌 잔액 업데이트 실패")
                
                if not self.account_manager.update_account_balance(to_account_id, to_new_balance):
                    raise Exception("받는 계좌 잔액 업데이트 실패")
                
                # 트랜잭션 커밋
                self.db.commit()
                return True
                
            except Exception as e:
                # 트랜잭션 롤백
                self.db.rollback()
                raise e
            finally:
                # 자동 커밋 복원
                self.db.connection.autocommit = True
                
        except Exception as e:
            print(f"이체 처리 오류: {e}")
            return False
    
    def history(self, user_id: str):
        """
        거래내역 조회
        
        Args:
            user_id: 사용자 ID
        """
        try:
            print("\n[거래내역 조회]")
            print("=" * 50)
            
            # 조회할 계좌 선택
            account_id = self.input_helper.input_account_id(
                "조회할 계좌번호 (전체 조회는 엔터): ", own_only=True, login_id=user_id
            )
            
            if account_id:
                # 특정 계좌 거래내역 조회
                self.show_account_transactions(account_id)
            else:
                # 전체 거래내역 조회
                self.show_user_transactions(user_id)
                
        except Exception as e:
            print(f"거래내역 조회 오류: {e}")
    
    def show_account_transactions(self, account_id: str):
        """
        특정 계좌의 거래내역 조회
        
        Args:
            account_id: 계좌번호
        """
        try:
            results = self.db.execute_query(
                SQLQueries.SELECT_TRANSACTIONS_BY_ACCOUNT,
                {'account_id': account_id}
            )
            
            if not results:
                print("거래내역이 없습니다.")
                return
            
            print(f"\n계좌번호: {account_id}")
            print("=" * 100)
            print(f"{'거래일시':<20} {'거래유형':<10} {'거래금액':<15} {'거래후잔액':<15} {'상대방정보':<20} {'메모':<20}")
            print("-" * 100)
            
            for data in results:
                transaction = Transaction.from_dict(data)
                counterpart_info = BankUtils.get_counterpart_display(
                    transaction.transaction_type,
                    transaction.counterpart_name,
                    transaction.depositor_name,
                    transaction.counterpart_account
                )
                
                print(f"{transaction.transaction_date.strftime('%Y-%m-%d %H:%M:%S'):<20} "
                      f"{transaction.transaction_type:<10} "
                      f"{BankUtils.format_currency(transaction.amount):<15} "
                      f"{BankUtils.format_currency(transaction.balance_after):<15} "
                      f"{counterpart_info:<20} "
                      f"{transaction.transaction_memo or '-':<20}")
            
            print("=" * 100)
            
        except Exception as e:
            print(f"계좌 거래내역 조회 오류: {e}")
    
    def show_user_transactions(self, user_id: str):
        """
        사용자의 전체 거래내역 조회
        
        Args:
            user_id: 사용자 ID
        """
        try:
            results = self.db.execute_query(
                SQLQueries.SELECT_TRANSACTIONS_BY_USER,
                {'user_id': user_id}
            )
            
            if not results:
                print("거래내역이 없습니다.")
                return
            
            print(f"\n전체 거래내역")
            print("=" * 120)
            print(f"{'거래일시':<20} {'계좌번호':<15} {'계좌명':<15} {'거래유형':<10} {'거래금액':<15} {'거래후잔액':<15} {'상대방정보':<20} {'메모':<20}")
            print("-" * 120)
            
            for data in results:
                transaction = Transaction.from_dict(data)
                counterpart_info = BankUtils.get_counterpart_display(
                    transaction.transaction_type,
                    transaction.counterpart_name,
                    transaction.depositor_name,
                    transaction.counterpart_account
                )
                
                print(f"{transaction.transaction_date.strftime('%Y-%m-%d %H:%M:%S'):<20} "
                      f"{transaction.account_id:<15} "
                      f"{data.get('account_name', '-'):<15} "
                      f"{transaction.transaction_type:<10} "
                      f"{BankUtils.format_currency(transaction.amount):<15} "
                      f"{BankUtils.format_currency(transaction.balance_after):<15} "
                      f"{counterpart_info:<20} "
                      f"{transaction.transaction_memo or '-':<20}")
            
            print("=" * 120)
            
        except Exception as e:
            print(f"사용자 거래내역 조회 오류: {e}")
    
    def save_transaction(self, transaction: Transaction) -> bool:
        """
        거래 기록을 DB에 저장
        
        Args:
            transaction: 저장할 거래 객체
            
        Returns:
            bool: 저장 성공 여부
        """
        try:
            result = self.db.execute_update(
                SQLQueries.INSERT_TRANSACTION,
                transaction.to_dict()
            )
            return result > 0
            
        except Exception as e:
            print(f"거래 기록 저장 오류: {e}")
            return False
    
    def record_deposit(self, account_id: str, amount: float, memo: str, user_id: str) -> bool:
        """
        입금 거래 기록 (내부용)
        
        Args:
            account_id: 계좌번호
            amount: 입금액
            memo: 거래 메모
            user_id: 사용자 ID
            
        Returns:
            bool: 기록 성공 여부
        """
        try:
            # 현재 잔액 조회
            account = self.account_manager.get_account_by_id(account_id)
            if not account:
                return False
            
            # 거래번호 생성
            transaction_id = BankUtils.generate_transaction_id()
            if not transaction_id:
                return False
            
            # 거래 기록 생성
            transaction = Transaction.create_deposit_withdrawal(
                transaction_id=transaction_id,
                account_id=account_id,
                transaction_type="입금",
                amount=amount,
                balance_after=account.balance
            )
            
            transaction.transaction_memo = memo
            
            return self.save_transaction(transaction)
            
        except Exception as e:
            print(f"입금 거래 기록 오류: {e}")
            return False
