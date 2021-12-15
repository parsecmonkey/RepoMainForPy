# コマンド処理

import cmd_help
import cmd_clone
import cmd_log
import cmd_diff
import cmd_plot
import cmd_message


def search(repo, cmd):
    # help
    if (cmd == "help"):
        cmd_help.run()
        return True

    # clone
    elif (cmd == "clone"):
        cmd_clone.run(1)
        return True

    # log
    elif (cmd == "log"):
        cmd_log.run(repo)
        return True

    # diff
    elif (cmd == "diff"):
        cmd_diff.run(repo)
        return True

    # plot
    elif (cmd == "plot"):
        cmd_plot.run(repo)
        return True

    # message
    elif(cmd == "message"):
        cmd_message.run(repo)
        return True

    # exit
    elif (cmd == "exit()" or cmd == "exit"):
        return False

    # 例外
    else:
        print("そのコマンドは使用できません")
        return True
