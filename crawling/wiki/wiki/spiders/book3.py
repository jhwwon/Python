import scrapy


class Book3Spider(scrapy.Spider):
    name = "book3"
    allowed_domains = ["wikibook.co.kr"]
    start_urls = ["https://wikibook.co.kr/list"]

    def parse(self, response):
        li_list = response.css('.book-url')
        for a in li_list[:5]:   # 리스트 10개 중에서 5개만 가져오기
            href = a.css('::attr(href)').extract_first()
            print(href)

            # 개별 도서 링크 값을 가지고 해당 링크 페이제를 크롤링 요청
            yield response.follow(
                      response.urljoin(href), self.parse_book
                  )

    # 개별 도서 페이지를 스크레이핑하는 함수 --- (※4)
    def parse_book(self, response):
        # 제목과 링크 추출하기 --- (※5)
        title = response.css('.main-title::text').extract_first()
        img_url = response.css('.book-image-2d::attr(src)').extract_first()
        # 결과 출력하기 --- (※6)
        yield {
            'title': title,
            'img_url': response.urljoin(img_url)
        }