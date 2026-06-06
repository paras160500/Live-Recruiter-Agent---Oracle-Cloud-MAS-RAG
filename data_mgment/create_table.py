from connection_db import connection_with_oracle

def create_tables():
    """
        This function create tables on oracle cloud.
    """
    # Setting up connection with orcal and getting 
    connection = connection_with_oracle()
    cursor = connection.cursor()

    # Initializing the HR Recruitment Schema
    # Candidate Pool :- The Hybrid table (Structured + Vector)

    cursor.execute("""
        CREATE TABLE candidate_pool (
            candidate_id VARCHAR(50) PRIMARY KEY,
            full_name VARCHAR2(100),
            summary CLOB ,                                  -- The text we will Vectorize
            skills VARCHAR2(1000),                          -- Comma-Seprated list of Keywords
            years_experience NUMBER,                        -- For SQL Filtering (e.g. > 5 years)
            salary_expectation NUMBER,                      -- For SQL Filtering (e.g. < 120k)
            resume_vector VECTOR(1536)                      -- Semantic Brain
        )
    """)
    print("Table Candidate_pool Created.")

    # Recruitment_Rules : Domain-Specific Instructions
    # Seperate this from the Generic Context_library to show domain isolation

    cursor.execute("""
        CREATE TABLE recruitment_rules (
            rule_id VARCHAR2(50) PRIMARY KEY,
            agent_persona CLOB,                         -- eg. "Culture fit officer" vs "Technical Screener
            evaluation_criteria CLOB,                   -- Specific rubric for agent
            rule_vector VECTOR(1536)
        )
    """)

    print("Table RECRUITMENT_RULES Created")

    connection.commit()
    print("HR Schema Initialized successfully")


if __name__ == "__main__":
    create_tables()