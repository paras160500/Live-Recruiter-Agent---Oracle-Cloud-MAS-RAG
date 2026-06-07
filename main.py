from data_mgment.create_table import create_tables
from data_mgment.empty_table import empty_vector_tables
from data_mgment.verify_table import verification_of_table
from connection_db import connection_with_oracle
from data_ingestion.fetch_and_transform import get_embeddings_batch
from sample_search_query import sample_check
from query_llm_logic.generate_recommendation import generate_hiring_recommendation

import oracledb

if __name__ == "__main__":
    # # Creating tables 
    # create_tables()

    # # Verify tables
    # verification_of_table()

    # # Emptying tables
    # empty_vector_tables()

    # Sample Hybrid Query Check
    # sample_check()
    
    search_query = "We need a Python Backend developer who can lead a team."
    max_budget = 160000
    min_experience = 4

    # Setting up proper agent persona
    agent_role = "rule_tech_screener"

    print(f"🎬 STARTING SIMULATION")
    print(f"   Query: '{search_query}'")
    print(f"   Budget: ${max_budget:,}")
    print(f"   Agent: {agent_role}\n")
    print("=" * 60)

    # Execute the pipeline
    recommendation = generate_hiring_recommendation(
        user_query=search_query,
        max_salary=max_budget,
        min_exp=min_experience,
        persona_id=agent_role
    )

    print("\n" + "=" * 60)
    print(f"📢 AI RECOMMENDATION ({agent_role})")
    print("=" * 60)
    print(recommendation)
