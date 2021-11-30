# log

import csv
from tqdm import tqdm

import contributor as con

# コントリビュータの更新
def set_contributor(contributors, author):
    # リストの重複を確認して追加
    i = 0
    for j in range(len(contributors)):
        # authorが既に存在するか確認
        if (author in contributors[i].get_name()):
            contributors[i].add_commit_count(1)
            break
        i += 1
    # authorがまだ登録されていない場合、追加
    if (i == len(contributors)):
        contributors.append(con.Contributor(author, 1))

def run(repo):
    f = open("./log/log.csv","w+", encoding="utf_8_sig", newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow([
        'commit_no',
        'author',
        'committed_datetime',
        'message',
        'hexsha']) # csvヘッダー追加

    commits_size = repo.git.rev_list('--count', 'HEAD') # コミットの総数
    commit_count = 0
    commit_files = 0 # 変更したファイル数
    insertions   = 0 # 追加した行数
    deletions    = 0 # 削除した行数
    lines        = 0 # 変更行の合計
    contributors = []
    with tqdm(total=int(commits_size), desc='log.csv') as pbar: # プログレスバーの設定
        for commit in repo.iter_commits():
            commit_no =  int(commits_size) - commit_count
            csv_writer.writerow([
                commit_no,
                commit.author,
                commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                commit.message,
                commit.hexsha]) # csvファイルに書き込み
            commit_count += 1

            # コントリビュータを更新
            set_contributor(contributors, str(commit.author))

            pbar.update(1) # プログレスバーの進捗率を更新

            # file_list = commit.stats.files # ファイルごとの変更履歴（行）
            # for file_name in file_list:
            #     commit_files += 1
            #     insertions += file_list.get(file_name).get('insertions') # 追加した行数
            #     deletions  += file_list.get(file_name).get('deletions') # 削除した行数
            #     lines      += file_list.get(file_name).get('lines') # 変更行の合計

    f.close()

    print("コミット数：" + commits_size)
    print("変更したファイル数：" + str(commit_files))
    print("・追加した行数：" + str(insertions))
    print("・削除した行数：" + str(deletions))
    print("・変更行の合計：" + str(lines))
    print("コントリビュータ：" + str(len(contributors)))
    for contributor in sorted(contributors, key=lambda c: c.commit_count, reverse=True):
        print(contributor)