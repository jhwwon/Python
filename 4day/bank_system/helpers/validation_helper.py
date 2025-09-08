"""
유효성 검사 헬퍼 클래스
Java의 ValidationHelper 클래스를 Python으로 변환
"""

import re
from typing import Optional
from ..database import get_database_connection


class ValidationHelper:
    """입력 데이터의 유효성을 검사하는 클래스"""
    
    def __init__(self):
        """ValidationHelper 초기화"""
        self.db = get_database_connection()
    
    def validate_user_id(self, user_id: str) -> bool:
        """
        사용자 ID 유효성 검사
        
        Args:
            user_id: 검사할 사용자 ID
            
        Returns:
            bool: 유효한 ID인지 여부
        """
        if len(user_id) < 4 or len(user_id) > 8:
            print("아이디는 4~8자리여야 합니다.")
            return False
        
        # 영문자(대소문자)와 숫자가 모두 포함되어야 함
        if not re.match(r'^(?=.*[a-zA-Z])(?=.*[0-9])[a-zA-Z0-9]+$', user_id):
            print("아이디는 영문과 숫자가 모두 포함되어야 합니다.")
            return False
        
        return True
    
    def validate_user_name(self, user_name: str) -> bool:
        """
        사용자 이름 유효성 검사
        
        Args:
            user_name: 검사할 사용자 이름
            
        Returns:
            bool: 유효한 이름인지 여부
        """
        if len(user_name) > 20:
            print("이름은 20자리까지만 가능합니다.")
            return False
        
        return True
    
    def validate_user_password(self, password: str, user_id: str) -> bool:
        """
        사용자 비밀번호 유효성 검사
        
        Args:
            password: 검사할 비밀번호
            user_id: 사용자 ID (비밀번호와 같으면 안됨)
            
        Returns:
            bool: 유효한 비밀번호인지 여부
        """
        if len(password) < 7 or len(password) > 12:
            print("비밀번호는 7~12자리여야 합니다.")
            return False
        
        # 영문자(대소문자)와 숫자가 모두 포함되어야 함
        if not re.match(r'^(?=.*[a-zA-Z])(?=.*[0-9])[a-zA-Z0-9]+$', password):
            print("비밀번호는 영문과 숫자가 모두 포함되어야 합니다.")
            return False
        
        if password == user_id:
            print("비밀번호는 아이디와 같을 수 없습니다.")
            return False
        
        return True
    
    def validate_email(self, email: str) -> bool:
        """
        이메일 유효성 검사
        
        Args:
            email: 검사할 이메일
            
        Returns:
            bool: 유효한 이메일인지 여부
        """
        if len(email) > 100:
            print("이메일은 100자리까지만 가능합니다.")
            return False
        
        # 기본적인 이메일 형식 검증
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            print("올바른 이메일 형식이 아닙니다. (예: test@example.com)")
            return False
        
        # 일반적인 도메인 검증
        common_domains = ['.com', '.net', '.org', '.edu', '.gov', '.co.kr', '.kr']
        email_lower = email.lower()
        if not any(email_lower.endswith(domain) for domain in common_domains):
            print("일반적인 도메인을 사용해주세요. (.com, .net, .org, .kr 등)")
            return False
        
        return True
    
    def validate_phone(self, phone: str) -> bool:
        """
        전화번호 유효성 검사
        
        Args:
            phone: 검사할 전화번호
            
        Returns:
            bool: 유효한 전화번호인지 여부
        """
        # 010-0000-0000 형식 검증
        if not re.match(r'^010-\d{4}-\d{4}$', phone):
            print("전화번호는 010-0000-0000 형식으로 입력해주세요.")
            return False
        
        # 중간 4자리가 1000 이상인지 확인
        middle_part = phone[4:8]
        try:
            if int(middle_part) < 1000:
                print("유효하지 않은 전화번호입니다. (010-1000-0000 이상이어야 합니다)")
                return False
        except ValueError:
            print("유효하지 않은 전화번호입니다.")
            return False
        
        return True
    
    def validate_account_password(self, password: str) -> bool:
        """
        계좌 비밀번호 유효성 검사
        
        Args:
            password: 검사할 계좌 비밀번호
            
        Returns:
            bool: 유효한 계좌 비밀번호인지 여부
        """
        if len(password) != 4:
            print("계좌 비밀번호는 4자리여야 합니다.")
            return False
        
        if not re.match(r'^[0-9]+$', password):
            print("계좌 비밀번호는 숫자만 입력 가능합니다.")
            return False
        
        return True
    
    def check_user_id_duplicate(self, user_id: str) -> bool:
        """
        사용자 ID 중복 확인
        
        Args:
            user_id: 확인할 사용자 ID
            
        Returns:
            bool: 중복되지 않으면 True, 중복되면 False
        """
        try:
            query = "SELECT COUNT(*) as count FROM users WHERE user_id = :user_id"
            results = self.db.execute_query(query, {'user_id': user_id})
            
            if results and len(results) > 0:
                count = results[0].get('COUNT', results[0].get('count', 0))
                if count > 0:
                    print("이미 존재하는 아이디입니다.")
                    return False
            
            return True
            
        except Exception as e:
            print(f"아이디 중복 확인 오류: {e}")
            return False
    
    def check_email_duplicate(self, email: str, current_user_id: Optional[str] = None) -> bool:
        """
        이메일 중복 확인 (수정 시 본인 제외)
        
        Args:
            email: 확인할 이메일
            current_user_id: 현재 사용자 ID (수정 시 본인 제외용)
            
        Returns:
            bool: 중복되지 않으면 True, 중복되면 False
        """
        try:
            if current_user_id:
                query = "SELECT COUNT(*) FROM users WHERE user_email = :email AND user_id != :current_user_id"
                params = {'email': email, 'current_user_id': current_user_id}
            else:
                query = "SELECT COUNT(*) FROM users WHERE user_email = :email"
                params = {'email': email}
            
            results = self.db.execute_query(query, params)
            
            if results and len(results) > 0:
                count = results[0].get('COUNT', results[0].get('count', 0))
                if count > 0:
                    print("이미 사용 중인 이메일입니다.")
                    return False
            
            return True
            
        except Exception as e:
            print(f"이메일 중복 확인 오류: {e}")
            return False
    
    def check_phone_duplicate(self, phone: str, current_user_id: Optional[str] = None) -> bool:
        """
        전화번호 중복 확인 (수정 시 본인 제외)
        
        Args:
            phone: 확인할 전화번호
            current_user_id: 현재 사용자 ID (수정 시 본인 제외용)
            
        Returns:
            bool: 중복되지 않으면 True, 중복되면 False
        """
        try:
            if current_user_id:
                query = "SELECT COUNT(*) FROM users WHERE user_phone = :phone AND user_id != :current_user_id"
                params = {'phone': phone, 'current_user_id': current_user_id}
            else:
                query = "SELECT COUNT(*) FROM users WHERE user_phone = :phone"
                params = {'phone': phone}
            
            results = self.db.execute_query(query, params)
            
            if results and len(results) > 0:
                count = results[0].get('COUNT', results[0].get('count', 0))
                if count > 0:
                    print("이미 사용 중인 전화번호입니다.")
                    return False
            
            return True
            
        except Exception as e:
            print(f"전화번호 중복 확인 오류: {e}")
            return False
    
    def validate_amount(self, amount: float) -> bool:
        """
        금액 유효성 검사
        
        Args:
            amount: 검사할 금액
            
        Returns:
            bool: 유효한 금액인지 여부
        """
        if amount < 1000:
            print("금액은 1,000원 이상이어야 합니다.")
            return False
        
        return True
    
    def validate_account_number(self, account_number: str) -> bool:
        """
        계좌번호 유효성 검사
        
        Args:
            account_number: 검사할 계좌번호
            
        Returns:
            bool: 유효한 계좌번호인지 여부
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
