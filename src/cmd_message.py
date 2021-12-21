import MeCab
from wordcloud import WordCloud
import collections
import csv as c


def mecab_wakati(text):
    # 形態素解析を行う(分かち書き)
    wakati_tagger = MeCab.Tagger("-Owakati")  # 分かち書き
    parse = wakati_tagger.parse(text)
    return parse


def mecab(text):
    # 形態素解析を行い品詞リストを返す
    tagger = MeCab.Tagger()
    tagger.parse("")
    node = tagger.parseToNode(text)

    node_list = []
    while node:
        # 例: ['吾輩', '名詞', '代名詞', '一般', '*', '*', '*', '吾輩', 'ワガハイ', 'ワガハイ']
        node_list.append([node.surface]+node.feature.split(","))
        node = node.next
    node_list = node_list[1:-1]  # BOS/EOSタグを除外

    return node_list


# キーワード解析
def keyword_analy(text):
    key_out = []
    key_list = ["ように", "修正", "追加", "削除", "作成", "変更", "編集", "更新", "整理", "調整"]
    for key in key_list:
        if key in text:
            key_out.append(key)

    return key_out


class WordCloudGenerator:
    """
    WordCloud
    """
    out_file_name = ""

    def __init__(self, font_path, background_color, width, height, collocations,
                 stopwords, max_words, regexp):
        """
        出力パラメータ初期化
        """
        self.font_path = font_path
        self.background_color = background_color
        self.width = width
        self.height = height
        self.collocations = collocations
        self.stopwords = stopwords
        self.max_words = max_words
        self.regexp = regexp

    def wordcloud_draw(self, parse):
        """
        wordcloud画像を出力
        @param
            parse 形態素解析結果
        """
        self.wordcloud = WordCloud(font_path=self.font_path, background_color=self.background_color, width=self.width, height=self.height,
                                   collocations=self.collocations, stopwords=self.stopwords, max_words=self.max_words, regexp=self.regexp, repeat=False)
        self.wordcloud.generate(parse)
        self.wordcloud.to_file(self.out_file_name)

    def frequency_count(self, wakati_text):
        """
        単語の頻出頻度算出
        @param 
            wakati_text str 分かち書きテキスト
        """
        words = wakati_text.split(" ")
        words = [word for word in words if word not in self.stopwords]
        word_freq = collections.Counter(words)
        return word_freq


def run(repo):
    # 入力テキストファイル
    OUT_FILE_NAME = "pic/wordcloud_message.png"
    # message.csv
    f = open("./log/message.csv","w+", encoding="utf_8_sig", newline='')
    csv = c.writer(f)
    # csvヘッダー追加
    csv.writerow([
        'commit_no',
        'message',
        'key_flag',
        'keyword',
        'marp_flag'
        'morpheme'])

    sum_commits    = repo.git.rev_list('--count', 'HEAD') # コミットの総数
    commit_count   = 0
    # commit message を取得
    TEXT = ""
    for commit in repo.iter_commits():
        commit_no =  int(sum_commits) - commit_count
        keyword  = keyword_analy(commit.message)
        key_flag = len(keyword)
        if key_flag == 0:
            keyword = "none"

        TEXT += commit.message

        # message.csvに書き込み
        csv.writerow([
            commit_no,
            commit.message,
            key_flag,
            keyword,
            0,
            "none"])

        commit_count += 1

    # 形態素解析
    mecab_all = mecab(TEXT)  # 形態素解析

    # 名詞及び名詞連結を取得#
    mecab_linking_noun = []
    for m in range(len(mecab_all)-1):
        if mecab_all[m][1] == "名詞" and mecab_all[m+1][1] == "名詞":
            mecab_linking_noun.append(
                mecab_all[m][0]+mecab_all[m+1][0])
        elif mecab_all[m][1] == "名詞":
            mecab_linking_noun.append(mecab_all[m][0])

    #### パラメータ ####
    STOP_WORDS = ["　"]  # ストップワード
    MAX_WORDS = 2000  # 出力個数の上限
    WIDTH = 500  # 出力画像の幅
    HEIGHT = 500  # 出力画像の高さ
    FONT_FILE = "data/ipaexg.ttf"  # フォントファイルのパス

    wakati = " ".join(mecab_linking_noun)  # 分かち書き

    wordCloudGenerator = WordCloudGenerator(font_path=FONT_FILE, background_color="white", width=WIDTH, height=HEIGHT, collocations=False,
                                            stopwords=STOP_WORDS, max_words=MAX_WORDS, regexp=r"[\w']+")  # WordCloud初期化
    wordCloudGenerator.out_file_name = OUT_FILE_NAME  # 出力ファイル名
    wordCloudGenerator.wordcloud_draw(wakati)  # 出力

    print(f"{OUT_FILE_NAME}に画像を出力しました")
    print()

    f.close()


if __name__ == "__main__":
    # 入力テキストファイル
    OUT_FILE_NAME = "pic/wordcloud_message.png"

    TEXT = "吾輩は吾輩である．名前はスーパー吾輩である．Yes, I am wagahai."

    mecab_all = mecab(TEXT)  # 形態素解析

    # 名詞及び名詞連結を取得#
    mecab_linking_noun = []
    for m in range(len(mecab_all)-1):
        if mecab_all[m][1] == "名詞" and mecab_all[m+1][1] == "名詞":
            mecab_linking_noun.append(
                mecab_all[m][0]+mecab_all[m+1][0])
        elif mecab_all[m][1] == "名詞":
            mecab_linking_noun.append(mecab_all[m][0])
    print(mecab_linking_noun)

    # exit(0)

    #### パラメータ ####
    STOP_WORDS = ["　"]  # ストップワード
    MAX_WORDS = 2000  # 出力個数の上限
    WIDTH = 500  # 出力画像の幅
    HEIGHT = 500  # 出力画像の高さ
    FONT_FILE = "data/ipaexg.ttf"  # フォントファイルのパス

    # wakati = mecab_wakati(TEXT)  # 分かち書き
    wakati = " ".join(mecab_linking_noun)  # 分かち書き

    wordCloudGenerator = WordCloudGenerator(font_path=FONT_FILE, background_color="white", width=WIDTH, height=HEIGHT, collocations=False,
                                            stopwords=STOP_WORDS, max_words=MAX_WORDS, regexp=r"[\w']+")  # WordCloud初期化
    wordCloudGenerator.out_file_name = OUT_FILE_NAME  # 出力ファイル名
    wordCloudGenerator.wordcloud_draw(wakati)  # 出力
