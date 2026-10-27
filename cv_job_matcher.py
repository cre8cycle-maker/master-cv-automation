import urllib.request
import json

# 1. Local offline Ollama endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"

# 2. Strict system prompt defining the CV Block vs Job Listing Matcher logic
system_prompt = (
    "You are an automated structural career matching engine. "
    "Your job is to compare the provided Modular Master CV blocks (skills, tools, projects) "
    "against the Job Listing parameters (responsibilities, must-haves, required tool stack). "
    "Output MUST be valid JSON strictly following these keys: "
    "match_percentage (integer 0-100), "
    "direct_matches (array of strings showing overlapping skills/tools), "
    "semantic_gaps (array of strings showing missing requirements), "
    "bridge_recommendation (string explaining how existing CV blocks can frame or bridge the gap). "
    "DO NOT include any conversational filler."
)

# 3. Inputs: Master CV Blocks vs Job Listing Parameters
payload_data = """
<master_cv_blocks>
- Industries Known: Tech Operations, SaaS Enablement, Corporate Training
- Core Skills: Workflow Optimization, Facilitation, Standard Operating Procedures (SOPs)
- Tool Stack: Notion, Slack, Confluence, Basic Python Scripting
- Projects: Developed internal onboarding workflows and managed cross-functional team execution.
</master_cv_blocks>

<job_listing_parameters>
- Role: Enablement and Training Lead
- Responsibilities: Facilitate corporate training sessions, build standard operating frameworks, manage cross-functional team collaboration tools.
- Must-Haves: Experience in training delivery, documentation writing, and team workflow coordination. Nice to have: LMS administration.
</job_listing_parameters>
"""

# 4. Construct request for Ollama
data = {
    "model": "llama3",
    "prompt": f"{system_prompt}\n\n{payload_data}",
    "stream": False,
    "format": "json"
}

req = urllib.request.Request(
    OLLAMA_URL,
    data=json.dumps(data).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

try:
    print("Running local CV vs Job structural block analysis...")
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print("\n--- Structural Match Result ---")
        print(result.get("response", "No response found."))

except Exception as e:
    print(f"\n[Error] Connection failed: {e}")
    print("Make sure Ollama is running in your OS terminal (`ollama run llama3`).")