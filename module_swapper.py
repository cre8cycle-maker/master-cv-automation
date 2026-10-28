import os
import json
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
MODULES_DIR = "modules"

def load_module(filename):
    path = os.path.join(MODULES_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def dynamic_module_swap():
    print("Executing Dynamic Module Swapping Analysis...")
    
    competencies = load_module("competencies.md")
    experience = load_module("experience.md")
    tools = load_module("tools.md")
    
    target_job = ""
    if os.path.exists("target_job.txt"):
        with open("target_job.txt", "r", encoding="utf-8") as f:
            target_job = f.read()
    else:
        target_job = "General Tech Operations Role"

    system_prompt = (
        "You are an AI Modular CV Architect. "
        "Review the target job description and the available modular blocks. "
        "Select and prioritize which competencies and experiences from the modules "
        "best fit this specific job. Output valid JSON with keys: "
        "selected_competencies (list), "
        "selected_experiences (list), "
        "rationale (string)."
    )

    payload = f"""
<target_job>
{target_job}
</target_job>

<available_competencies>
{competencies}
</available_competencies>

<available_experiences>
{experience}
</available_experiences>
"""

    data = {
        "model": "llama3",
        "prompt": f"{system_prompt}\n\n{payload}",
        "stream": False,
        "format": "json"
    }

    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )

    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print("\n--- Dynamic Module Swapping Selection ---")
        print(result.get("response", "No response."))

if __name__ == "__main__":
    dynamic_module_swap()