#-*- coding:utf-8 -*-
"""
プレイゾーン
"""


class Area:
    def __init__(self, player):
        self.deck = player.deck  # 山札
        self.player_name = player.name  # プレイヤー名
        self.hands = []  # 手札
        self.fight = []  # バトル場, Monsterインスタンスのリスト
        self.bench = []  # ベンチ, Monsterインスタンスのリスト
        self.trash = []  # トラッシュ
        self.max_sides = player.deck.remain() // 10  # サイドにおける枚数
        self.sides = []  # サイド
        # self.studium = []  # スタジアムカード置き場

    def draw(self, n):
        """
        デッキからカードをn枚引いて手札に加える
        """
        for _n in range(n):
            self.hands.append(self.deck.pop(0))
        print(f"カードを{n}枚手札に加えました")
        
