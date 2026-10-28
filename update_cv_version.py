import urllib.request
import json
import subprocess
import os
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
CV_FILE_PATH = "master_cv.md"

def get_current_cv_content():
    if not os.path.exists(CV_FILE_PATH):
        # Default starter content if file doesn't exist
        return "# MASTER CV - VERSION: MCVversion1.0\n\n## Core Competencies\n- Workflow Optimization\n- SOP Authoring"
    with open(CV_FILE_PATH, "r", encoding="utf-8") as f:
        return f.read()

try:
    current_cv_text = get_current_cv_content()
    
    system_prompt = (
        "You are an automated Git-backed Master CV version control engine. "
        "Ingest the current Master CV file text and a newly completed learning output. "
        "1. Increment the version tag in the header (e.g., MCVversion1.0 to MCVversion1.1). "
        "2. Integrate the newly verified skill into the core competencies list. "
        "3. Output valid JSON with exact keys: "
        "new_version (string), "
        "updated_cv_content (string of full markdown document), "
        "commit_message (string describing changes). "
        "Do NOT include conversational text."
    )

    learning_output = """
- Activity Type: Dynamic File Reading Integration
- Topic Mastered: Native disk I/O handling in local Python automation pipelines (`cv_job_matcher_dynamic.py`)
- Evidence: Successfully built and executed dynamic local file reading and structured JSON generation.
"""

    payload_data = f"""
<current_master_cv_file>
{current_cv_text}
</current_master_cv_file>

<new_learning_output>
{learning_output}
</new_learning_output>
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

    print("Reading 'master_cv.md' and processing version update locally...")
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        parsed_response = json.loads(result.get("response", "{}"))

        new_version = parsed_response.get('new_version')
        commit_message = parsed_response.get('commit_message')
        updated_content = parsed_response.get('updated_cv_content')

        print(f"\nNew Version Tag: {new_version}")
        print(f"Commit Message: {commit_message}")

        # Write updated markdown straight back to master_cv.md
        with open(CV_FILE_PATH, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"Updated '{CV_FILE_PATH}' successfully on disk.")

        # Automate Git push
        print("\n--- Executing Git Backup ---")
        subprocess.run(["git", "add", CV_FILE_PATH], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("[Success] Dynamic CV update committed and pushed to GitHub!")

except Exception as e:
    print(f"\n[Error] Execution failed: {e}")