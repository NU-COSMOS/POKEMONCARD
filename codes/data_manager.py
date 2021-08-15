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

    def common(self, card):
        """
        共通項目
        """
        res = []
        # カード名のチェック
        # カード名が文字列かどうかチェック
        res.append(type(card["name"]) == str)

        # カードタイプが存在するものかどうかチェック
        res.append(card["card_type"] in self.card_types)

        # イラストが存在するかチェック
        res.append(os.path.isfile(card["img"]))

        return all(res)

    def monster(card):
        """
        モンスター
        """

    def trainer(card):
        """
        トレーナー
        """

    def accessory(card):
        """
        持ち物
        """

    def energy(card):
        """
        エネルギーカード
        """

    def field(card):
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