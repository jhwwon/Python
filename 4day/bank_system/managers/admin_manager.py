"""
관리자 관리 매니저 클래스
Java의 AdminManager 클래스를 Python으로 변환 (간단 버전)
"""

from datetime import datetime
from typing import Optional, List
from ..database import get_database_connection, SQLQueries
from ..entities.account import Account
from ..entities.interest import InterestPayment
from ..helpers.input_helper import InputHelper
from ..helpers.validation_helper import ValidationHelper
from ..utils.bank_utils import BankUtils
from ..utils.interest_calculator import InterestCalculator


class AdminManager:
    """관리자 관련 기능을 관리하는 클래스"""
    
    def __init__(self):
        """AdminManager 초기화"""
        self.db = get_database_connection()
        self.validator = ValidationHelper()
        self.input_helper = InputHelper()
    
    def admin_login(self) -> Optional[str]:
        """
        관리자 로그인
        
        Returns:
            Optional[str]: 로그인 성공 시 admin_id, 실패 시 None
        """
        try:
            print("\n[관리자 로그인]")
            print("=" * 50)
            
            admin_id = self.input_helper.input("관리자 ID: ")
            password = self.input_helper.input("비밀번호: ")
            
            # 간단한 관리자 인증 (실제로는 DB에서 관리자 테이블 조회)
            if admin_id == "admin" and password == "admin123":
                print("✅ 관리자 로그인 성공!")
                return admin_id
            else:
                print("❌ 관리자 인증에 실패했습니다.")
                return None
                
        except Exception as e:
            print(f"관리자 로그인 오류: {e}")
            return None
    
    def get_admin_name(self, admin_id: str) -> str:
        """
        관리자 이름 조회
        
        Args:
            admin_id: 관리자 ID
            
        Returns:
            str: 관리자 이름
        """
        return "시스템관리자"  # 간단한 구현
    
    def view_all_accounts(self):
        """전체 계좌 조회"""
        try:
            print("\n[전체 계좌 조회]")
            print("=" * 120)
            
            results = self.db.execute_query(SQLQueries.SELECT_ALL_ACCOUNTS)
            
            if not results:
                print("등록된 계좌가 없습니다.")
                return
            
            print(f"{'계좌번호':<15} {'계좌명':<15} {'계좌종류':<10} {'잔액':<15} {'이자율':<10} {'소유자':<15} {'개설일':<12}")
            print("-" * 120)
            
            for data in results:
                account = Account.from_dict(data)
                print(f"{account.account_id:<15} {account.account_name:<15} "
                      f"{account.account_type:<10} {BankUtils.format_currency(account.balance):<15} "
                      f"{InterestCalculator.format_interest_rate(account.interest_rate):<10} "
                      f"{data.get('user_name', '-'):<15} "
                      f"{account.create_date.strftime('%Y-%m-%d'):<12}")
            
            print("=" * 120)
            
        except Exception as e:
            print(f"전체 계좌 조회 오류: {e}")
    
    def view_user_accounts(self):
        """사용자별 계좌 조회"""
        try:
            print("\n[사용자별 계좌 조회]")
            print("=" * 50)
            
            user_id = self.input_helper.input("조회할 사용자 ID: ")
            
            results = self.db.execute_query(
                SQLQueries.SELECT_ACCOUNTS_BY_USER,
                {'user_id': user_id}
            )
            
            if not results:
                print("해당 사용자의 계좌가 없습니다.")
                return
            
            print(f"\n{user_id}님의 계좌 목록")
            print("=" * 80)
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
            print(f"사용자별 계좌 조회 오류: {e}")
    
    def view_interest_history(self):
        """이자 지급 내역 조회"""
        try:
            print("\n[이자 지급 내역 조회]")
            print("=" * 100)
            
            results = self.db.execute_query(SQLQueries.SELECT_INTEREST_PAYMENTS)
            
            if not results:
                print("이자 지급 내역이 없습니다.")
                return
            
            print(f"{'지급ID':<12} {'계좌번호':<15} {'지급일':<20} {'지급금액':<15} {'관리자':<15}")
            print("-" * 100)
            
            for data in results:
                payment = InterestPayment.from_dict(data)
                print(f"{payment.payment_id:<12} {payment.account_id:<15} "
                      f"{payment.payment_date.strftime('%Y-%m-%d %H:%M:%S'):<20} "
                      f"{BankUtils.format_currency(payment.interest_amount):<15} "
                      f"{payment.admin_id:<15}")
            
            print("=" * 100)
            
        except Exception as e:
            print(f"이자 지급 내역 조회 오류: {e}")
    
    def execute_interest_payment(self, admin_id: str) -> bool:
        """
        이자 지급 실행
        
        Args:
            admin_id: 관리자 ID
            
        Returns:
            bool: 이자 지급 성공 여부
        """
        try:
            print("\n[이자 지급 실행]")
            print("=" * 50)
            
            # 이자 지급 대상 계좌 조회
            eligible_accounts = InterestCalculator.get_all_interest_eligible_accounts()
            
            if not eligible_accounts:
                print("이자 지급 대상 계좌가 없습니다.")
                return False
            
            # 이자 지급 요약 정보
            summary = InterestCalculator.get_interest_summary(eligible_accounts)
            print(f"이자 지급 대상: {summary['total_accounts']}개 계좌")
            print(f"총 지급 금액: {BankUtils.format_currency(summary['total_amount'])}")
            
            # 계좌 종류별 집계
            for account_type, info in summary['by_type'].items():
                print(f"  {account_type}: {info['count']}개 계좌, {BankUtils.format_currency(info['amount'])}")
            
            print("\n이자 지급을 실행하시겠습니까?")
            if not self.input_helper.confirm_action():
                print("이자 지급이 취소되었습니다.")
                return False
            
            # 이자 지급 처리
            success_count = 0
            total_amount = 0
            
            for interest_info in eligible_accounts:
                if self.process_interest_payment(interest_info, admin_id):
                    success_count += 1
                    total_amount += interest_info.interest_amount
            
            print(f"\n✅ 이자 지급 완료!")
            print(f"성공: {success_count}개 계좌")
            print(f"총 지급 금액: {BankUtils.format_currency(total_amount)}")
            
            return success_count > 0
            
        except Exception as e:
            print(f"이자 지급 실행 오류: {e}")
            return False
    
    def process_interest_payment(self, interest_info, admin_id: str) -> bool:
        """
        개별 계좌 이자 지급 처리
        
        Args:
            interest_info: 이자 정보 객체
            admin_id: 관리자 ID
            
        Returns:
            bool: 이자 지급 성공 여부
        """
        try:
            # 이자 지급 ID 생성
            payment_id = BankUtils.generate_payment_id()
            
            # 이자 지급 기록 생성
            payment = InterestPayment.create_payment(
                payment_id=payment_id,
                account_id=interest_info.account_id,
                interest_amount=interest_info.interest_amount,
                admin_id=admin_id
            )
            
            # 새 잔액 계산
            new_balance = interest_info.principal + interest_info.interest_amount
            
            # DB 트랜잭션 시작
            self.db.connection.autocommit = False
            
            try:
                # 이자 지급 기록 저장
                result = self.db.execute_update(
                    SQLQueries.INSERT_INTEREST_PAYMENT,
                    payment.to_dict()
                )
                
                if result <= 0:
                    raise Exception("이자 지급 기록 저장 실패")
                
                # 계좌 잔액 업데이트
                result = self.db.execute_update(
                    SQLQueries.UPDATE_ACCOUNT_BALANCE,
                    {
                        'account_id': interest_info.account_id,
                        'balance': new_balance,
                        'last_interest_date': interest_info.current_date
                    }
                )
                
                if result <= 0:
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
            print(f"계좌 {interest_info.account_id} 이자 지급 오류: {e}")
            return False
