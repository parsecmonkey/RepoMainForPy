# コマンド処理

def search(repo, cmd):
    # log
    if (cmd == "log"):
        for commit in repo.iter_commits():
            print(commit.author, commit.committed_datetime, commit.hexsha)
        return True

    # 終了
    elif (cmd == "exit()" or cmd == "exit"):
        return False

    # 例外
    else:
        print("そのコマンドは使用できません")
        return True
