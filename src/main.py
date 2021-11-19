import git
import os

import Color

# タイトルを表示
def setTitle():
    print(f"{Color.CYAN} _____              _____ _                 {Color.RESET}")
    print(f"{Color.CYAN}|  _  |___ ___ ___ |     |_|___ ___         {Color.RESET}")
    print(f"{Color.CYAN}|    _|  _| . | . || | | | |   |  _|        {Color.RESET}")
    print(f"{Color.CYAN}|_|\__|___|  _|___||_|_|_|_|_|_|___| for Py {Color.RESET}")
    print(f"{Color.CYAN}          |_|                               {Color.RESET}\n")

def setEnd():
    print(f"\n{Color.CYAN}end{Color.RESET}\n")

# フォルダを削除
def rmtree(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, 0o777)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(top)

# 最初に実行
if __name__ == "__main__":
    path = "project" # レポジトリのパス

    setTitle()

    if os.path.isdir(path):
        rmtree(path) # projectフォルダが存在していれば削除

    print("解析するレポジトリのURLを入力してください")
    boolClone = True
    while (boolClone):
        try:
            url = input(">>> ")
            repo = git.Repo.clone_from(url, path) # レポジトリをクローン
            print("レポジトリをクローンしました\n")
            boolClone = False
        except Exception as err:
            print("レポジトリをクローン出来ませんでした\nもう一度、入力してください")

    print("コマンドを入力してください")
    command = input(">>> ")

    if (command == "log"):
        # git log
        for commit in repo.iter_commits():
            print(commit.author, commit.committed_datetime, commit.hexsha)

    setEnd()