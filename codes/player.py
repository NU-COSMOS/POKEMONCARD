#-*- coding:utf-8 -*-
"""
プレイヤークラス
"""


class Player:
    def __init__(self, name, deck):
        self.name = name  # プレイヤー名
        self.deck = deck  # 使用するデッキ