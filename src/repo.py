# repo

import git

# レポジトリクラス
class Repo:
    def __init__(self):
        self.repo = git.Repo

    def clone_repo(self, url, path):
        self.repo = git.Repo.clone_from(url, path) # レポジトリをクローン

r = Repo() # インスタンスを生成

def clone_repo(url, path):
    r.clone_repo(url, path)

def get_repo():
    return r.repo