#-*- coding:utf-8 -*-
"""
データ編集インタフェース
"""
from deck import Deck
from data_manager import Data

def main():
    content = int(input("1:カードデータ, 2:デッキ\n編集内容を選択してください："))

    if content == 1:
        operation = int(input("1:登録, 2:修正, 3:削除, 4:閲覧"))
        path = input("カードデータファイルのパスを入力してください：")
        if operation == 1:
            Data.regist(path)

        elif operation == 2:
            Data.update(path)

        elif operation == 3:
            Data.delete(path)

        elif operation == 4:
            Data.show(path)    

        else:
            print("終了します")
            exit(1)

    elif content == 2:
        operation = int(input("1:登録"))
        if operation == 1:
            path = input("カードデータファイルのパスを入力してください：")
            Deck.regist(path)

        else:
            print("終了します")
            exit(1)

if __name__ == "__main__":
    main()