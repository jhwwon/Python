import codecs

# EUC_KR로 저장된 CSV 파일 읽기
filename = "list-euckr.csv"
csv = codecs.open(filename, "r", "euc_kr").read()

rows = csv.split("\r\n")
data = []
for row in rows:
    if row == "": continue
    cells = row.split(",")  # ex) ["ID", "이름", "가격"]  [1000, "비누", 300] ...
    data.append(cells)  # ex) [ ["ID", "이름", "가격"], [1000, "비누", 300], ...]

# 결과 출력하기
for c in data:
    print(c[1], c[2])