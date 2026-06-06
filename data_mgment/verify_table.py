from connection_db import connection_with_oracle

def verification_of_table():
    connection = connection_with_oracle()
    cursor = connection.cursor()
    cursor.execute(""" 
        SELECT table_name
        from user_tables 
        where table_name in ('CANDIDATE_POOL' , 'RECRUITMENT_RULES')
        order by table_name   
    """)

    tables = cursor.fetchall()
    print(f"Tables found {len(tables)}")

    # Inspect the Candidate_pool Table 
    print("Column Defination of the candidate_pool Table")
    cursor.execute("""
        select column_name , data_type , data_length
        from user_tab_columns
        where table_name = 'CANDIDATE_POOL'
        order by column_id
    """)

    for row in cursor.fetchall():
        print(row)


    # Inspect the Recruitment_rules Table
    print("")
    print("*"*50) 
    print("\nColumn Defination of the Recruitment_rules Table")
    cursor.execute("""
        select column_name , data_type , data_length
        from user_tab_columns
        where table_name = 'RECRUITMENT_RULES'
        order by column_id
    """)

    for row in cursor.fetchall():
        print(row)


    # connection Heartbeat
    print("")
    print("*"*50)
    print("\nRunning a simple test query on DUAL...")
    cursor.execute("select 'Oracle connection OK' from dual")
    print(cursor.fetchone()[0])