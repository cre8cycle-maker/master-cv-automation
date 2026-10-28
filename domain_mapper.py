import urllib.request
import json

# 1. Local offline Ollama endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"

# 2. Strict system prompt for Domain/Industry Transferability Mapping
system_prompt = (
    "You are an automated industry and domain transferability mapping engine for career automation. "
    "Your job is to analyze a target job listing's company background and industry, "
    "compare it against the candidate's historical domains, and output valid JSON. "
    "Output MUST strictly follow these keys: "
    "target_industry (string), "
    "historical_domain_overlap (boolean), "
    "transferability_rationale (string explaining how past operational environments apply to this new domain). "
    "DO NOT include any conversational filler."
)

# 3. Inputs: Candidate's Historical Domains vs Target Job Listing
payload_data = """
<candidate_historical_domains>
- SaaS & B2B Software Operations
- Corporate Training & Enterprise Enablement
- Digital Transformation & Process Optimization
</candidate_historical_domains>

<target_job_listing>
- Company: FinTech Solutions Inc.
- Industry: Financial Technology / Digital Banking Software
- Listing Overview: Seeking an Enablement Lead to drive internal software adoption, streamline onboarding workflows, and author operational procedures for financial technology products.
</target_job_listing>
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
    print("Running local Company Domain & Industry Transferability mapping...")
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print("\n--- Domain Transferability Output ---")
        print(result.get("response", "No response found."))

except Exception as e:
    print(f"\n[Error] Connection failed: {e}")
    print("Make sure Ollama is running in your OS terminal (`ollama run llama3`).")