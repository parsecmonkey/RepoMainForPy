# main

import color
import cmd_seek
import cmd_clone
import repo

# タイトルを表示
def set_title():
    print(f"{color.CYAN} _____              _____ _                 {color.RESET}")
    print(f"{color.CYAN}|  _  |___ ___ ___ |     |_|___ ___         {color.RESET}")
    print(f"{color.CYAN}|    _|  _| . | . || | | | |   |  _|        {color.RESET}")
    print(f"{color.CYAN}|_|\__|___|  _|___||_|_|_|_|_|_|___| for Py {color.RESET}")
    print(f"{color.CYAN}          |_|                               {color.RESET}\n")

def set_end():
    print(f"\n{color.CYAN}end{color.RESET}\n")

def main():

    set_title()

    cmd_clone.run(0) # レポジトリをクローン

    cmd_flag = True
    while (cmd_flag):
        print("コマンドを入力してください")
        in_cmd = input(">>> ")
        cmd_flag = cmd_seek.run(repo.get_repo(), in_cmd)

    set_end()

# 最初に実行
if __name__ == "__main__":
    main()