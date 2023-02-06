from Korpora import Korpora
from tokenizers.implementations import BertWordPieceTokenizer
import os

class HanbertTest:
    def __init__(self):
        global nsmc
        nsmc = Korpora.load("nsmc", force_download=True)

    def write_lines(self, path, lines):
        with open(path, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(f'{line}\n')
    def exec(self):
        self.write_lines("data/hanbert/train.txt", nsmc.train.get_all_texts())
        self.write_lines("data/hanbert/test.txt", nsmc.test.get_all_texts()) #코랩에서는 data를 content로 사용한다

        wordpiece_tokenizer = BertWordPieceTokenizer(lowercase=False)
        wordpiece_tokenizer.train(
            files=["./data/hanbert/train.txt", "./data/hanbert/test.txt"],
            vocab_size=10000,
        )
        # wordpiece_tokenizer.save_model("/gdrive/My Drive/nlpbook/wordpiece")
        wordpiece_tokenizer.save_model("./save/wordpiece")

if __name__ == '__main__':
    HanbertTest().exec()