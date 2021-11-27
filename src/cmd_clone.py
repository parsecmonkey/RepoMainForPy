# clone

import os
import re

import repo

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

def run(i):
    root_path = "project" # レポジトリのパス

    print("解析するレポジトリのURLを入力してください")
    url = input(">>> ")

    # 最初だけ確認
    if os.path.isdir(root_path):
        if i == 0:
            rmtree(root_path) # projectフォルダが存在していれば削除

    bool_clone = True
    while (bool_clone):
        try:
            # "://"でURLか判定
            if url.find("://"):
                file_name = url[url.rfind('/') + 1:] # 一番後ろのファイル名を抽出

            path = root_path + "/" + file_name # project/..

            repo.clone_repo(url, path) # レポジトリをクローン
            print("レポジトリをクローンしました\n")
            bool_clone = False
        except Exception as err:
            if os.path.isdir(path):
                print("すでにクローン済みです\n")
                bool_clone = False
            else:
                print("レポジトリをクローン出来ませんでした\nもう一度、入力してください")
                url = input(">>> ")