# plot

import matplotlib.pyplot as plt
import calendar
import datetime
from datetime import datetime as dt
import csv
import seaborn as sns
import pandas as pd
from tqdm import tqdm

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
    if   (dow == "Sun"): return 0
    elif (dow == "Mon"): return 1
    elif (dow == "Tue"): return 2
    elif (dow == "Wed"): return 3
    elif (dow == "Thu"): return 4
    elif (dow == "Fri"): return 5
    elif (dow == "Sat"): return 6

# 月を英語の文字列で取得
def get_month_en(day): # day of week
    month_en = datetime.datetime.strptime(day, '%Y-%m-%d').strftime('%b')
    return month_en

# 月が変わった(week+0.5)を取得
def get_month_change_point(year_dayslist):
    month_point = [] # 月が替わるタイミングのweek

    day_count = 0
    week = 0
    for month in range(12):
        month_point.append(week+0.5)
        for i in range(calendar.monthrange(int(get_year()), month+1)[1]):
            dow = get_dow(year_dayslist[day_count])
            day_count += 1
            if dow == "Sat":
                week += 1
                
    return month_point
    
# 現在の年の日数を取得
def calc_days():
    year_days = 0
    for i in range(12):
        year_days += calendar.monthrange(get_year(), i+1)[1]
    return year_days

# 現在の年の日付をリストで取得
def get_year_dayslist():
    year_dayslist = []
    for month in range(12):
        for day in range(calendar.monthrange(int(get_year()), month+1)[1]):
            year_dayslist.append("{:<4d}-{:0>2d}-{:0>2d}".format(get_year(), month+1, day+1))
    return year_dayslist

# 現在の年のコミットデータを作成
def set_commit_calendar( year_days, year_dayslist, committed_year, committed_datetimes):
    f = open("./log/commit_calendar.csv","w+", encoding="utf_8_sig", newline='')
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
    with tqdm(total=year_days, desc='commit_calendar.csv') as pbar: # プログレスバーの設定
        for month in range(12):
            for day in range(calendar.monthrange(int(get_year()), month+1)[1]):
                commit_count = committed_datetimes.count(year_dayslist[day_count])
                dow = get_dow(year_dayslist[day_count])
                dow_no = get_dow_no(dow)
                month_en = get_month_en(year_dayslist[day_count])
                # committed_year.setdefault(year_dayslist[day_count], committed_datetimes.count(year_dayslist[day_count]))
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

                pbar.update(1) # プログレスバーの進捗率を更新

    f.close()

# 日付差の日数を算出（リストに最終日も含めたいので、＋１）
def get_dayslist(committed_datetimes, sum_commits):
    dayslist = [] # 最初から最後のコミット間の日付リスト
    first_commit = committed_datetimes[int(sum_commits)-1]
    last_commit  = committed_datetimes[0]
    # 日付条件の設定
    strdt = dt.strptime(first_commit, '%Y-%m-%d').date()  # 開始日
    enddt = dt.strptime(last_commit, '%Y-%m-%d').date()  # 終了日
    # 日付差の日数を算出（リストに最終日も含めたいので、＋１しています）
    days_num = (enddt - strdt).days + 1

    for i in range(days_num):
        dayslist.append(strdt + datetime.timedelta(days=i)) # 日付差のリスト

    return dayslist

# コミットの合計値を日付順で計算
def get_sum_commit_list(committed_datetimes, dayslist):
    sum_commit = 0 # コミット合計
    sum_commit_list = []
    for day in dayslist:
        sum_commit += committed_datetimes.count(str(day))
        sum_commit_list.append(sum_commit)
    return sum_commit_list

def run(repo):

    # ------------
    # --- fig2 ---
    # ------------

    sum_commits    = repo.git.rev_list('--count', 'HEAD') # コミットの総数
    # コミット履歴を取得
    committed_datetimes = [] # コミットした日付リスト
    for commit in repo.iter_commits():
        committed_datetimes.append(commit.committed_datetime.strftime('%Y-%m-%d'))

    dayslist = get_dayslist(committed_datetimes, sum_commits) # 日付差の日数を算出
    sum_commit_list = get_sum_commit_list(committed_datetimes, dayslist) # コミットの合計値を日付順で計算

    # ------------
    # --- fig1 ---
    # ------------

    year_days = calc_days() # 現在の年の日数
    year_dayslist = get_year_dayslist() # 現在の年の日付リスト
    committed_year = {} # 現在の年の日ごとコミット数
    mcp = get_month_change_point(year_dayslist) # 月が変わった(week+0.5)を取得

    # コミットデータを作成
    set_commit_calendar(year_days, year_dayslist, committed_year, committed_datetimes)
    
    # ------------
    # --- plot ---
    # ------------

    # --- fig1 ---

    # CSV読み込み
    df1 = pd.read_csv("./log/commit_calendar.csv",sep=",")
    df1.columns = ['year','month','month_en','day','dow_no','dow', 'week', 'commit']
    df1 = df1.pivot('dow_no','week','commit')

    fig1, ax1 = plt.subplots(figsize=(10, 3)) # 10対3のプロットを作成

    sns.heatmap(
        df1, 
        cmap="Greens", 
        linewidths=.25, 
        square=True, 
        cbar=False)

    ax1.set_title(str(get_year()) + " year (" + repo.git.rev_list('--count', 'HEAD') + " commit)")
    ax1.set_xlabel('')
    ax1.set_ylabel('')
    ax1.set_yticks([1.5, 3.5, 5.5])
    ax1.set_yticklabels(['Mon', 'Wed', 'Fri'], rotation=0)
    ax1.set_xticks([mcp[0], mcp[1], mcp[2], mcp[3], mcp[4], mcp[5], mcp[6], mcp[7], mcp[8], mcp[9], mcp[10], mcp[11]])
    ax1.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=0)

    fig1.savefig("pic/commit_calendar.png", tight_layout=True) # グラフを画像で保存

    # --- fig2 ---

    fig2, ax2 = plt.subplots(figsize=(10, 5))

    ax2.plot(dayslist, sum_commit_list, linestyle="-.", marker=".", color="forestgreen")
    ax2.grid(b=True, which='major', color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
    ax2.minorticks_on()
    ax2.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.set_title("commit transition")
    ax2.set_xlabel('date')
    ax2.set_ylabel('commits')

    fig2.savefig("pic/commit_transition.png", tight_layout=True)