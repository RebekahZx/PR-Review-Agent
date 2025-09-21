from github import Github



class PRFetcher:

    def __init__(self, repo_url, token=None):

        # Extract repo name from URL (e.g., https://github.com/user/repo -> user/repo)

        self.repo_name = "/".join(repo_url.rstrip("/").split("/")[-2:])

        self.token = token or "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"  # Replace or use env var

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

