"""
은행 시스템 메인 클래스
Java의 BankSystem 클래스를 Python으로 변환
"""

import sys
import signal
from typing import Optional
from .database import get_database_connection, close_database_connection
from .managers.user_manager import UserManager
from .managers.account_manager import AccountManager
from .managers.transaction_manager import TransactionManager
from .managers.admin_manager import AdminManager
from .managers.scheduler_manager import SchedulerManager


class BankSystem:
    """은행 시스템의 메인 클래스"""
    
    def __init__(self):
        """BankSystem 초기화"""
        self.login_id: Optional[str] = None
        self.admin_login_id: Optional[str] = None
        
        # 데이터베이스 연결
        try:
            self.db = get_database_connection()
            print("은행 계좌 시스템 DB 연결 성공!\n")
        except Exception as e:
            print(f"데이터베이스 연결 실패: {e}")
            self.exit()
            return
        
        # 매니저 객체들 초기화
        try:
            self.user_manager = UserManager()
            self.transaction_manager = TransactionManager()
            self.account_manager = AccountManager(
                user_manager=self.user_manager,
                transaction_manager=self.transaction_manager
            )
            self.transaction_manager.set_account_manager(self.account_manager)
            self.admin_manager = AdminManager()
            
            # 스케줄러 초기화 및 시작
            self.scheduler_manager = SchedulerManager(self.admin_manager)
            self.scheduler_manager.start()
            
            # 시스템 종료 시 정리 작업
            self._setup_shutdown_handler()
            
        except Exception as e:
            print(f"시스템 초기화 오류: {e}")
            self.exit()
    
    def _setup_shutdown_handler(self):
        """시스템 종료 시 정리 작업 설정"""
        def signal_handler(signum, frame):
            print("\n시스템이 종료됩니다...")
            if self.scheduler_manager:
                self.scheduler_manager.stop()
            print("안전하게 종료되었습니다.")
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def run(self):
        """시스템 실행"""
        try:
            self.list()
        except KeyboardInterrupt:
            print("\n시스템이 종료됩니다...")
            self.exit()
        except Exception as e:
            print(f"시스템 실행 오류: {e}")
            self.exit()
    
    def exit(self):
        """시스템 종료"""
        try:
            # 스케줄러 정리
            if hasattr(self, 'scheduler_manager') and self.scheduler_manager:
                self.scheduler_manager.stop()
            
            # 데이터베이스 연결 종료
            close_database_connection()
            
        except Exception as e:
            print(f"시스템 종료 중 오류: {e}")
        
        print("은행 시스템이 정상적으로 종료되었습니다.")
        sys.exit(0)
    
    def logout(self):
        """로그아웃"""
        self.login_id = None
        self.admin_login_id = None
        print("로그아웃되었습니다.")
        self.list()
    
    def list(self):
        """메인 화면 표시"""
        if self.login_id is None and self.admin_login_id is None:
            print("\n-- 은행 계좌 관리 시스템 --")
            print("계좌 서비스를 이용하려면 로그인해주세요.")
            
            # 스케줄러 상태 표시
            if self.scheduler_manager and self.scheduler_manager.is_running():
                print(f"✅ 자동 이자 지급: {self.scheduler_manager.get_next_execution_info()}")
            
            self.menu()
            return
        
        if self.admin_login_id is not None:
            print(f"\n[관리자 모드] {self.admin_manager.get_admin_name(self.admin_login_id)}님")
            
            # 스케줄러 상태 표시
            if self.scheduler_manager:
                print(self.scheduler_manager.get_next_execution_info())
        else:
            self.account_manager.list_accounts(self.login_id)
        
        self.menu()
    
    def menu(self):
        """메뉴 표시 및 처리"""
        print("=" * 120)
        
        if self.login_id is None and self.admin_login_id is None:
            # 메인 메뉴
            print("✅ 메인메뉴: 1.회원가입 | 2.사용자 로그인 | 3.관리자 로그인 | 4.종료")
            choice = input("메뉴선택: ").strip()
            
            if choice == "1":
                self.user_manager.join()
                self.list()
            elif choice == "2":
                user_id = self.user_manager.login()
                if user_id:
                    self.login_id = user_id
                self.list()
            elif choice == "3":
                admin_id = self.admin_manager.admin_login()
                if admin_id:
                    self.admin_login_id = admin_id
                self.list()
            elif choice == "4":
                self.exit()
            else:
                print("1 ~ 4번의 숫자만 입력이 가능합니다.")
                self.menu()
        
        elif self.admin_login_id is not None:
            # 관리자 메뉴
            print("✅ 계좌관리\t\t✅ 이자관리\t\t✅ 시스템관리\t\t✅ 기타")
            print("=" * 120)
            print("1. 전체계좌조회\t\t3. 수동이자지급\t\t5. 스케줄러상태\t\t6. 로그아웃")
            print("2. 사용자별계좌조회\t\t4. 이자지급내역조회\t\t0. 종료")
            print("=" * 120)
            choice = input("메뉴선택: ").strip()
            
            if choice == "1":
                self.admin_manager.view_all_accounts()
                self.list()
            elif choice == "2":
                self.admin_manager.view_user_accounts()
                self.list()
            elif choice == "3":
                self.execute_manual_interest_payment()
                self.list()
            elif choice == "4":
                self.admin_manager.view_interest_history()
                self.list()
            elif choice == "5":
                self.show_scheduler_status()
                self.list()
            elif choice == "6":
                self.logout()
            elif choice == "0":
                self.exit()
            else:
                print("0 ~ 6번의 숫자만 입력이 가능합니다.")
                self.menu()
        
        else:
            # 사용자 메뉴
            print("✅ 계좌관리\t✅ 거래업무\t✅ 기타설정\t✅ 시스템")
            print("=" * 120)
            print("1. 계좌생성\t4. 입금\t\t8. 계좌비밀번호변경\t10. 로그아웃")
            print("2. 계좌조회\t5. 출금\t\t9. 회원정보수정\t0. 종료")
            print("3. 계좌해지\t6. 이체")
            print("\t\t7. 거래내역조회")
            print("=" * 120)
            choice = input("메뉴선택: ").strip()
            
            if choice == "1":
                self.account_manager.create_account(self.login_id)
                self.list()
            elif choice == "2":
                self.account_manager.read_account(self.login_id)
                self.list()
            elif choice == "3":
                self.account_manager.delete_account_menu(self.login_id)
                self.list()
            elif choice == "4":
                self.transaction_manager.deposit(self.login_id)
                self.list()
            elif choice == "5":
                self.transaction_manager.withdraw(self.login_id)
                self.list()
            elif choice == "6":
                self.transaction_manager.transfer(self.login_id)
                self.list()
            elif choice == "7":
                self.transaction_manager.history(self.login_id)
                self.menu()
            elif choice == "8":
                self.account_manager.change_password(self.login_id)
                self.list()
            elif choice == "9":
                self.user_manager.modify_user_info(self.login_id)
                self.list()
            elif choice == "10":
                self.logout()
            elif choice == "0":
                self.exit()
            else:
                print("0 ~ 10번의 숫자만 입력이 가능합니다.")
                self.menu()
    
    def show_scheduler_status(self):
        """스케줄러 상태 표시"""
        print("\n[스케줄러 상태 정보]")
        print("=" * 120)
        
        if self.scheduler_manager:
            if self.scheduler_manager.is_running():
                print("상태: 실행 중")
                print(self.scheduler_manager.get_next_execution_info())
                print("실행 시간: 매월 마지막 날 오후 2시")
                print("실행 내용: 모든 계좌 이자 일괄 지급")
            else:
                print("상태: 중지됨")
        else:
            print("상태: 스케줄러가 초기화되지 않음")
        
        print("=" * 120)
        input("엔터키를 누르면 메뉴로 돌아갑니다.")
    
    def execute_manual_interest_payment(self):
        """수동 이자 지급"""
        print("\n[수동 이자 지급]")
        print("=" * 120)
        print("   주의사항:")
        print("   - 자동 스케줄러가 현재 실행 중입니다.")
        
        if self.scheduler_manager and self.scheduler_manager.is_running():
            print(f"   - {self.scheduler_manager.get_next_execution_info()}")
        
        print("   - 수동 지급은 긴급상황이나 테스트 목적으로만 사용하세요.")
        print("   - 정기 이자 지급은 자동 스케줄러가 처리합니다.")
        print("=" * 120)
        
        print("\n수동 이자 지급을 실행하는 이유를 선택하세요:")
        print("1. 긴급 상황 (고객 민원, 시스템 오류 등)")
        print("2. 테스트 목적")
        print("3. 특별 지급 (이벤트, 보상 등)")
        print("4. 스케줄러 문제로 인한 수동 실행")
        print("5. 취소")
        choice = input("선택 (1 - 5): ").strip()
        
        reason_map = {
            "1": "MANUAL_EMERGENCY",
            "2": "MANUAL_TEST", 
            "3": "MANUAL_SPECIAL",
            "4": "MANUAL_SCHEDULER_ISSUE"
        }
        
        if choice == "5":
            print("수동 이자 지급이 취소되었습니다.")
            return
        
        if choice not in reason_map:
            print("잘못된 선택입니다. 취소됩니다.")
            return
        
        reason = reason_map[choice]
        
        print("\n정말로 수동 이자 지급을 실행하시겠습니까?")
        if self.user_manager.input_helper.confirm_action():
            print(f"수동 이자 지급을 실행합니다... (사유: {reason})")
            self.admin_manager.execute_interest_payment(f"{self.admin_login_id}_{reason}")
            print("✅ 수동 이자 지급이 완료되었습니다!")
        else:
            print("수동 이자 지급이 취소되었습니다.")


def main():
    """메인 함수"""
    try:
        bank_system = BankSystem()
        bank_system.run()
    except Exception as e:
        print(f"시스템 시작 오류: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
