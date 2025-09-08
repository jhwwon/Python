"""
스케줄러 관리 매니저 클래스
Java의 SchedulerManager 클래스를 Python으로 변환 (간단 버전)
"""

import threading
import time
from datetime import datetime, timedelta
from typing import Optional
from .admin_manager import AdminManager


class SchedulerManager:
    """이자 지급 스케줄러를 관리하는 클래스"""
    
    def __init__(self, admin_manager: AdminManager):
        """SchedulerManager 초기화"""
        self.admin_manager = admin_manager
        self.scheduler_thread: Optional[threading.Thread] = None
        self.running = False
        self.stop_event = threading.Event()
    
    def start(self):
        """스케줄러 시작"""
        if self.running:
            return
        
        self.running = True
        self.stop_event.clear()
        
        # 스케줄러 스레드 시작
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        
        print("✅ 이자 지급 스케줄러가 시작되었습니다.")
    
    def stop(self):
        """스케줄러 중지"""
        if not self.running:
            return
        
        self.running = False
        self.stop_event.set()
        
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=5)
        
        print("✅ 이자 지급 스케줄러가 중지되었습니다.")
    
    def is_running(self) -> bool:
        """스케줄러 실행 상태 확인"""
        return self.running and not self.stop_event.is_set()
    
    def get_next_execution_info(self) -> str:
        """다음 실행 정보 반환"""
        if not self.is_running():
            return "스케줄러가 중지됨"
        
        # 다음 실행 시간 계산 (매월 마지막 날 오후 2시)
        now = datetime.now()
        next_month = now.replace(day=1) + timedelta(days=32)
        next_month = next_month.replace(day=1) - timedelta(days=1)  # 마지막 날
        next_execution = next_month.replace(hour=14, minute=0, second=0, microsecond=0)
        
        if next_execution <= now:
            next_execution = next_execution + timedelta(days=1)
        
        return f"다음 실행: {next_execution.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def _scheduler_loop(self):
        """스케줄러 메인 루프"""
        while self.running and not self.stop_event.is_set():
            try:
                # 현재 시간 확인
                now = datetime.now()
                
                # 매월 마지막 날 오후 2시에 실행
                if self._should_execute_interest_payment(now):
                    self._execute_scheduled_interest_payment()
                
                # 1시간마다 체크
                time.sleep(3600)
                
            except Exception as e:
                print(f"스케줄러 오류: {e}")
                time.sleep(60)  # 오류 시 1분 후 재시도
    
    def _should_execute_interest_payment(self, now: datetime) -> bool:
        """이자 지급 실행 조건 확인"""
        # 매월 마지막 날 오후 2시
        if now.hour != 14 or now.minute != 0:
            return False
        
        # 마지막 날인지 확인
        next_day = now + timedelta(days=1)
        return next_day.month != now.month
    
    def _execute_scheduled_interest_payment(self):
        """스케줄된 이자 지급 실행"""
        try:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 자동 이자 지급 실행")
            
            # 관리자 ID로 이자 지급 실행
            admin_id = "AUTO_SCHEDULER"
            success = self.admin_manager.execute_interest_payment(admin_id)
            
            if success:
                print("✅ 자동 이자 지급이 완료되었습니다.")
            else:
                print("❌ 자동 이자 지급에 실패했습니다.")
                
        except Exception as e:
            print(f"자동 이자 지급 실행 오류: {e}")
    
    def get_status_info(self) -> dict:
        """스케줄러 상태 정보 반환"""
        return {
            'running': self.is_running(),
            'next_execution': self.get_next_execution_info(),
            'thread_alive': self.scheduler_thread.is_alive() if self.scheduler_thread else False
        }
