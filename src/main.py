import git
import os
import shutil

url  = 'https://github.com/parsecmonkey/RepoMainForPy'
path = 'project' # レポジトリのパス

# フォルダを削除
def rmtree(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, 0o777)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(top)

if os.path.isdir(path):
    rmtree(path) # projectフォルダが存在していれば削除

git.Repo.clone_from(url, path) # レポジトリをクローン

repo = git.Repo(path)

# git log
for commit in repo.iter_commits():
    print(commit.author, commit.committed_datetime, commit.hexsha)