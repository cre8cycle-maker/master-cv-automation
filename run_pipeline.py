import subprocess
import sys
import os

def run_script(script_name):
    print(f"\n==================================================")
    print(f"Executing Pipeline Step: {script_name}")
    print(f"==================================================")
    
    if not os.path.exists(script_name):
        print(f"[Error] Script not found: {script_name}")
        sys.exit(1)
        
    result = subprocess.run([sys.executable, script_name], capture_output=False)
    
    if result.returncode != 0:
        print(f"[Error] Step '{script_name}' failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    else:
        print(f"[Success] Step '{script_name}' completed successfully.")

def main():
    print("Starting Local Offline JAA Career Pipeline...")
    
    # 1. Parse incoming Job Description
    run_script("parse_job.py")
    
    # 2. Run Structural Match Analysis against Master CV
    run_script("cv_job_matcher_dynamic.py")
    
    # 3. Run Company Domain & Industry Transferability Mapping
    run_script("domain_mapper.py")
    
    # 4. Update Master CV Version & Push to Git Cloud Backup
    run_script("update_cv_version.py")
    
    print("\n==================================================")
    print("🎉 Full JAA Pipeline Executed & Backed Up Successfully!")
    print("==================================================")

if __name__ == "__main__":
    main()