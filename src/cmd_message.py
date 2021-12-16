import MeCab
from wordcloud import WordCloud
import collections


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

    # commit message を取得
    TEXT = ""
    for commit in repo.iter_commits():
        TEXT += commit.message

    # 形態素解析
    mecab_all = mecab(TEXT)  # 形態素解析

    part_of_speech = {"名詞"}  # 出力する品詞リスト

    # 出力する品詞リストに含まれる形態素のみ抽出
    mecab_only_noun = []
    for feature in mecab_all:
        if feature[1] in part_of_speech:
            mecab_only_noun.append(feature[0])

    #### パラメータ ####
    STOP_WORDS = ["　"]  # ストップワード
    MAX_WORDS = 2000  # 出力個数の上限
    WIDTH = 500  # 出力画像の幅
    HEIGHT = 500  # 出力画像の高さ
    FONT_FILE = "data/ipaexg.ttf"  # フォントファイルのパス

    wakati = " ".join(mecab_only_noun)  # 分かち書き

    wordCloudGenerator = WordCloudGenerator(font_path=FONT_FILE, background_color="white", width=WIDTH, height=HEIGHT, collocations=False,
                                            stopwords=STOP_WORDS, max_words=MAX_WORDS, regexp=r"[\w']+")  # WordCloud初期化
    wordCloudGenerator.out_file_name = OUT_FILE_NAME  # 出力ファイル名
    wordCloudGenerator.wordcloud_draw(wakati)  # 出力

    print(f"{OUT_FILE_NAME}に画像を出力しました")
    print()


if __name__ == "__main__":
    # 入力テキストファイル
    OUT_FILE_NAME = "pic/wordcloud_message.png"

    TEXT = "吾輩は吾輩である．名前はスーパー吾輩である．Yes, I am wagahai."

    mecab_all = mecab(TEXT)  # 形態素解析

    # 出力する品詞リスト
    part_of_speech = {"名詞"}

    mecab_only_noun = []
    for feature in mecab_all:
        if feature[1] in part_of_speech:
            mecab_only_noun.append(feature[0])
    print(mecab_only_noun)

    #### パラメータ ####
    STOP_WORDS = ["　"]  # ストップワード
    MAX_WORDS = 2000  # 出力個数の上限
    WIDTH = 500  # 出力画像の幅
    HEIGHT = 500  # 出力画像の高さ
    FONT_FILE = "data/ipaexg.ttf"  # フォントファイルのパス

    # wakati = mecab_wakati(TEXT)  # 分かち書き
    wakati = " ".join(mecab_only_noun)  # 分かち書き

    wordCloudGenerator = WordCloudGenerator(font_path=FONT_FILE, background_color="white", width=WIDTH, height=HEIGHT, collocations=False,
                                            stopwords=STOP_WORDS, max_words=MAX_WORDS, regexp=r"[\w']+")  # WordCloud初期化
    wordCloudGenerator.out_file_name = OUT_FILE_NAME  # 出力ファイル名
    wordCloudGenerator.wordcloud_draw(wakati)  # 出力
