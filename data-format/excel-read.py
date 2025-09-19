import openpyxl

# 엑셀 파일 열기
book = openpyxl.load_workbook("./data-format/stats_104102.xlsx")
# 로드된 엑셀 파일의 worksheet 추출
sheet0 = book.worksheets[0]

# 시트의 각 행을 순서대로 추출
data = []
for row in sheet0.rows:
    data.append([row[0].value, row[10].value])     # 1번째 컬럼(지역명)과 11번째 컬럼값(2018) 가져오기. 
    # print([row[0].value, row[10].value])

# 필요없는 앞의 3줄 삭제하기
del data[0]; del data[1]; del data[2]

# 데이터를 인구 순서로 정렬
data = sorted(data, key=lambda x:x[1])  # 인구 변동 값을 key로 해서 오름차순으로 정렬해서 다시 data에 덮어씌움

# 하위 5위를 출력
for i, a in enumerate(data):
    if i >= 5: break   # 하위 5위까지만 처리하고 빠져나감
    print(i+1, a[0], a[1])  # 순위 지역 변동수