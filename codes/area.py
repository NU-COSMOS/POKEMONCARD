#-*- coding:utf-8 -*-
"""
プレイゾーン
"""
import numpy as np
import cv2
from PIL import Image


def pil2cv(image):
    ''' PIL型 -> OpenCV型 '''
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image


class Area:
    back_h = 500  # 背景画像高さ
    back_w = 740  # 背景画像幅
    card_h = 140  # カード画像高さ
    card_w = 100  # カード画像幅
    battle_x = (back_w // 2) - (card_w // 2)  # バトル場の左上x座標
    battle_y = 30  # バトル場の左上y座標
    bench_x = 140  # ベンチ一番左の左上x座標
    bench_y = 340  # ベンチ一番左の左上x座標

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
        self.area_img = np.full((Area.back_h, Area.back_w, 3), 255.0).astype(np.uint8)  # プレイエリアの画像背景

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
            for n, card in enumerate(self.hands):
                print(f'{n}:{card.name}')
            
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
            if len(self.bench) >= 5:
                print('これ以上ベンチにポケモンを出せません')
                break
            
            choice = input('ベンチにポケモンを出しますか？(y/n)：')
            if choice == 'y':
                for n, card in enumerate(self.hands):
                    print(f'{n}:{card.name}')

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

    def get_img(self):
        """
        場の画像を画像で表示
        cv2は日本語対応してないためpilで開いてからcv2に変換
        """
        # バトル場のポケモン画像
        if len(self.battle) != 0:
            battle_img = Image.open(self.battle[-1].img)
            battle_img = pil2cv(battle_img)
            battle_img = cv2.resize(battle_img, (Area.card_w, Area.card_h))
            self.area_img[Area.battle_y:Area.battle_y+Area.card_h, 
                        Area.battle_x:Area.battle_x+Area.card_w] = battle_img

        # ベンチポケモンの画像
        if len(self.bench) != 0:
            for i, b in enumerate(self.bench):
                bench_img = Image.open(b[-1].img)
                bench_img = pil2cv(bench_img)
                bench_img = cv2.resize(bench_img, (Area.card_w, Area.card_h))
                print()
                self.area_img[Area.bench_y:Area.bench_y+Area.card_h, 
                              Area.bench_x*(i+1)+(i*10):Area.bench_x*(i+1)+(i*10)+Area.card_w] = bench_img

        return self.area_img

        
