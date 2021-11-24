# log

import sys

def run(repo):
    sys.stdout = open("log.txt","w+", encoding="utf-8") # 標準出力をファイルに変更

    for commit in repo.iter_commits():
        print(commit.author, commit.committed_datetime, commit.hexsha)
        print(commit.message)
        
    sys.stdout = sys.__stdout__ # 元に戻す