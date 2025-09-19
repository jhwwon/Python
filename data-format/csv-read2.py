import csv, codecs


# CSV 파일 열기
filename = "list-euckr.csv"
fp = codecs.open(filename, "r", "euc-kr")

# 한 줄씩 읽어 들이기(CSV 모듈 이용)
reader = csv.reader(fp, delimiter=",")

for cells in reader:
    print(cells[1], cells[2])

