import os, requests, json

JIRA_BASE = os.environ.get("JIRA_BASE_URL")
JIRA_EMAIL = os.environ.get("JIRA_EMAIL")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")
JIRA_PROJECT = os.environ.get("JIRA_PROJECT")
JIRA_ISSUE_TYPE = os.environ.get("JIRA_ISSUE_TYPE")

def create_issue(summary, description):
    if not all([JIRA_BASE, JIRA_EMAIL, JIRA_API_TOKEN]):
        raise Exception("Missing required environment variables: JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN")

    # make sure no trailing slash in base URL
    base = JIRA_BASE.rstrip("/")
    url = f"{base}/rest/api/3/issue"
    auth = (JIRA_EMAIL, JIRA_API_TOKEN)
    payload = {
        "fields": {
            "project": {"key": JIRA_PROJECT},
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": description}
                        ]  
                     }
                ]    
            },
            "issuetype": {"name": JIRA_ISSUE_TYPE}

        }
    }
    headers = {"Content-Type":"application/json"}
    r = requests.post(url, auth=auth, headers=headers, data=json.dumps(payload))

    if r.status_code == 401:
        raise Exception(
            "Unauthorized (401). Check that:\n"
            "- JIRA_BASE_URL is correct (no trailing slash)\n"
            "- JIRA_EMAIL is the Atlassian login email\n"
            "- JIRA_API_TOKEN is a valid token from https://id.atlassian.com/manage-profile/security/api-tokens\n"
        )
    elif r.status_code >= 400:
        raise Exception(f"Jira API error {r.status_code}: {r.text}")

    return r.json()

if __name__ == "__main__":
    try:
        issue = create_issue(
            "Test issue from script",
            "This is a test created by running jira_create_issue.py directly"
        )
        print("✅ Issue created:", issue)
    except Exception as e:
        print("❌ Error:", e)

