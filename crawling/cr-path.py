from urllib.parse import urljoin

base = "http://example.com/html/a.html"

print( urljoin(base, "b.html") )        # base 문자열과 b.html문자열을 합침
print( urljoin(base, "sub/c.html") )
print( urljoin(base, "../index.html") )
print( urljoin(base, "../img/hoge.png") )
print( urljoin(base, "../css/hoge.css") )