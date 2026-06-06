from data_mgment.create_table import create_tables
from data_mgment.empty_table import empty_vector_tables
from data_mgment.verify_table import verification_of_table
from connection_db import connection_with_oracle
from data_ingestion.fetch_and_transform import get_embeddings_batch
from sample_search_query import sample_check
import oracledb

if __name__ == "__main__":
    # # Creating tables 
    # create_tables()

    # # Verify tables
    # verification_of_table()

    # # Emptying tables
    # empty_vector_tables()

    sample_check()
    pass