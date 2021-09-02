#-*- coding:utf-8 -*-
import json
import random
import os
import pickle

from card import *


def dic2instance(dic):
    """
    辞書型で保存されたカードをカードインスタンスに変換
    """
    if dic['card_type'] == 'Monster':
        return Monster(dic)

    elif dic['card_type'] == 'Energy':
        return Energy(dic)


class Deck:
    def __init__(self, path):
        # デッキ読み込み
        # デッキは中身がカードインスタンスのリスト形式で与えられる
        self.deck = []
        with open(path, 'rb') as f:
            load_deck = pickle.load(f)
        for card in load_deck:
            self.deck.append(dic2instance(card))            

    def shuffle(self):
        """
        山札をシャッフル
        """
        random.shuffle(self.deck)

    def pick(self, n):
        """
        山札からカードをn枚引く
        """
        # 引いたカードを格納するリスト
        drawn = []

        # n枚引く
        for _i in range(n):
            drawn.append(self.deck.pop(0))

        print(f'カードを{n}枚引きました')

        return drawn

    def back(self, cards):
        """
        カードを山札に戻す
        cards:戻すカードのリスト
        """
        for card in cards:
            self.deck.append(card)
        self.shuffle()

    def search(self, name):
        """
        特定の名前のカードを引く
        """
        # 引いたカードを格納するリスト
        drawn = []
        for i, card in enumerate(self.deck):
            if card['name'] == name:
                drawn.append(self.deck.pop(i))
                break

        if len(drawn) == 0:
            print('指定されたカードは見つかりませんでした')

        return drawn

    def remain(self):
        """
        山札の残り枚数を返す
        """
        return len(self.deck)

    def pop(self, n):
        return self.deck.pop(n)

    def extend(self, list):
        self.deck.extend(list)

    def append(self, list):
        self.deck.append(list)

    def can_draw(self):
        """
        山札にカードが残っているかを確認
        """
        return self.remain() > 0

    @staticmethod
    def regist(cards_path):
        """
        デッキの登録
        """
        # カードデータが存在するか確認
        if not os.path.isfile(cards_path):
            print("カードデータが見つかりませんでした")
            print("終了します")
            exit(1)

        # カードデータの読み込み
        with open(cards_path, 'r') as f:
            cards = json.load(f)

        num = int(input("デッキ枚数を入力してください(10の倍数のみ)"))

        # デッキ格納リスト
        deck = []

        # デッキ情報
        for _n in range(num):
            id = int(input("デッキに入れるカードのmain_idを入力してください："))
            deck.append(cards['cards'][id])

        # 登録したデッキの確認
        print("デッキ内容：")
        for card in deck:
            print(card['name'])

        deck_name = input("デッキ名：")
        with open('../' + deck_name + '.pkl', 'wb') as f:
            pickle.dump(deck, f)