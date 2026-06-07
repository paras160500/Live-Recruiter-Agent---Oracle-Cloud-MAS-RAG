from connection_db import connection_with_oracle

def fetch_all_active_persona():    
    connection = connection_with_oracle()
    cursor = connection.cursor()
    print("Fetching Hiring Personals from Oracle DB")
    cursor.execute("SELECT rule_id, agent_persona, evaluation_criteria FROM recruitment_rules")
    rules = cursor.fetchall()

    active_personas = {}

    for r in rules:
        r_id , persona_lob , criteria_lob = r

        # FIX: Check if it's a LOB and read it, otherwise use as string
        persona = persona_lob.read() if hasattr(persona_lob, 'read') else str(persona_lob)
        criteria = criteria_lob.read() if hasattr(criteria_lob, 'read') else str(criteria_lob)

        active_personas[r_id] = {
            "persona": persona,
            "criteria": criteria
        }

        print(f"🆔 ID: {r_id}")
        print(f"👤 Persona: {persona}")
        print(f"📋 Criteria Snippet: {criteria[:80]}...")
        print("-" * 50)

    print(f"\n✅ Loaded {len(active_personas)} personas into application memory.")
    return active_personas