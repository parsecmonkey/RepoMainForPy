# log

def run(repo):
    for commit in repo.iter_commits():
        print(commit.author, commit.committed_datetime, commit.hexsha)