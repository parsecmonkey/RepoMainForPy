import git
import os
import shutil

url = 'https://github.com/parsecmonkey/RepoMainForPy'

to_path = 'project' # cloneしたプロジェクトを出力するパス
delete_path = "project"

# projectフォルダが存在していれば削除
if(os.path.isdir('project/') == True):
    shutil.rmtree('project/')
        
git.Repo.clone_from(url, to_path)

# repo = git.Repo()

# for commit in repo.iter_commits('master'):
#     print(commit.author, commit.committed_datetime, commit.hexsha)