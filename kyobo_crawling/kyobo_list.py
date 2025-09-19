"""
주제: 프로그래밍 언어
검색어: Python
"""

import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import re

def crawl_kyobo_books():
    """교보문고에서 Python 관련 도서 제목과 할인 가격 크롤링"""
    
    # 검색 설정
    search_keyword = "Python"
    url = f"https://search.kyobobook.co.kr/web/search?vPstrKeyWord={urllib.parse.quote(search_keyword)}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        print(f"교보문고에서 '{search_keyword}' 검색 중...")
        
        # 웹 페이지 요청
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.select('div.prod_info_box')
        
        if not books:
            print("도서 정보를 찾을 수 없습니다.")
            return
        
        # 상위 5개 도서 처리
        books = books[:5]
        
        print(f"\n=== '{search_keyword}' 관련 도서 {len(books)}개 ===")
        print("=" * 70)
        
        for i, book in enumerate(books, 1):
            # 제목 추출
            title_elem = book.select_one('a.prod_info')
            title = title_elem.get_text(strip=True) if title_elem else "제목 없음"
            
            # 가격 추출
            price_elem = book.select_one('span.price')
            price = "가격 없음"
            if price_elem and price_elem.get_text(strip=True):
                price_text = price_elem.get_text(strip=True)
                if re.search(r'[\d,]+', price_text):
                    price = price_text
            
            # 결과 출력
            print(f"[{i}] {title}")
            print(f"    할인 가격: {price}")
            print("-" * 70)
            
            time.sleep(0.5)
        
        print("크롤링 완료!")
        
    except Exception as e:
        print(f"오류 발생: {e}")

def main():
    """메인 함수"""
    print("교보문고 도서 크롤링 프로그램")
    print("=" * 70)
    crawl_kyobo_books()

if __name__ == "__main__":
    main()
