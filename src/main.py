import git
import os
import shutil
import subprocess

url = 'https://github.com/parsecmonkey/RepoMainForPy'

to_path = 'project' # cloneしたプロジェクトを出力するパス
delete_path = "project"

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

rmtree(delete_path) # projectフォルダが存在していれば削除

git.Repo.clone_from(url, to_path)

# repo = git.Repo()

# for commit in repo.iter_commits('master'):
#     print(commit.author, commit.committed_datetime, commit.hexsha)