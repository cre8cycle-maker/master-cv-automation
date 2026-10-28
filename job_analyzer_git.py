import os
import subprocess
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from langchain_ollama import ChatOllama

def fetch_job_text(url: str) -> str:
    """Fetches job page text cleanly using standard HTTP requests with browser headers."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for script in soup(["script", "style"]):
                script.extract()
            return soup.get_text(separator="\n", strip=True)
        else:
            print(f"⚠️ HTTP Error {response.status_code}: Could not fetch page directly.")
            return ""
    except Exception as e:
        print(f"⚠️ Error fetching URL: {e}")
        return ""

def extract_details_with_llama(page_text: str):
    print("🤖 Analyzing job details locally with llama3...")
    llm = ChatOllama(
        model="llama3",
        num_ctx=32000,
        temperature=0.0
    )
    
    prompt = f"""
    Analyze the following webpage text from a job posting and extract:
    1. Job Title
    2. Company Name
    3. Key Tech Stack/Skills Required
    4. Brief Summary of Responsibilities

    Webpage Text:
    {page_text[:15000]}
    """
    
    response = llm.invoke(prompt)
    return response.content

def save_and_commit_to_git(job_title: str, company: str, details: str, source_url: str):
    # Get current date for date-wise version control structure
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Create date-wise directory path: tracked_jobs/YYYY-MM-DD/
    dir_path = os.path.join("tracked_jobs", current_date)
    os.makedirs(dir_path, exist_ok=True)
    
    # Sanitize names for safe filenames
    safe_company = "".join(c for c in company if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_').lower()
    safe_title = "".join(c for c in job_title if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_').lower()
    
    if not safe_company or safe_company == "linkedin_company":
        safe_company = "target_company"
    if not safe_title or safe_title == "linkedin_role":
        safe_title = "job_posting"
        
    filename = os.path.join(dir_path, f"{safe_company}_{safe_title}.md")
    
    markdown_content = f"""# Job Application Target
- **Source URL**: {source_url}
- **Ingetion Date**: {current_date}
- **Status**: Automated Local Extraction (Llama 3)

## Extracted Details & Requirements
{details}
"""
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    print(f"📁 Saved structured target: {filename}")
    
    # Execute Git Version Control Commands automatically
    try:
        print("🔄 Running Git version control updates...")
        subprocess.run(["git", "add", filename], check=True)
        
        commit_message = f"chore(jobs): add tracked job for {company} ({current_date})"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        
        # Optional: Uncomment the line below if you want it to push automatically to remote origin
        # subprocess.run(["git", "push"], check=True)
        
        print("✅ Git SVC commit completed successfully for date:", current_date)
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git operation warning/error (make sure you are in a git repo): {e}")

def main():
    job_url = "https://www.linkedin.com/jobs/view/4477117239/"
    
    print(f"Fetching content from: {job_url}")
    page_text = fetch_job_text(job_url)
    
    if page_text:
        extracted_info = extract_details_with_llama(page_text)
        save_and_commit_to_git("Software Engineer", "LinkedIn Target", extracted_info, job_url)
    else:
        print("❌ Failed to retrieve job page text.")

if __name__ == "__main__":
    main()