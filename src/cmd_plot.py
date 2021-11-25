# plot

import matplotlib.pyplot as plt
import calendar
import datetime
import csv
import seaborn as sns
import pandas as pd

# 現在の年を取得
def get_year():
    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")
    return int(year)

# 曜日を取得
def get_dow(day): # day of week
    dow = datetime.datetime.strptime(day, '%Y-%m-%d').strftime('%a')
    return dow

# 曜日を数字で取得
def get_dow_no(dow):
    if (dow == "Sun"):
        return 0
    elif (dow == "Mon"):
        return 1
    elif (dow == "Tue"):
        return 2
    elif (dow == "Wed"):
        return 3
    elif (dow == "Thu"):
        return 4
    elif (dow == "Fri"):
        return 5
    elif (dow == "Sat"):
        return 6

# 月を英語の文字列で取得
def get_month_en(day): # day of week
    month_en = datetime.datetime.strptime(day, '%Y-%m-%d').strftime('%b')
    return month_en
    
# 現在の年の日数を取得
def calc_days():
    year_days = 0
    for i in range(12):
        year_days += calendar.monthrange(get_year(), i+1)[1]
    return year_days

# 現在の年の日付をリストで取得
def get_days_list():
    days_list = []
    for month in range(12):
        for day in range(calendar.monthrange(int(get_year()), month+1)[1]):
            days_list.append("{:<4d}-{:0>2d}-{:0>2d}".format(get_year(), month+1, day+1))
    return days_list

# 現在の年のコミットデータを作成
def set_commit_data(year_days, days_list, committed_year, committed_datetimes):
    f = open("./log/commit_data.csv","w+", encoding="utf_8_sig", newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow([
        'year',
        'month',
        'month_en',
        'day',
        'dow_no',
        'dow',
        'week',
        'commit']) # csvヘッダー追加

    day_count = 0
    week = 0
    # 現在の年の日ごとコミット数を計算
    for month in range(12):
        for day in range(calendar.monthrange(int(get_year()), month+1)[1]):
            commit_count = committed_datetimes.count(days_list[day_count])
            dow = get_dow(days_list[day_count])
            dow_no = get_dow_no(dow)
            month_en = get_month_en(days_list[day_count])
            # committed_year.setdefault(days_list[day_count], committed_datetimes.count(days_list[day_count]))
            csv_writer.writerow([
                get_year(),
                month+1,
                month_en,
                day+1,
                dow_no,
                dow,
                week,
                commit_count]) # csvファイルに書き込み
            day_count += 1

            if dow == "Sat":
                week += 1

    f.close()

def run(repo):
    # コミット履歴を取得
    committed_datetimes = []
    for commit in repo.iter_commits():
        committed_datetimes.append(commit.committed_datetime.strftime('%Y-%m-%d'))

    year_days = calc_days() # 現在の年の日数
    days_list = get_days_list() # 現在の年の日付リスト
    committed_year = {} # 現在の年の日ごとコミット数

    # コミットデータを作成
    set_commit_data(year_days, days_list, committed_year, committed_datetimes)

    # CSV読み込み
    df = pd.read_csv("./log/commit_data.csv",sep=",")
    df.columns = ['year','month','month_en','day','dow_no','dow', 'week', 'commit']
    df = df.pivot('dow_no','week','commit')
    
    f, ax = plt.subplots(figsize=(11, 3)) # 11対3のプロットを作成

    sns.heatmap(
        df, 
        cmap="Greens", 
        linewidths=.10, 
        square=True, 
        cbar=False, 
        xticklabels=4, 
        yticklabels=2)

    plt.title(str(get_year()) + " year (" + repo.git.rev_list('--count', 'HEAD') + " commit)")
    plt.xlabel('')
    plt.ylabel('')
    plt.yticks(rotation=0)
    plt.yticks([1.5, 3.5, 5.5], ['Mon', 'Wed', 'Fri'])
    plt.show() # プロット表示