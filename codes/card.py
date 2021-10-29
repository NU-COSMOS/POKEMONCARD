#-*- coding:utf-8 -*-
"""
カードの定義
"""
import random

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
    def __init__(self, dic):
        super().__init__(dic['name'], dic['card_type'], dic['img'], dic['main_id'], dic['sub_id'])
        self.cur_hp = dic['hp']  # 現在の体力
        self.max_hp = dic['hp']  # 体力の最大値
        self.types = dic['types']  # タイプのlist
        # self.chara = chara  # 特性名
        self.skills = dic['skills']  # 技のlist
        self.weaks = dic['weaks']  # 弱点属性のlist
        self.resists = dic['resists']  # 抵抗属性のlist
        self.escape = dic['escape']  # 逃げるのに必要なエネルギーカードのlist
        self.before = dic['before']  # 進化前のポケモン名
        self.status = []  # 状態異常
        self.has_energy = []  # ついているエネルギーカード
        self.has_item = []  # 持たせた道具

    def initialize(self):
        """
        モンスターの状態を初期化する
        進化時の進化前やトラッシュに送られる時に使用されることを想定
        """
        self.cur_hp = self.max_hp
        self.status = []
        self.has_energy = []
        self.has_item = []

    @staticmethod
    def coin_toss(trial_num):
        # ランダムにコインの表裏を出力
        heads_tails_list   = []
        random_sample      = ["表","裏"]
        if trial_num == 'I':
            while(1):
                random_num = "".join(random.sample(random_sample,1))
                heads_tails_list.append(random_num)
                if random_num == "裏":
                    break
        else: 
            for i in range(int(trial_num)):
                random_num = "".join(random.sample(random_sample,1))
                heads_tails_list.append(random_num)   

        # 表の数
        heads_num = heads_tails_list.count("表") 

        return heads_tails_list, heads_num  

    def change_cur_hp(self, damage):
        """
        体力を変化させる
        """
        # 瀕死の時
        if self.cur_hp - damage <= 0:
            self.cur_hp = 0

        # 体力上限の時
        elif self.cur_hp - damage > self.max_hp:
            self.cur_hp = self.max_hp

        else:
            self.cur_hp -= damage

        if damage >= 0:
            print(damage,"ダメージ!" ) 
        elif damage < 0:
            print(damage,"回復!")      

    def change_status(self, status):
        """
        状態を変化させる
        """
        if status == 'None':
            self.status = []
        elif '回復' in status:
            recovery_status = status.replace('回復', '')
            self.status.remove(recovery_status)
            print(self.name,'は',recovery_status,'から回復した')
        else:
            self.status.append(status)

        self.status = list(set(self.status)) 

    def status_effect(self, player_name):
        """
        特殊状態による効果
        """    
        if self.status != []:
            if "毒" in self.status:    
                print(player_name,"の",self.name,"は毒のダメージを受けている")
            if "やけど" in self.status:
                print(player_name,"の",self.name,"はやけどのダメージを受けている")
            #if "ねむり" in self.status:
#            if "まひ" in self.status: 
#            if "こんらん" in self.status:

            return self.status
            
                             
    def show(self):
        """
        モンスターの状態を表示
        """
        s = ','.join(self.status)
        print(f'{self.name}({self.cur_hp}/{self.max_hp}) 状態異常：{s}')





class Accessory(Card):
    """
    ポケモンに持たせることができる道具
    """
    def __init__(self, dic):
        super().__init__(dic['name'], dic['card_type'], dic['img'], dic['main_id'], dic['sub_id'])


class Energy(Card):
    """
    エネルギーカード
    """
    def __init__(self, dic):
        super().__init__(dic['name'], dic['card_type'], dic['img'], dic['main_id'], dic['sub_id'])
        self.color = dic['color']  # エネルギーの色


class Support(Card):
    """
    サポートカード
    """
    def __init__(self, dic):
        super().__init__(dic['name'], dic['card_type'], dic['img'], dic['main_id'], dic['sub_id'])


class Goods(Card):
    """
    グッズカード
    """
    def __init__(self, dic):
        super().__init__(dic['name'], dic['card_type'], dic['img'], dic['main_id'], dic['sub_id'])


class Stadium(Card):
    """
    スタジアムカード
    """
    def __init__(self, dic):
        super().__init__(dic['name'], dic['card_type'], dic['img'], dic['main_id'], dic['sub_id'])