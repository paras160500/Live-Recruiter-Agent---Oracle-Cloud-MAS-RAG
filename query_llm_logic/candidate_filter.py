from data_ingestion.fetch_and_transform import get_embeddings_batch
import oracledb
from connection_db import connection_with_oracle

def find_candidates_hybrid(user_query, max_salary=1000000, min_experience=0):
    ''' 
        Perfom Hybrid search
        1 :- Vector : Semantically match the user query against the candidate resume
        2 :- SQL : Filter out the candidate who dont meet the salary and experience 
    '''
    print(f"Searching for user query : {user_query}")
    print(f"Constrain : Salary <= ${max_salary} , Experience >= {min_experience}")

    # Vectorize the query using the helper function
    query_vector = get_embeddings_batch([user_query])[0]

    # Prepare a Hybrid Query Search
    # we select the candidate details and the distance score 
    # We use Dot product for similarity(Higher is better)

    sql = """
        SELECT candidate_id, full_name, years_experience, salary_expectation, summary,
               VECTOR_DISTANCE(resume_vector, :v, DOT) as similarity
        FROM candidate_pool
        WHERE salary_expectation <= :max_sal
          AND years_experience >= :min_exp
        ORDER BY similarity DESC
        FETCH FIRST 3 ROWS ONLY
    """

    connection = connection_with_oracle()
    cursor = connection.cursor()

    # Execute
    cursor.setinputsizes(v=oracledb.DB_TYPE_VECTOR)

    cursor.execute(sql, {
        "v": query_vector,
        "max_sal": max_salary,
        "min_exp": min_experience
    })

    results = cursor.fetchall()
    converted_results = []

    for row in results:
        c_id, name, exp, sal, summary_lob, score = row
        summary_text = summary_lob.read() if hasattr(summary_lob, 'read') else str(summary_lob)
        converted_results.append((c_id, name, exp, sal, summary_text, score))

    cursor.close()
    connection.close()

    print(f"   -> Found {len(converted_results)} candidates fitting criteria.\n")
    return converted_results


def check_candidate_query_logic():
    test_query = "Experienced Python Developer"
    test_salary = 150000
    test_exp = 2

    print(f"🧪 Testing Engine with: '{test_query}' (Max Salary: ${test_salary:,})")

    results = find_candidates_hybrid(test_query, max_salary=test_salary, min_experience=test_exp)

    print("--- Test Results ---")
    for r in results:
        c_id, name, exp, sal, summary_lob, score = r

        # Handle LOB conversion safely
        summary_text = summary_lob.read() if hasattr(summary_lob, 'read') else str(summary_lob)

        print(f"✅ Found: {name}")
        print(f"   Salary: ${sal:,}")
        print(f"   Match Score: {score:.4f}")
        print("-" * 30)