# diff

import sys

def run(repo):
    sys.stdout = open('log/diff.log',"w+", encoding="utf_8_sig") # 標準出力をdiff.logに変更

    commits_size = repo.git.rev_list('--count', 'HEAD') # コミットの総数
    commit_count = 0
    hexsha = "HEAD"
    for commit in repo.iter_commits():
        commit_no =  int(commits_size) - commit_count
        if (commit_count != 0):
            print("\n--- " + str(commit_no+1) + " commit .. " + str(commit_no) + " commit ---\n")
            print(repo.git.diff(hexsha + ".." + commit.hexsha)) # ファイルの差分を取得
        hexsha = commit.hexsha
        commit_count += 1

    print("\n--- 1 commit .. 0 commit ---\n")
    print(repo.git.diff(hexsha + "..4b825dc642cb6eb9a060e54bf8d69288fbee4904")) # ファイルの差分を取得

    sys.stdout = sys.__stdout__ # 標準出力をコンソールにもどす
    print("diff.log に出力しました")