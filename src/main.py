import git
import os

import color
import cmd

# タイトルを表示
def setTitle():
    print(f"{color.CYAN} _____              _____ _                 {color.RESET}")
    print(f"{color.CYAN}|  _  |___ ___ ___ |     |_|___ ___         {color.RESET}")
    print(f"{color.CYAN}|    _|  _| . | . || | | | |   |  _|        {color.RESET}")
    print(f"{color.CYAN}|_|\__|___|  _|___||_|_|_|_|_|_|___| for Py {color.RESET}")
    print(f"{color.CYAN}          |_|                               {color.RESET}\n")

def setEnd():
    print(f"\n{color.CYAN}end{color.RESET}\n")

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

def main():
    path = "project" # レポジトリのパス

    setTitle()

    if os.path.isdir(path):
        rmtree(path) # projectフォルダが存在していれば削除

    print("解析するレポジトリのURLを入力してください")
    bool_clone = True
    while (bool_clone):
        try:
            url = input(">>> ")
            repo = git.Repo.clone_from(url, path) # レポジトリをクローン
            print("レポジトリをクローンしました\n")
            bool_clone = False
        except Exception as err:
            print("レポジトリをクローン出来ませんでした\nもう一度、入力してください")

    bool_cmd = True
    while (bool_cmd):
        print("コマンドを入力してください")
        in_cmd = input(">>> ")
        bool_cmd = cmd.search(repo, in_cmd)
        print("\n")

    setEnd()

# 最初に実行
if __name__ == "__main__":
    main()