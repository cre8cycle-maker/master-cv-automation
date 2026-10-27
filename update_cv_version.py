import urllib.request
import json
import subprocess
import os

# 1. Local offline Ollama endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"

# 2. Strict system prompt for autonomous Git-backed CV versioning
system_prompt = (
    "You are an automated Git-backed Master CV version control and learning integration engine. "
    "Your job is to take the current Master CV state, ingest a newly completed learning output, "
    "increment the version number correctly (e.g., MCVversion1.0 to MCVversion1.1), "
    "update the modular competencies section, "
    "and output valid JSON containing: "
    "new_version (string), "
    "updated_cv_content (string of the full updated markdown content), "
    "commit_message (string describing the version increment and verified skill addition). "
    "DO NOT include any conversational filler."
)

# 3. Inputs: Current Master CV snippet vs Newly Completed Learning Output
payload_data = """
<current_master_cv>
# MASTER CV - VERSION: MCVversion1.0

<core_competencies>
- Workflow Optimization
- SOP Authoring
</core_competencies>
</current_master_cv>

<new_learning_output>
- Activity Type: Hands-on Python Script Execution
- Topic Mastered: Local JSON parsing and structural API calls via Ollama (`parse_job.py` and `cv_job_matcher.py`)
- Evidence: Successfully executed local offline parsing scripts generating valid JSON match schemas.
</new_learning_output>
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
    print("Running local AI version control and verified skill updater...")
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        
        parsed_response = json.loads(result.get("response", "{}"))
        new_version = parsed_response.get('new_version')
        commit_message = parsed_response.get('commit_message')
        updated_content = parsed_response.get('updated_cv_content')

        print(f"\n--- Version Update Generated ---")
        print(f"New Version Tag: {new_version}")
        print(f"Commit Message: {commit_message}")

        # 5. Write the updated content to your local master_cv.md file
        cv_file_path = "master_cv.md"
        with open(cv_file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"Successfully updated local file: {cv_file_path}")

        # 6. Execute Git Automation (Add, Commit, Push)
        print("\n--- Executing Git Cloud Backup ---")
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
        print("\n[Success] Git commit and push completed! Your cloud repository is now updated.")

except Exception as e:
    print(f"\n[Error] Execution failed: {e}")
    print("Make sure Ollama is running in your OS terminal (`ollama run llama3`).")