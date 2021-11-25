# log

import csv

def run(repo):
    f = open("log/log.csv","w+", encoding="utf_8_sig", newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow([
        'commit_no',
        'author',
        'committed_datetime',
        'message',
        'hexsha']) # csvヘッダー追加

    commits_size = repo.git.rev_list('--count', 'HEAD') # コミットの総数
    commit_count = 0
    for commit in repo.iter_commits():
        commit_no =  int(commits_size) - commit_count
        csv_writer.writerow([
            commit_no,
            commit.author,
            commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            commit.message,
            commit.hexsha]) # csvファイルに書き込み
        commit_count += 1

    f.close()

    print("コミット数：" + commits_size)