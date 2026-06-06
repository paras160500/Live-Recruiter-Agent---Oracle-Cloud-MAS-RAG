from connection_db import connection_with_oracle
import oracledb
from openai import OpenAI
from fetch_and_transform import get_embeddings_batch

def insert_SQL_data(hr_data):
    """
        Insert SQL data to both tables(No vector data)
        This need a dictionary which we need to add to SQL
    """
    connection = connection_with_oracle()
    cursor = connection.cursor()
    candidates = hr_data.get("candidates" , [])
    for cand in candidates:
        cursor.execute("""
                MERGE INTO candidate_pool target
                USING (SELECT :candidate_id AS id FROM dual) source
                ON (target.candidate_id = source.id)
                WHEN NOT MATCHED THEN
                    INSERT (candidate_id, full_name, years_experience, salary_expectation, skills, summary)
                    VALUES (:candidate_id, :full_name, :years_experience, :salary_expectation, :skills, :summary)
            """, {
                "candidate_id": cand['candidate_id'],
                "full_name": cand['full_name'],
                "years_experience": cand['years_experience'],
                "salary_expectation": cand['salary_expectation'],
                "skills": cand['skills'],
                "summary": cand['summary']
            })
    print(f"{len(candidates)} added to the candidate_pool")


# Now with Rules

    rules = hr_data.get("rules" , [])
    for rule in rules:
            cursor.execute("""
                MERGE INTO recruitment_rules target
                USING (SELECT :rule_id AS id FROM dual) source
                ON (target.rule_id = source.id)
                WHEN NOT MATCHED THEN
                    INSERT (rule_id, agent_persona, evaluation_criteria)
                    VALUES (:rule_id, :agent_persona, :evaluation_criteria)
            """, {
                "rule_id": rule['rule_id'],
                "agent_persona": rule['agent_persona'],
                "evaluation_criteria": rule['evaluation_criteria']
            })

    print(f"{len(rules)} added to the recruitment_rules table")

    connection.commit()
    print("\n✅ SQL Data Added.")


def insert_vector_data():
    """
        Fetch the whole table row and then convert into vector and store  again 
        takes no arguments.
    """
    connection = connection_with_oracle()
    cursor = connection.cursor()
    # Start with candidate_pool
    cursor.execute("SELECT candidate_id, summary FROM candidate_pool WHERE resume_vector IS NULL")
    rows_to_process = cursor.fetchall()

    if rows_to_process:
        summaries = [row[1].read() for row in rows_to_process]
        vectors = get_embeddings_batch(summaries)

        for i, (cand_id, _) in enumerate(rows_to_process):
                cursor.setinputsizes(vec=oracledb.DB_TYPE_VECTOR)
                cursor.execute("""
                    UPDATE candidate_pool
                    SET resume_vector = :vec
                    WHERE candidate_id = :id
                """, {"vec": vectors[i], "id": cand_id})
        
        connection.commit()
        print("--- Candidates Update with Vector")
    else:
        print("--- No Candidate need vectorization")


    # Recruitment Rules
    cursor.execute("SELECT rule_id, agent_persona || ' ' || evaluation_criteria FROM recruitment_rules WHERE rule_vector IS NULL")
    rows_to_process = cursor.fetchall()

    if rows_to_process:
        # Check the text is string of lob(CLOB)
        text = [] 
        for row in rows_to_process:
            data = row[1]
            if hasattr(data , 'read'):
                text.append(data.read()) # For CLOB
            else:
                text.append(data) # For string 

        vectors = get_embeddings_batch(text) 

        for i, (rule_id, _) in enumerate(rows_to_process):
                cursor.setinputsizes(vec=oracledb.DB_TYPE_VECTOR)
                cursor.execute("""
                    UPDATE recruitment_rules
                    SET rule_vector = :vec
                    WHERE rule_id = :id
                """, {"vec": vectors[i], "id": rule_id})

        connection.commit()
        print("--- Rules Update with Vector")
    else:
        print("--- No Row required any Vectorization")   

    print("\n Vectorization Done 💯")      
