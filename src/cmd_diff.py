# diff

import sys
from tqdm import tqdm

# 変更行から文字を検索し、その行を抜き出す
def search_lines(repo, hexsha_after, hexsha_before, commit_no):
    s = repo.git.diff(hexsha_after + ".." + hexsha_before)  # diffログを"s"に入れる
    lines = s.splitlines()                                  # 行ごと(改行判定(split)もして）リスト化
    
    search_flag = "False"
    search = []
    for line in lines:                                      # 行ごとにまわす
        if line.startswith("+") or line.startswith("-"):    # もしも行の先頭が"+"or"-""の時...
            # if "@" in line:                               # もしも"@"が含まれていた時...
            search.append(line)
            search_flag = "True"

    if search_flag:
        print("\n--- " + str(commit_no+1) + " commit .. " + str(commit_no) + " commit ---\n")
        for list in search:                                #ログで見やすく改行するためのfor文
            print(list)

def run(repo):
    sys.stdout = open('./log/diff.log',"w+", encoding="utf_8_sig") # 標準出力をdiff.logに変更

    sum_commits  = repo.git.rev_list('--count', 'HEAD') # コミットの総数
    commit_count = 0
    hexsha_after = "HEAD" # 差分取得用のハッシュ値（親）

    with tqdm(total=int(sum_commits), desc='diff.log') as pbar: # プログレスバーの設定
        for commit in repo.iter_commits():
            commit_no =  int(sum_commits) - commit_count

            if (commit_count != 0):
                # print(repo.git.diff(hexsha + ".." + commit.hexsha)) # ファイルの差分を取得

                search_lines(repo, hexsha_after, commit.hexsha, commit_no) # 変更行から文字を検索し、その行を抜き出す

            hexsha_after = commit.hexsha
            commit_count += 1
            pbar.update(1) # プログレスバーの進捗率を更新

    search_lines(repo, hexsha_after, "4b825dc642cb6eb9a060e54bf8d69288fbee4904", 0) # 最初のコミットの差分

    sys.stdout = sys.__stdout__ # 標準出力をコンソールにもどす