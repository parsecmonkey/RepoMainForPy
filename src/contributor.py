# contributor

# コントリビュータクラス
class Contributor:
    def __init__(self, name, commit_count):
        self.name = name
        self.commit_count = commit_count

    # 情報のprint結果を定義
    def __repr__(self):
        return "name: " + str(self.name) + " commit: " + str(self.commit_count)

    # nameを更新
    def set_name(self, name):
        self.name = name
    
    # commit_countを更新
    def set_commit_count(self, commit_count):
        self.commit_count = commit_count

    # nameを取得
    def get_name(self):
        return self.name

    # commit_countを取得
    def get_commit_count(self):
        return self.commit_count

    # commit_countにnumを足す
    def add_commit_count(self, num):
        self.commit_count += num