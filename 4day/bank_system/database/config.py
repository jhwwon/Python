"""
데이터베이스 설정 파일
"""

# Oracle 데이터베이스 연결 설정
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 1521,
    'service_name': 'orcl',
    'username': 'jhw1',
    'password': '1234',
    'encoding': 'UTF-8'
}

# 연결 풀 설정
POOL_CONFIG = {
    'min': 1,
    'max': 10,
    'increment': 1
}

# SQL 쿼리 상수들
class SQLQueries:
    """자주 사용되는 SQL 쿼리들을 상수로 정의"""
    
    # 사용자 관련
    INSERT_USER = """
        INSERT INTO users (user_id, user_name, user_password, user_email, user_phone, join_date)
        VALUES (:user_id, :user_name, :user_password, :user_email, :user_phone, :join_date)
    """
    
    SELECT_USER_BY_ID = """
        SELECT user_id, user_name, user_password, user_email, user_phone, join_date
        FROM users WHERE user_id = :user_id
    """
    
    SELECT_USER_BY_EMAIL = """
        SELECT user_id, user_name, user_password, user_email, user_phone, join_date
        FROM users WHERE user_email = :user_email
    """
    
    SELECT_USER_BY_PHONE = """
        SELECT user_id, user_name, user_password, user_email, user_phone, join_date
        FROM users WHERE user_phone = :user_phone
    """
    
    UPDATE_USER = """
        UPDATE users 
        SET user_name = :user_name, user_password = :user_password, 
            user_email = :user_email, user_phone = :user_phone
        WHERE user_id = :user_id
    """
    
    # 계좌 관련
    INSERT_ACCOUNT = """
        INSERT INTO accounts (account_id, account_name, account_type, account_password, 
                            balance, user_id, create_date, interest_rate, last_interest_date)
        VALUES (:account_id, :account_name, :account_type, :account_password, 
                :balance, :user_id, :create_date, :interest_rate, :last_interest_date)
    """
    
    SELECT_ACCOUNT_BY_ID = """
        SELECT account_id, account_name, account_type, account_password, balance, 
               user_id, create_date, interest_rate, last_interest_date
        FROM accounts WHERE account_id = :account_id
    """
    
    SELECT_ACCOUNTS_BY_USER = """
        SELECT account_id, account_name, account_type, account_password, balance, 
               user_id, create_date, interest_rate, last_interest_date
        FROM accounts WHERE user_id = :user_id
        ORDER BY create_date DESC
    """
    
    SELECT_ALL_ACCOUNTS = """
        SELECT a.account_id, a.account_name, a.account_type, a.account_password, a.balance, 
               a.user_id, a.create_date, a.interest_rate, a.last_interest_date,
               u.user_name
        FROM accounts a
        JOIN users u ON a.user_id = u.user_id
        ORDER BY a.create_date DESC
    """
    
    UPDATE_ACCOUNT_BALANCE = """
        UPDATE accounts 
        SET balance = :balance, last_interest_date = :last_interest_date
        WHERE account_id = :account_id
    """
    
    UPDATE_ACCOUNT_PASSWORD = """
        UPDATE accounts 
        SET account_password = :account_password
        WHERE account_id = :account_id
    """
    
    DELETE_ACCOUNT = """
        DELETE FROM accounts WHERE account_id = :account_id
    """
    
    # 거래 관련
    INSERT_TRANSACTION = """
        INSERT INTO transactions (transaction_id, transaction_date, account_id, transaction_type, 
                                amount, balance_after, counterpart_account, counterpart_name, 
                                depositor_name, transaction_memo)
        VALUES (:transaction_id, :transaction_date, :account_id, :transaction_type, 
                :amount, :balance_after, :counterpart_account, :counterpart_name, 
                :depositor_name, :transaction_memo)
    """
    
    SELECT_TRANSACTIONS_BY_ACCOUNT = """
        SELECT transaction_id, transaction_date, account_id, transaction_type, 
               amount, balance_after, counterpart_account, counterpart_name, 
               depositor_name, transaction_memo
        FROM transactions 
        WHERE account_id = :account_id
        ORDER BY transaction_date DESC
    """
    
    SELECT_TRANSACTIONS_BY_USER = """
        SELECT t.transaction_id, t.transaction_date, t.account_id, t.transaction_type, 
               t.amount, t.balance_after, t.counterpart_account, t.counterpart_name, 
               t.depositor_name, t.transaction_memo, a.account_name
        FROM transactions t
        JOIN accounts a ON t.account_id = a.account_id
        WHERE a.user_id = :user_id
        ORDER BY t.transaction_date DESC
    """
    
    # 이자 관련
    INSERT_INTEREST_PAYMENT = """
        INSERT INTO interest_payments (payment_id, account_id, payment_date, interest_amount, admin_id)
        VALUES (:payment_id, :account_id, :payment_date, :interest_amount, :admin_id)
    """
    
    SELECT_INTEREST_PAYMENTS = """
        SELECT payment_id, account_id, payment_date, interest_amount, admin_id
        FROM interest_payments
        ORDER BY payment_date DESC
    """
    
    SELECT_INTEREST_PAYMENTS_BY_ACCOUNT = """
        SELECT payment_id, account_id, payment_date, interest_amount, admin_id
        FROM interest_payments
        WHERE account_id = :account_id
        ORDER BY payment_date DESC
    """
    
    # 시퀀스 관련
    GET_NEXT_ACCOUNT_SEQ = "SELECT seq_account.NEXTVAL FROM DUAL"
    GET_NEXT_TRANSACTION_SEQ = "SELECT seq_transaction.NEXTVAL FROM DUAL"
