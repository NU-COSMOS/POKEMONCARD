#-*- coding:utf-8 -*-
"""
プレイゾーン
"""


class Area:
    def __init__(self, player):
        self.deck = player.deck  # 山札
        self.player_name = player.name  # プレイヤー名
        self.hands = []  # 手札
        self.battle = []  # バトル場, Monsterインスタンスのリスト
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

    def set_hands(self, n = 5):
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
                if hand.card_type == 'Monster' and hand.before == 'たね':
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
        試合開始時に手札からバトル場にポケモンを出す
        """
        while(1):
            self.show_hands()
            
            num = int(input("バトル場に出すカードの番号を入力してください；"))

            if self.hands[num].card_type == 'Monster' and self.hands[num].before == 'たね':
                break

            print("そのカードは選択できません")

        self.battle.append(self.hands.pop(num))

    def set_bench(self):
        """
        手札からベンチにポケモンを出す
        """
        while(1):
            choice = input('ベンチにポケモンを出しますか？(y/n)：')
            if choice == 'y':
                # 手札を表示
                self.show_hands()

                num = int(input("ベンチに出すカードの番号を入力してください；"))

                if self.hands[num].card_type == 'Monster' and self.hands[num].before == 'たね':
                    self.bench.append([self.hands.pop(num)])
                else:
                    print("そのカードはベンチにおけません")

            else:
                break

    def draw_side(self, n):
        """
        サイドをn枚引いて手札に加える
        """
        for _n in range(n):
            if len(self.sides) != 0:
                self.hands.append(self.sides.pop(0))

    def battle2trash(self):
        """
        バトル場にいるポケモンをトラッシュに送る
        """
        for card in self.battle:
            # ついているエネルギーカードをトラッシュへ
            if len(card.has_energy) != 0:
                for _e in range(len(card.has_energy)):
                    self.trash.append(card.has_energy.pop(0))

            # ついているアイテムカードをトラッシュへ
            if len(card.has_item) != 0:
                for _i in range(len(card.has_item)):
                    self.trash.append(card.has_item.pop(0))

            # 状態異常と体力を初期化
            card.cur_hp = card.max_hp
            card.status = []

        # モンスターカードをトラッシュへ
        for _b in range(len(self.battle)):
            self.trash.append(self.battle.pop(0))

    def bench2battle(self):
        """
        ベンチポケモンをバトル場に出す
        """
        print("ベンチポケモン一覧")
        for b in range(len(self.bench)):
            print(f'{b}：{self.bench[b][-1].name}')

        num = int(input("バトル場に出すベンチポケモンの番号："))

        self.battle = self.bench.pop(num)

    def show(self):
        """
        場の状況を表示
        """
        print(f'\n{self.player_name}のエリア')
        print('バトル場')
        self.battle[-1].show()
        print('ベンチ：')
        for b in self.bench:
            b[-1].show()
        print(f'残り山札枚数：{self.deck.remain()}')
        print(f'残りサイド枚数：{len(self.sides)}')
        print('手札')
        for hand in self.hands:
            print(hand.name)
