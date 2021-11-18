import git

# urlは適宜自身が編集可能なレポジトリに書き換えてください
url = 'https://github.com/parsecmonkey/RepoMainForPy'

# cloneしたプロジェクトを出力するパス
to_path = 'project'

git.Repo.clone_from(url, to_path)