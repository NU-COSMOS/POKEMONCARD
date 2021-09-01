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

    def set_hands(self, n):
        """
        ゲーム開始時の手札の作成
        たねポケモンが手札に含まれていない場合やり直す
        """
        # たねポケモン存在判別用フラグ
        flag = False

        while(1):
            flag = False
            for _n in range(n):
                self.hands.append(self.deck.pop(0))

            for hand in self.hands:
                if hand['card_type'] == 'Monster' and hand['before'] == 'たね':
                    flag = True

            if flag:
                print('たねポケモンを引くことができました')
                break

            # たねポケモンを引くことができなかった場合
            # 手札をすべて山札に戻してシャッフル
            self.all_back_shuffle()

        print(f"{n}枚の手札で開始します")

    def set_sides(self):
        """
        ゲーム開始時にサイドをセット
        """
        for _n in range(self.max_sides):
            self.sides.append(self.deck.pop(0))
        print(f"{self.max_sides}枚のサイドをセット")

    def all_back_shuffle(self):
        """
        手札をすべて山札に戻し、山札をシャッフル
        """
        # 手札をすべて山札に戻す
        self.deck.extend(self.hands)

        # 山札をシャッフル
        self.deck.shuffle()

    def set_monster(self):
        """
        試合開始時にモンスターを場に出す
        """
        # 手札からバトル場にポケモンを出す
        self.set_battle()
        # 手札からベンチにポケモンを出す
        self.set_bench()

    def set_battle(self):
        """
        手札からバトル場にポケモンを出す
        """

        
