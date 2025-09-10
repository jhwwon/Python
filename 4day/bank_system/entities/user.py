"""
사용자 엔티티 클래스
Java의 User 클래스를 Python으로 변환
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """사용자 정보를 담는 클래스"""
    
    user_id: str                    # 아이디
    user_name: str                  # 이름
    user_password: str              # 비밀번호
    user_email: str                 # 이메일
    user_phone: str                 # 전화번호
    join_date: Optional[datetime] = None  # 회원가입일
    
    def __post_init__(self):
        """객체 생성 후 자동 초기화(가입일 설정)"""
        if self.join_date is None:
            self.join_date = datetime.now()
    
    def __str__(self) -> str:
        """사용자 정보를 문자열로 반환"""
        return f"User(id={self.user_id}, name={self.user_name}, email={self.user_email})"
    
    def to_dict(self) -> dict:
        """사용자 정보를 딕셔너리로 변환 (DB 저장용)"""
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_password': self.user_password,
            'user_email': self.user_email,
            'user_phone': self.user_phone,
            'join_date': self.join_date
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """딕셔너리에서 User 객체 생성 (DB 조회용)"""
        return cls(
            user_id=data.get('USER_ID', data.get('user_id', '')),
            user_name=data.get('USER_NAME', data.get('user_name', '')),
            user_password=data.get('USER_PASSWORD', data.get('user_password', '')),
            user_email=data.get('USER_EMAIL', data.get('user_email', '')),
            user_phone=data.get('USER_PHONE', data.get('user_phone', '')),
            join_date=data.get('JOIN_DATE', data.get('join_date', None))
        )
