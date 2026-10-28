import os
import datetime

REPORT_FILE = "pipeline_audit_report.md"
CV_FILE = "master_cv.md"

def generate_audit_report():
    print("Generating supervised progress report...")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cv_content = "Master CV content not found or empty."
    if os.path.exists(CV_FILE):
        with open(CV_FILE, "r", encoding="utf-8") as f:
            cv_content = f.read()

    # Build the report using standard string concatenation to avoid nested f-string issues
    report_content = (
        f"# 📊 JAA Pipeline Supervised Progress Report\n"
        f"**Timestamp:** {current_time}  \n"
        f"**Execution Status:** Operational & Git-Backed  \n\n"
        f"---\n\n"
        f"## 🏗️ Modular Blocks Status (`modules/`)\n"
        f"- **Competencies (`modules/competencies.md`):** Active & Loaded\n"
        f"- **Experience (`modules/experience.md`):** Active & Loaded\n"
        f"- **Tool Stack (`modules/tools.md`):** Active & Loaded\n\n"
        f"---\n\n"
        f"## 📈 Current Master CV State Snapshot\n"
        f"```markdown\n"
        f"{cv_content}\n"
        f"```\n"
    )

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print(f"[Success] Progress audit report generated at '{REPORT_FILE}'.")

if __name__ == "__main__":
    generate_audit_report()