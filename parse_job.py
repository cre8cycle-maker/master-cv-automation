import urllib.request
import json

# 1. Define the local endpoint (Ollama running offline)
OLLAMA_URL = "http://localhost:11434/api/generate"

# 2. Define the strict system prompt and schema guardrails
system_prompt = (
    "You are an automated JSON extraction engine for a career automation pipeline. "
    "Your ONLY job is to analyze the provided Master CV and Job Description, check for key matches, "
    "and output valid JSON. DO NOT include conversational filler, introductions, or explanations. "
    "Output MUST strictly follow this JSON schema keys: "
    "match_score (integer), matched_keywords (array of strings), "
    "missing_gaps (array of strings), actionable_feedback (string)."
)

# 3. Define the user payload (Master CV vs Job Description)
user_payload = """
<master_cv>
- Role: Operations & Training Specialist
- Experience: Facilitated software adoption, managed team SLAs, wrote internal process documentation, coordinated onboarding workflows.
</master_cv>

<job_description>
- Role: L&D Enablement Facilitator
- Requirements: Experience in corporate training facilitation, LMS deployment, writing standard operating procedures (SOPs), and managing cross-functional team workflows.
</job_description>
"""

# 4. Construct the request body for Ollama
data = {
    "model": "llama3",
    "prompt": f"{system_prompt}\n\n{user_payload}",
    "stream": False,
    "format": "json"  # Instructs Ollama to enforce valid JSON output
}

req = urllib.request.Request(
    OLLAMA_URL,
    data=json.dumps(data).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

try:
    print("Sending request to local offline AI engine...")
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        
        # 5. Print the raw JSON response destined for BaseData0001
        print("\n--- Parsed JSON Output Received Locally ---")
        print(result.get("response", "No response field found."))

except Exception as e:
    print(f"\n[Error] Could not connect to local AI engine: {e}")
    print("Ensure Ollama is running locally via your OS terminal (`ollama run llama3`).")