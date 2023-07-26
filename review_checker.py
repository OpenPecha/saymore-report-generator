from pathlib import Path
from annotation_time_report import dump_yaml

import requests

def has_merge_commit(repo):
    url = f'https://api.github.com/repos/MonlamAI/{repo}/commits'
    response = requests.get(url)

    if response.status_code == 200:
        commits = response.json()

        for commit in commits:
            if 'parents' in commit and len(commit['parents']) > 1:
                return True

        return False

    else:
        print(f'Failed to fetch commits from GitHub API. Status Code: {response.status_code}')
        return None
    
def get_repo_without_merge_commit(repo_list):
    repo_without_merge_commit = []
    for repo in repo_list:
        if not has_merge_commit(repo):
            repo_without_merge_commit.append(repo)
    return repo_without_merge_commit

if __name__ == "__main__":

    repo_list = Path('./repo_list.txt').read_text().split('\n')
    repo_without_merge_commit = get_repo_without_merge_commit(repo_list)
    dump_yaml(repo_without_merge_commit, Path('./repo_without_merge_commit.yaml'))