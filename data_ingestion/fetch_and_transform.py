import urllib.request
import time 
import os, json
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
import tiktoken
tokenizre = tiktoken.get_encoding('cl100k_base')
open_ai_api_key = os.getenv("OPENAI_API_KEY")

# Fetching  data  and saving in local
def fetch_and_save_data():
    url = "https://raw.githubusercontent.com/Denis2054/RAG-Driven-Generative-AI-2nd-Edition/main/enterprise_data/talent_acquisition/hr_data.json"
    output_name = 'hr_data.json'

    urllib.request.urlretrieve(url , output_name)
    print("Download complete")

    # Let the file system settle down
    print("Let file system settle down")
    time.sleep(5)

    print("\n🎉 SUCCESS!")


# Load HR Data in memory
def load_in_memory():
    """
        For fetching the hr_data from the local and make dictionary
        This will return dict of data
    """
    hr_data = {}
    file_path = "hr_data.json"

    if os.path.exists(file_path):
        try:
            with open(file_path , "r" , encoding="utf-8") as file:
                hr_data = json.load(file)
            print(f"✅ HR Data Loaded Successfully")
            print(f"   - Candidates found: {len(hr_data.get('candidates', []))}")
            print(f"   - Recruitment Rules found: {len(hr_data.get('rules', []))}")
            return hr_data
        except json.JSONDecodeError as e:
            print("Error in data loading from file to memory")
    else:
        print("No File Exist")
        return None 


# Chunking process logic

def chunk_text(text , chunk_size = 400 , overlap = 50):
    """ 
        Chunk Token based on the token count and overlap 
    """
    tokens = tokenizre.encode(text)
    chunks = []
    for i in range(0 , len(tokens), chunk_size - overlap):
        chunk_tokens = tokens[i : i + chunk_size]
        chunk_text = tokenizre.decode(chunk_tokens)
        chunk_text = chunk_text.replace('\n' , " ")
        if chunk_text:
            chunks.append(chunk_text)
    return chunks


# Embeddings logic

EMBEDDING_DIM = 1536 # Dimension for text-embedding-3-small
GENERATION_MODEL = "gpt-5.2"

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_embeddings_batch(texts):
    """
    Generates embeddings for a batch of texts using OpenAI.
    """
    
    client = OpenAI(api_key=open_ai_api_key)
    EMBEDDING_MODEL = "text-embedding-3-small"
    texts = [t.replace("\n", " ") for t in texts]

    response = client.embeddings.create(input=texts, model=EMBEDDING_MODEL)

    return [item.embedding for item in response.data]