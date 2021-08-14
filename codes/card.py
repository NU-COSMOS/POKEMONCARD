#-*- coding:utf-8 -*-
"""
カードの定義
"""


class Card:
    """
    カード
    """
    def __init__(self, name, card_type, img, main_id, sub_id):
        self.name = name  # カード名
        self.card_type = card_type  # カードの種類(モンスター, トレーナーetc)
        self.img = img  # カードイラストのパス
        self.main_id = main_id  # すべてのカードごとに異なるid
        self.sub_id = sub_id  # 違うカードだが同一として扱うためのid


class Monster(Card):
    """
    モンスター
    """
    def __init__(self, name, card_type,
                 img, cur_hp, max_hp, types, 
                 chara, skills, weaks, 
                 resists, escape, before, 
                 main_id, sub_id, status = None):
        super().__init__(name, card_type, img, main_id, sub_id)
        self.cur_hp = cur_hp  # 現在の体力
        self.max_hp = max_hp  # 体力の最大値
        self.types = types  # タイプのlist
        self.chara = chara  # 特性名
        self.skills = skills  # 技のlist
        self.weaks = weaks  # 弱点属性のlist
        self.resists = resists  # 抵抗属性のlist
        self.escape = escape  # 逃げるのに必要なエネルギーカード
        self.before = before  # 進化前のポケモンのsub_id
        self.status = status  # 状態異常
        self.has_energy = []  # ついているエネルギーカード
        self.has_item = []  # 持たせた道具


class Accessory(Card):
    """
    ポケモンに持たせることができる道具
    """
    def __init__(self, name, card_type, img, main_id, sub_id):
        super().__init__(name, card_type, img, main_id, sub_id)


class Energy(Card):
    """
    エネルギーカード
    """
    def __init__(self, name, card_type, img, main_id, sub_id, color):
        super().__init__(name, card_type, img, main_id, sub_id)
        self.color = color  # エネルギーの色


class Trainer(Card):
    """
    トレーナーカード
    """
    def __init__(self, name, card_type, img, main_id, sub_id):
        super().__init__(name, card_type, img, main_id, sub_id)


class Field(Card):
    """
    フィールドカード
    """
    def __init__(self, name, card_type, img, main_id, sub_id):
        super().__init__(name, card_type, img, main_id, sub_id)