import os
import requests

# Получаем имя пользователя и токен из переменных окружения
USERNAME = os.getenv("GITHUB_USERNAME")
TOKEN = os.getenv("GITHUB_TOKEN")

if not USERNAME or not TOKEN:
    raise ValueError("Переменные окружения GITHUB_USERNAME и GITHUB_TOKEN не установлены")

# Получаем репозитории
def get_repositories(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url, auth=(USERNAME, TOKEN))
    if response.status_code != 200:
        raise Exception(f"Ошибка: {response.status_code}, {response.text}")
    return response.json()

# Сортируем по дате обновления
def sort_repositories_by_date(repos):
    return sorted(repos, key=lambda repo: repo["updated_at"], reverse=True)

# Генерируем Markdown
def generate_markdown(repos):
    markdown = "# My GitHub Repositories\n\n"
    for repo in repos:
        name = repo["name"]
        url = repo["html_url"]
        updated_at = repo["updated_at"]
        markdown += f"- [{name}]({url}) - Last updated: {updated_at}\n"
    return markdown

if __name__ == "__main__":
    repos = get_repositories(USERNAME)
    sorted_repos = sort_repositories_by_date(repos)
    markdown_content = generate_markdown(sorted_repos)
    with open("README.md", "w") as f:
        f.write(markdown_content)
