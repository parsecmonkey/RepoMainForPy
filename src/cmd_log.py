# log

import csv
from tqdm import tqdm

import contributor as con

# コントリビュータの追加した行などを更新
def add_con_lines(c, insertions, deletions): # c:contributors
    c.add_insertions(insertions) # 追加した行
    c.add_deletions(deletions) # 削除した行

# コントリビュータの更新
def set_contributor(c, author, insertions, deletions, commit): # c:contributors
    # リストの重複を確認して追加
    i = 0
    for j in range(len(c)):
        # authorが既に存在するか確認
        if author in c[i].get_name():
            c[i].add_commit_count(1)
            add_con_lines(c[i], insertions, deletions)
            c[i].set_first_commit(commit.committed_datetime.strftime('%Y-%m-%d'))
            break
        i += 1
    # authorがまだ登録されていない場合、追加
    if i == len(c):
        c.append(con.Contributor(author, 1))
        add_con_lines(c[i], insertions, deletions)
        c[i].set_last_commit(commit.committed_datetime.strftime('%Y-%m-%d'))

def run(repo):
    # log.csv
    f_log = open("./log/log.csv","w+", encoding="utf_8_sig", newline='')
    csv_log = csv.writer(f_log)
    # csvヘッダー追加
    csv_log.writerow([
        'commit_no',
        'author',
        'committed_datetime',
        'message',
        'hexsha'])

    # contributors.csv
    f_con = open("./log/contributors.csv","w+", encoding="utf_8_sig", newline='')
    csv_con = csv.writer(f_con)
    csv_con.writerow([
        'Contributor',
        'Commits(%)',
        '+lines',
        '-lines',
        'First commit',
        'Last commit',
        'Active days',
        'Ranking'])

    sum_commits    = repo.git.rev_list('--count', 'HEAD') # コミットの総数
    commit_count   = 0
    commit_files   = 0 # 変更したファイル数
    sum_insertions = 0 # 追加した行数の合計
    sum_deletions  = 0 # 削除した行数の合計
    lines          = 0 # 変更行の合計
    merge_count    = 0 # マージコミット数
    contributors   = []
    with tqdm(total=int(sum_commits), desc='log.csv') as pbar: # プログレスバーの設定
        for commit in repo.iter_commits():
            commit_no =  int(sum_commits) - commit_count
            insertions   = 0 # 追加した行数（コミットごと）
            deletions    = 0 # 削除した行数（コミットごと）

            file_list = commit.stats.files # ファイルごとの変更履歴（行）
            for file_name in file_list:
                commit_files += 1
                insertions += file_list.get(file_name).get('insertions') # 追加した行数
                deletions  += file_list.get(file_name).get('deletions') # 削除した行数
                lines      += file_list.get(file_name).get('lines') # 変更行の合計

            # log.csvに書き込み
            csv_log.writerow([
                commit_no,
                commit.author,
                commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                commit.message,
                commit.hexsha])
            commit_count += 1

            # コントリビュータを更新
            set_contributor(contributors, str(commit.author), insertions, deletions, commit)

            sum_insertions += insertions
            sum_deletions  += deletions

            # マージコミット数を計測
            if commit.message.startswith("Merge pull request"):
                merge_count += 1

            pbar.update(1) # プログレスバーの進捗率を更新

    rank = 1
    with tqdm(total=len(contributors), desc='contributors.csv') as pbar:
        for con in sorted(contributors, key=lambda c: c.commit_count, reverse=True):
            # contributors.csvに書き込み
            commit_percent = con.get_commit_count() / int(sum_commits) * 100
            csv_con.writerow([
                con.get_name(),
                str(con.get_commit_count()) + "({:.1f})".format(commit_percent),
                con.get_insertions(),
                con.get_deletions(),
                con.get_first_commit(),
                con.get_last_commit(),
                0,
                rank])
            rank += 1
            pbar.update(1)

    f_log.close()
    f_con.close()

    print("コミット数：" + sum_commits)
    print("マージコミット数：" + str(merge_count))
    print("変更したファイル数(のべ)：" + str(commit_files))
    print("・追加した行数：" + str(sum_insertions))
    print("・削除した行数：" + str(sum_deletions))
    print("・変更行の和　：" + str(lines))
    print("・変更行の差　：" + str(sum_insertions - sum_deletions))
    print("コントリビュータ：" + str(len(contributors)))
    for contributor in sorted(contributors, key=lambda c: c.commit_count, reverse=True):
        print(contributor)