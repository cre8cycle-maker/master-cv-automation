import urllib.request
import json
import os

# 1. Local Ollama API endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"

# 2. File paths on disk
CV_FILE_PATH = "master_cv.md"
JOB_FILE_PATH = "target_job.txt"

def read_file_content(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Required file not found at: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

try:
    print(f"Reading local files: '{CV_FILE_PATH}' and '{JOB_FILE_PATH}'...")
    master_cv_text = read_file_content(CV_FILE_PATH)
    target_job_text = read_file_content(JOB_FILE_PATH)

    system_prompt = (
        "You are an automated CV vs Job Description structural analyzer. "
        "Analyze the provided Master CV content against the Target Job Description. "
        "Output valid JSON ONLY with these exact keys: "
        "match_percentage (integer), "
        "direct_matches (list of strings), "
        "semantic_gaps (list of strings), "
        "bridge_recommendation (string). "
        "Do not include any conversational text."
    )

    payload_data = f"""
<candidate_master_cv>
{master_cv_text}
</candidate_master_cv>

<target_job_description>
{target_job_text}
</target_job_description>
"""

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

    print("Executing local AI structural match analysis...")
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        
        print("\n--- Dynamic Match Result ---")
        print(result.get("response", "No response received."))

except Exception as e:
    print(f"\n[Error] Execution failed: {e}")