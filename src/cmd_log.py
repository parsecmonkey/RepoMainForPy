# log

import sys

def run(repo):
    sys.stdout = open("log.txt","w+", encoding="utf-8") # 標準出力をファイルに変更

    commits_size = repo.git.rev_list('--count', 'HEAD') # コミットの総数
    commit_count = 0
    for commit in repo.iter_commits():
        print("---", int(commits_size) - commit_count, "commit ---")
        print("author :", commit.author)
        print("committed_datetime :", commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S'))
        print("hexsha :", commit.hexsha)
        print(commit.message)
        commit_count += 1

    sys.stdout = sys.__stdout__ # 元に戻す

    print("コミット数：" + commits_size)