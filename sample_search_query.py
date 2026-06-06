import oracledb
from connection_db import connection_with_oracle
from data_ingestion.fetch_and_transform import get_embeddings_batch

def sample_check():
    connection = connection_with_oracle()
    cursor = connection.cursor()
    
    user_query = "Leadership and teambuilding Experience"
    max_budget = 170000

    print(f"🔎 Query: '{user_query}'")
    print(f"💰 Constraint: Salary <= ${max_budget}\n")

    # First generate embeddings for the user query
    query_vector = get_embeddings_batch([user_query])[0]

    # Execute Hybrid SQL
    # Filter by SQL Salary and order by vector distance

    cursor.setinputsizes(v=oracledb.DB_TYPE_VECTOR)
    cursor.execute("""
        SELECT candidate_id, full_name, salary_expectation, summary,
            VECTOR_DISTANCE(resume_vector, :v, DOT) as similarity
        FROM candidate_pool
        WHERE salary_expectation <= :budget
        ORDER BY similarity DESC
        FETCH FIRST 3 ROWS ONLY
    """, {"v": query_vector, "budget": max_budget})

    results = cursor.fetchall()

    print("Hybrid Search Result")
    for r in results:
        cand_id, name, salary, summary_lob, score = r

        # FIX: Convert LOB to string
        summary_text = summary_lob.read()

        print(f"Candidate: {name} (ID: {cand_id})")
        print(f"Salary: ${salary:,}")
        print(f"Match Score: {score:.4f}")
        print(f"Summary Snippet: {summary_text[:100]}...")
        print("-" * 50)