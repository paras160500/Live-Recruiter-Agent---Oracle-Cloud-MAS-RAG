from .active_persona import fetch_all_active_persona
from .candidate_filter import find_candidates_hybrid
from openai import OpenAI
import os 
from dotenv import load_dotenv
load_dotenv()
api_key_open_ai = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key_open_ai)

def generate_hiring_recommendation(user_query, max_salary, min_exp, persona_id="rule_tech_screener"):
    
    # Validation
    active_personas = fetch_all_active_persona()
    if persona_id not in active_personas:
        return f"❌ Error: Persona '{persona_id}' not found. Available: {list(active_personas.keys())}"
    
    # Retrive Context
    persona_data = active_personas[persona_id]
    system_persona = persona_data['persona']
    grading_rubric = persona_data['criteria']

    print(f"🤖 ACTIVATING AGENT: {persona_id}")
    print(f"   Goal: {system_persona}")

    # Hybrid Search
    candidates = find_candidates_hybrid(user_query, max_salary, min_exp)

    if not candidates:
        return "⚠️ No candidates found"
    
    # Augmented the prompt 
    # Turning database raw into a readable textblock 
    context_block = ""

    for c in candidates:
        c_id , name , exp , sal , summary_lob , score = c

        summary = summary_lob.read() if hasattr(summary_lob, 'read') else str(summary_lob)

        context_block += f"""
        --- CANDIDATE PROFILE ---
        ID: {c_id}
        Name: {name}
        Cost: ${sal:,} (Budget: ${max_salary:,})
        Experience: {exp} years
        Resume Summary: {summary}
        (Vector Match Score: {score:.4f})
        -------------------------
        """

    # 5. Construct the Final Prompt
    user_message = f"""
    USER REQUEST: "{user_query}"

    CANDIDATES FOUND (Database Output):
    {context_block}

    INSTRUCTIONS:
    Based on your persona rules below, evaluate these candidates.
    1. Select the BEST fit.
    2. Explain WHY, referencing their specific skills.
    3. If they are over budget or underqualified, mention it as a risk.

    YOUR GRADING RUBRIC:
    {grading_rubric}
    """

    # 6. Generate (Call OpenAI)
    print("🧠 analyzing candidates via GPT...")

    
    response = client.chat.completions.create(
        model="gpt-5.2",
        messages=[
            {"role": "system", "content": system_persona},
            {"role": "user", "content": user_message}
        ],
        temperature=0.3 # Low temperature for factual evaluation
    )

    return response.choices[0].message.content