import openpyxl

# 엑셀 파일 열기
book = openpyxl.load_workbook("./data-format/stats_104102.xlsx")
# 로드된 엑셀 파일의 worksheet 추출
sheet0 = book.active # == book.worksheets[0]

# 서울을 제외한 인구수를 구해서 마지막 행에 추가
for i in range(0, 10):  # 컬럼 11개를 순회
    total = sheet0[str(chr(i + 66)) + "3"].value   # 아스키(ascii)코드표를 보고 알파벳 문자 참고(계 값)
    seoul = sheet0[str(chr(i + 66)) + "4"].value   # 아스키(ascii)코드표를 보고 알파벳 문자 참고(서울 값)

    # 서울을 제외한 인구수 변동 값
    output = total - seoul
    print("서울 제외 인구=", output)

    # 엑셀의 마지막 행에 추가 수정
    sheet0[str(chr(i + 66)) + "21"] = output

    # 엑셀 시트 셀의 속성 변경(색깔, 폰트 기타 등등)
    sheet0[str(chr(i + 66)) + "21"].font = openpyxl.styles.Font(size=14, color="00FF00")

# 실제 적용한 시트를 다른 엑셀에 저장
book.save("./data-format/population2.xlsx") 
print("ok")