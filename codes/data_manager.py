#-*- coding:utf-8 -*-
"""
カード情報の管理
"""
import os


class Checker:
    """
    各項目の入力内容をチェック
    """
    def __init__(self):
        self.card_types = ["Monster", "Trainer", "Accessory", "Energy", "Field"]
        self.types = ["炎", "水", "電気", "無", "闘", "悪", "鋼", "超", "草", "妖", "竜", "None"]

    def common(self, card):
        """
        共通項目
        """
        res = []
        # カード名が文字列かどうかチェック
        res.append(type(card["name"]) == str)

        # カードタイプが存在するものかどうかチェック
        res.append(card["card_type"] in self.card_types)

        # イラストが存在するかチェック
        res.append(os.path.isfile(card["img"]))

        return all(res)

    def monster(self, card):
        """
        モンスター
        """
        res = []
        # 体力が10の倍数かつ0以下でないか
        res.append(card["hp"] % 10 == 0 and card["hp"] <= 0)

        # タイプに存在するものが入力されているか
        for type in card["types"]:
            res.append(type in self.types)

        # タイプにNoneが含まれていないか
        res.append("None" not in card["types"])

        # 弱点属性に存在するものが入力されているか
        for weak in card["weaks"]:
            res.append(weak in self.types)

        # 弱点属性にNoneが含まれている場合, Noneだけか
        if "None" in card["weaks"]:
            res.append(len(card["weaks"] == 1))

        # 抵抗属性に存在するものが入力されているか
        for resist in card["resists"]:
            res.append(resist in self.types)
        for escape in card["escape"]:
            res.append(escape in self.types)

    def trainer(self, card):
        """
        トレーナー
        """

    def accessory(self, card):
        """
        持ち物
        """

    def energy(self, card):
        """
        エネルギーカード
        """

    def field(self, card):
        """
        フィールドカード
        """


class Data:
    """
    データ操作オブジェクト
    """
    def regist():
        """
        新しいカードデータを登録
        """
        # 新しいカードを辞書型で登録
        new_card = {}

        # 入力内容のチェッカー
        checker = Checker()

        # 共通項目を入力
        while(1):
            new_card["name"] = input("カード名：")
            new_card["card_type"] = input("カードの種類(Monster, Trainer, Accessory, Energy, Field)：")
            new_card["img"] = input("カードイラストのパス：")

            # 入力内容をチェック
            if checker.common(new_card):
                break
            print("入力内容に誤りがあるのでもう一度やり直してください")

        # 各カードタイプごとの情報を入力
        while(1):
            # モンスターカードの入力内容
            if new_card["card_type"] == "Monster":
                new_card["hp"] = int(input("モンスターの体力："))
                print("属性一覧：{}".format(checker.types))
                new_card["types"] = input("モンスターのタイプ(例：炎,水)：").split(",")
                new_card["weaks"] = input("モンスターの弱点属性(例：炎,水)：").split(",")
                new_card["resists"] = input("モンスターの抵抗属性(例：炎,水)：").split(",")
                new_card["escape"] = input("モンスターが逃げるのに必要なエネルギー(例：炎,炎)：").split(",")
                new_card["chara"] = input("特性名：")
                new_card["skills"] = input("技名(例：なきごえ,たいあたり)：").split(",")
                new_card["before"] = input("進化前(たね or ポケモン名)：")

            # 入力内容をチェック
            if checker.monster(new_card):
                break
            print("モンスターの入力内容に誤りがあるのでもう一度やり直してください")

    def delete():
        """
        登録済みのカードデータを削除
        """
    
    def update():
        """
        登録済みのカードデータを変更
        """
    
    def search():
        """
        カードデータの検索
        """

    def show():
        """
        カードデータの閲覧
        """

Data.regist()