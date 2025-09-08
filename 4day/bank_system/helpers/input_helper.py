"""
입력 처리 헬퍼 클래스
Java의 InputHelper 클래스를 Python으로 변환
"""

from typing import Optional
from .validation_helper import ValidationHelper


class InputHelper:
    """사용자 입력을 처리하고 유효성을 검사하는 클래스"""
    
    def __init__(self):
        """InputHelper 초기화"""
        self.validator = ValidationHelper()
        self.account_manager = None  # 나중에 설정됨
    
    def set_account_manager(self, account_manager):
        """
        AccountManager 설정
        
        Args:
            account_manager: AccountManager 인스턴스
        """
        self.account_manager = account_manager
    
    def input(self, prompt: str) -> str:
        """
        기본 입력 메소드 - 빈 값 입력 방지
        
        Args:
            prompt: 입력 프롬프트
            
        Returns:
            str: 사용자 입력값
        """
        while True:
            try:
                user_input = input(prompt).strip()
                if user_input:
                    return user_input
            except KeyboardInterrupt:
                print("\n프로그램을 종료합니다.")
                exit(0)
            except EOFError:
                print("\n입력이 종료되었습니다.")
                exit(0)
    
    def confirm_action(self) -> bool:
        """
        작업 확인 여부 입력
        
        Returns:
            bool: 확인하면 True, 취소하면 False
        """
        print("보조메뉴: 1.확인 | 2.취소")
        choice = self.input("메뉴선택: ")
        return choice == "1"
    
    def input_user_id(self) -> str:
        """
        사용자 ID 입력 및 검증
        
        Returns:
            str: 유효한 사용자 ID
        """
        while True:
            user_id = self.input("아이디 (4~8자리, 영문+숫자): ")
            if (self.validator.validate_user_id(user_id) and 
                self.validator.check_user_id_duplicate(user_id)):
                return user_id
    
    def input_name(self) -> str:
        """
        이름 입력 및 검증
        
        Returns:
            str: 유효한 이름
        """
        while True:
            user_name = self.input("이름(20자리 이하): ")
            if self.validator.validate_user_name(user_name):
                return user_name
    
    def input_password(self, user_id: str) -> str:
        """
        비밀번호 입력 및 검증
        
        Args:
            user_id: 사용자 ID (비밀번호와 같으면 안됨)
            
        Returns:
            str: 유효한 비밀번호
        """
        while True:
            password = self.input("비밀번호 (7~12자리, 영문+숫자): ")
            if self.validator.validate_user_password(password, user_id):
                return password
    
    def input_email(self) -> str:
        """
        이메일 입력 및 검증
        
        Returns:
            str: 유효한 이메일
        """
        while True:
            email = self.input("이메일(test@example.com): ")
            if self.validator.validate_email(email):
                return email
    
    def input_phone(self) -> str:
        """
        전화번호 입력 및 검증
        
        Returns:
            str: 유효한 전화번호
        """
        while True:
            phone = self.input("전화번호(010-0000-0000 형식): ")
            if self.validator.validate_phone(phone):
                return phone
    
    def input_account_password(self) -> str:
        """
        계좌 비밀번호 입력 및 검증
        
        Returns:
            str: 유효한 계좌 비밀번호
        """
        while True:
            password = self.input("계좌 비밀번호 (4자리 숫자): ")
            if self.validator.validate_account_password(password):
                return password
    
    def input_amount(self, prompt: str) -> float:
        """
        금액 입력 및 검증
        
        Args:
            prompt: 입력 프롬프트
            
        Returns:
            float: 유효한 금액
        """
        while True:
            try:
                amount_str = self.input(prompt)
                amount = float(amount_str)
                
                if self.validator.validate_amount(amount):
                    return amount
                    
            except ValueError:
                print("올바른 숫자를 입력해주세요.")
    
    def input_account_id(self, prompt: str, own_only: bool = False, login_id: Optional[str] = None) -> str:
        """
        계좌번호 입력 및 검증
        
        Args:
            prompt: 입력 프롬프트
            own_only: 본인 계좌만 허용할지 여부
            login_id: 로그인한 사용자 ID
            
        Returns:
            str: 유효한 계좌번호
        """
        while True:
            account_id = self.input(prompt)
            
            # accountManager가 설정되지 않았으면 그냥 반환
            if self.account_manager is None:
                return account_id
            
            # 1. 계좌 존재 여부 확인
            if not self.account_manager.account_exists(account_id):
                print("존재하지 않는 계좌번호입니다.")
                continue
            
            # 2. 본인 계좌 여부 확인 (own_only가 true일 때만)
            if own_only and not self.account_manager.is_my_account(account_id, login_id):
                print("본인 계좌만 입력 가능합니다.")
                continue
            
            # 모든 검증 통과
            return account_id
    
    def input_new_user_password(self, login_id: str) -> Optional[str]:
        """
        새 비밀번호 입력 (유효성 검사 포함)
        
        Args:
            login_id: 로그인한 사용자 ID
            
        Returns:
            Optional[str]: 새 비밀번호 또는 None (기존 유지)
        """
        while True:
            try:
                user_input = input("새 비밀번호 또는 엔터 (기존 유지): ").strip()
                
                if not user_input:  # 빈 입력이면 기존 유지
                    return None
                
                if self.validator.validate_user_password(user_input, login_id):
                    return user_input
                    
            except KeyboardInterrupt:
                print("\n프로그램을 종료합니다.")
                exit(0)
            except EOFError:
                print("\n입력이 종료되었습니다.")
                exit(0)
    
    def input_new_user_email(self, login_id: str) -> Optional[str]:
        """
        새 이메일 입력 (유효성 검사 포함)
        
        Args:
            login_id: 로그인한 사용자 ID
            
        Returns:
            Optional[str]: 새 이메일 또는 None (기존 유지)
        """
        while True:
            try:
                user_input = input("새 이메일 또는 엔터 (기존 유지): ").strip()
                
                if not user_input:  # 빈 입력이면 기존 유지
                    return None
                
                if (self.validator.validate_email(user_input) and 
                    self.validator.check_email_duplicate(user_input, login_id)):
                    return user_input
                    
            except KeyboardInterrupt:
                print("\n프로그램을 종료합니다.")
                exit(0)
            except EOFError:
                print("\n입력이 종료되었습니다.")
                exit(0)
    
    def input_new_user_phone(self, login_id: str) -> Optional[str]:
        """
        새 전화번호 입력 (유효성 검사 포함)
        
        Args:
            login_id: 로그인한 사용자 ID
            
        Returns:
            Optional[str]: 새 전화번호 또는 None (기존 유지)
        """
        while True:
            try:
                user_input = input("새 전화번호 또는 엔터 (기존 유지): ").strip()
                
                if not user_input:  # 빈 입력이면 기존 유지
                    return None
                
                if (self.validator.validate_phone(user_input) and 
                    self.validator.check_phone_duplicate(user_input, login_id)):
                    return user_input
                    
            except KeyboardInterrupt:
                print("\n프로그램을 종료합니다.")
                exit(0)
            except EOFError:
                print("\n입력이 종료되었습니다.")
                exit(0)
    
    def input_menu_choice(self, prompt: str, valid_choices: list) -> str:
        """
        메뉴 선택 입력 및 검증
        
        Args:
            prompt: 입력 프롬프트
            valid_choices: 유효한 선택지 리스트
            
        Returns:
            str: 유효한 메뉴 선택
        """
        while True:
            choice = self.input(prompt)
            if choice in valid_choices:
                return choice
            else:
                print(f"올바른 선택지를 입력해주세요. ({', '.join(valid_choices)})")
    
    def input_yes_no(self, prompt: str) -> bool:
        """
        예/아니오 입력
        
        Args:
            prompt: 입력 프롬프트
            
        Returns:
            bool: 예면 True, 아니오면 False
        """
        while True:
            choice = self.input(f"{prompt} (y/n): ").lower()
            if choice in ['y', 'yes', '예', 'ㅇ']:
                return True
            elif choice in ['n', 'no', '아니오', 'ㄴ']:
                return False
            else:
                print("y 또는 n을 입력해주세요.")
