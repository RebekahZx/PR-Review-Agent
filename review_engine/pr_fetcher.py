import os
from github import Github



class PRFetcher:

    def __init__(self, repo_url, token=None):

        # Extract repo name from URL (e.g., https://github.com/user/repo -> user/repo)

        self.repo_name = "/".join(repo_url.rstrip("/").split("/")[-2:])

        self.token = token or os.environ.get("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("Set GITHUB_TOKEN in the environment (never hard-code tokens).")

        self.gh = Github(self.token)

        self.repo = self.gh.get_repo(self.repo_name)



    def get_pr_diff(self, pr_number):

        pr = self.repo.get_pull(pr_number)

        files = pr.get_files()

        diff_list = []

        for f in files:

            diff_list.append({

                "filename": f.filename,

                "patch": f.patch or ""  # the code changes

            })

        return diff_list

