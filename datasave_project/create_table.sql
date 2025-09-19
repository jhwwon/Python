-- Oracle 데이터베이스 테이블 생성 스크립트

-- 기존 테이블 삭제 (있다면)
DROP TABLE top5List CASCADE CONSTRAINTS;

-- top5List 테이블 생성
CREATE TABLE top5List (
    seller VARCHAR2(100) NOT NULL,
    item VARCHAR2(500) NOT NULL,
    price NUMBER(10) NOT NULL
);

-- 테이블 구조 확인
DESC top5List;

-- 테이블 생성 확인
SELECT table_name, column_name, data_type, data_length, nullable
FROM user_tab_columns 
WHERE table_name = 'TOPLIST'
ORDER BY column_id;

-- 샘플 데이터 삽입 (테스트용)
INSERT INTO top5List (seller, item, price) VALUES ('테스트판매자', '테스트상품', 100000);
COMMIT;

-- 데이터 확인
SELECT * FROM top5List;
