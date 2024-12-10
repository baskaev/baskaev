
import requests

GITHUB_API_URL = "https://api.github.com"
USERNAME = "baskaev"  # Замените на ваш GitHub username
TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_repositories():
    url = f"{GITHUB_API_URL}/users/{USERNAME}/repos"
    headers = {"Authorization": f"token {TOKEN}"}
    params = {"sort": "created", "direction": "desc"}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def update_readme(repositories):
    with open("README.md", "r") as file:
        content = file.readlines()
    
    start_index = content.index("<!--START_SECTION:repositories-->\n") + 1
    end_index = content.index("<!--END_SECTION:repositories-->\n")
    
    repo_list = [
        f"- [{repo['name']}]({repo['html_url']}) ⭐ {repo['stargazers_count']} stars\n"
        for repo in repositories
    ]
    
    content[start_index:end_index] = repo_list
    
    with open("README.md", "w") as file:
        file.writelines(content)

if __name__ == "__main__":
    repositories = fetch_repositories()
    update_readme(repositories[:10])  # Берем 10 последних репозиториев
