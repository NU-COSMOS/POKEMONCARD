#-*- coding:utf-8 -*-
"""
カード情報の管理
"""


class Data:
    def regist():
        """
        新しいカードデータを登録
        """
        # 新しいカードを辞書型で登録
        new_card = {}

        # 共通項目を入力
        new_card["name"] = input("カード名を入力してください：")
        new_card["card_type"] = input("カードの種類(Monster, Trainer, Accessory, Energy, Field)：")
        new_card["img"] = input("カードイラストのパス：")


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