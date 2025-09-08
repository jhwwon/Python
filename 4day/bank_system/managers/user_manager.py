"""
사용자 관리 매니저 클래스
Java의 UserManager 클래스를 Python으로 변환
"""

from datetime import datetime
from typing import Optional, List
from ..database import get_database_connection, SQLQueries
from ..entities.user import User
from ..helpers.input_helper import InputHelper
from ..helpers.validation_helper import ValidationHelper


class UserManager:
    """사용자 관련 기능을 관리하는 클래스"""
    
    def __init__(self):
        """UserManager 초기화"""
        self.db = get_database_connection()
        self.validator = ValidationHelper()
        self.input_helper = InputHelper()
    
    def get_user_name(self, user_id: str) -> str:
        """
        사용자 ID로 사용자 이름 조회
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            str: 사용자 이름 또는 user_id (조회 실패 시)
        """
        try:
            results = self.db.execute_query(
                SQLQueries.SELECT_USER_BY_ID, 
                {'user_id': user_id}
            )
            
            if results:
                return results[0].get('USER_NAME', results[0].get('user_name', ''))
            
        except Exception as e:
            print(f"사용자 이름 조회 오류: {e}")
        
        return user_id
    
    def check_user_exists(self, user_id: str) -> bool:
        """
        사용자 존재 여부 확인
        
        Args:
            user_id: 확인할 사용자 ID
            
        Returns:
            bool: 사용자 존재 여부
        """
        try:
            results = self.db.execute_query(
                "SELECT COUNT(*) as count FROM users WHERE user_id = :user_id",
                {'user_id': user_id}
            )
            
            if results and len(results) > 0:
                # Oracle에서는 COUNT(*)가 대문자로 반환됨
                count = results[0].get('COUNT', results[0].get('count', 0))
                return count > 0
            
            return False
            
        except Exception as e:
            print(f"사용자 존재 확인 오류: {e}")
            return False
    
    def join(self) -> bool:
        """
        회원가입 처리
        
        Returns:
            bool: 회원가입 성공 여부
        """
        try:
            print("\n[회원가입]")
            print("=" * 50)
            
            # 사용자 정보 입력
            user_id = self.input_helper.input_user_id()
            user_name = self.input_helper.input_name()
            user_password = self.input_helper.input_password(user_id)
            user_email = self.input_helper.input_email()
            user_phone = self.input_helper.input_phone()
            
            # 사용자 객체 생성
            user = User(
                user_id=user_id,
                user_name=user_name,
                user_password=user_password,
                user_email=user_email,
                user_phone=user_phone,
                join_date=datetime.now()
            )
            
            # DB에 저장
            if self.save_user(user):
                print(f"✅ 회원가입이 완료되었습니다! 환영합니다, {user_name}님!")
                return True
            else:
                print("❌ 회원가입에 실패했습니다.")
                return False
                
        except Exception as e:
            print(f"회원가입 오류: {e}")
            return False
    
    def save_user(self, user: User) -> bool:
        """
        사용자 정보를 DB에 저장
        
        Args:
            user: 저장할 사용자 객체
            
        Returns:
            bool: 저장 성공 여부
        """
        try:
            result = self.db.execute_update(
                SQLQueries.INSERT_USER,
                user.to_dict()
            )
            return result > 0
            
        except Exception as e:
            print(f"사용자 저장 오류: {e}")
            return False
    
    def login(self) -> Optional[str]:
        """
        로그인 처리
        
        Returns:
            Optional[str]: 로그인 성공 시 user_id, 실패 시 None
        """
        try:
            print("\n[로그인]")
            print("=" * 50)
            
            # 사용자 ID 입력
            user_id = self.input_helper.input("아이디: ")
            if not self.check_user_exists(user_id):
                print("존재하지 않는 아이디입니다.")
                return None
            
            # 비밀번호 입력
            password = self.input_helper.input("비밀번호: ")
            
            # 로그인 검증
            if self.verify_login(user_id, password):
                user_name = self.get_user_name(user_id)
                print(f"✅ 로그인 성공! 환영합니다, {user_name}님!")
                return user_id
            else:
                print("❌ 비밀번호가 일치하지 않습니다.")
                return None
                
        except Exception as e:
            print(f"로그인 오류: {e}")
            return None
    
    def verify_login(self, user_id: str, password: str) -> bool:
        """
        로그인 정보 검증
        
        Args:
            user_id: 사용자 ID
            password: 비밀번호
            
        Returns:
            bool: 로그인 성공 여부
        """
        try:
            results = self.db.execute_query(
                "SELECT user_password FROM users WHERE user_id = :user_id",
                {'user_id': user_id}
            )
            
            if results:
                # Oracle에서는 컬럼명이 대문자로 반환될 수 있음
                stored_password = results[0].get('USER_PASSWORD', results[0].get('user_password', ''))
                print(f"DEBUG: 입력한 비밀번호: '{password}'")  # 디버깅용
                print(f"DEBUG: 저장된 비밀번호: '{stored_password}'")  # 디버깅용
                print(f"DEBUG: 비밀번호 길이 - 입력: {len(password)}, 저장: {len(stored_password)}")  # 디버깅용
                
                # 공백 제거 후 비교
                password_trimmed = password.strip()
                stored_trimmed = stored_password.strip()
                print(f"DEBUG: 공백 제거 후 - 입력: '{password_trimmed}', 저장: '{stored_trimmed}'")  # 디버깅용
                
                return stored_trimmed == password_trimmed
            
            return False
            
        except Exception as e:
            print(f"로그인 검증 오류: {e}")
            return False
    
    def modify_user_info(self, user_id: str) -> bool:
        """
        회원 정보 수정
        
        Args:
            user_id: 수정할 사용자 ID
            
        Returns:
            bool: 수정 성공 여부
        """
        try:
            print("\n[회원 정보 수정]")
            print("=" * 50)
            
            # 현재 사용자 정보 조회
            current_user = self.get_user_by_id(user_id)
            if not current_user:
                print("사용자 정보를 찾을 수 없습니다.")
                return False
            
            print(f"현재 정보: {current_user.user_name}, {current_user.user_email}, {current_user.user_phone}")
            print("수정하지 않을 항목은 엔터를 눌러주세요.")
            
            # 새 정보 입력
            new_name = self.input_helper.input_new_user_name(user_id)
            new_email = self.input_helper.input_new_user_email(user_id)
            new_phone = self.input_helper.input_new_user_phone(user_id)
            new_password = self.input_helper.input_new_user_password(user_id)
            
            # 수정할 정보가 있는지 확인
            if not any([new_name, new_email, new_phone, new_password]):
                print("수정할 정보가 없습니다.")
                return False
            
            # 수정된 정보로 업데이트
            update_data = {
                'user_id': user_id,
                'user_name': new_name or current_user.user_name,
                'user_email': new_email or current_user.user_email,
                'user_phone': new_phone or current_user.user_phone,
                'user_password': new_password or current_user.user_password
            }
            
            if self.update_user(update_data):
                print("✅ 회원 정보가 수정되었습니다.")
                return True
            else:
                print("❌ 회원 정보 수정에 실패했습니다.")
                return False
                
        except Exception as e:
            print(f"회원 정보 수정 오류: {e}")
            return False
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        사용자 ID로 사용자 정보 조회
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            Optional[User]: 사용자 객체 또는 None
        """
        try:
            results = self.db.execute_query(
                SQLQueries.SELECT_USER_BY_ID,
                {'user_id': user_id}
            )
            
            if results:
                return User.from_dict(results[0])
            
            return None
            
        except Exception as e:
            print(f"사용자 조회 오류: {e}")
            return None
    
    def update_user(self, user_data: dict) -> bool:
        """
        사용자 정보 업데이트
        
        Args:
            user_data: 업데이트할 사용자 데이터
            
        Returns:
            bool: 업데이트 성공 여부
        """
        try:
            result = self.db.execute_update(
                SQLQueries.UPDATE_USER,
                user_data
            )
            return result > 0
            
        except Exception as e:
            print(f"사용자 업데이트 오류: {e}")
            return False
    
    def get_all_users(self) -> List[User]:
        """
        모든 사용자 조회 (관리자용)
        
        Returns:
            List[User]: 사용자 리스트
        """
        try:
            results = self.db.execute_query(
                "SELECT * FROM users ORDER BY join_date DESC"
            )
            
            return [User.from_dict(data) for data in results]
            
        except Exception as e:
            print(f"사용자 목록 조회 오류: {e}")
            return []
    
    def delete_user(self, user_id: str) -> bool:
        """
        사용자 삭제 (관리자용)
        
        Args:
            user_id: 삭제할 사용자 ID
            
        Returns:
            bool: 삭제 성공 여부
        """
        try:
            # 계좌가 있는지 확인
            account_count = self.db.execute_query(
                "SELECT COUNT(*) as count FROM accounts WHERE user_id = :user_id",
                {'user_id': user_id}
            )
            
            if account_count[0]['count'] > 0:
                print("계좌가 있는 사용자는 삭제할 수 없습니다.")
                return False
            
            # 사용자 삭제
            result = self.db.execute_update(
                "DELETE FROM users WHERE user_id = :user_id",
                {'user_id': user_id}
            )
            
            return result > 0
            
        except Exception as e:
            print(f"사용자 삭제 오류: {e}")
            return False
