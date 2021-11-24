# コマンド処理

import cmd_log
import cmd_help

def search(repo, cmd):
    # help
    if (cmd == "help"):
        cmd_help.run()
        return True

    # log
    elif (cmd == "log"):
        cmd_log.run(repo)
        return True

    # exit
    elif (cmd == "exit()" or cmd == "exit"):
        return False

    # 例外
    else:
        print("そのコマンドは使用できません")
        return True