from connection_db import connection_with_oracle

def empty_vector_tables():
    """
        Empty all the tables using truncate not deleting the tables
    """
    connection = connection_with_oracle()
    cursor = connection.cursor()
    try:
        print("Empting the candidate_pool")
        cursor.execute("truncate table CANDIDATE_POOL")

        print("Empting recruitment_rules")
        cursor.execute("truncate table RECRUITMENT_RULES")
    except Exception as e:
        print(f"Error emptying the tables : {str(e)}")
  