#-*- coding:utf-8 -*-
"""
計算
"""

from card import Monster

class Calculation:
    """
    カード
    """

    @staticmethod
    def damage_cal_coin(trial_num, base_damage, add_damage):

        heads_tails_list, heads_num = Monster.coin_toss(trial_num)

        if trial_num == 'I':
            print("コインを裏が出るまで投げ,",add_damage,"×表の数 追加ダメージを与えます")
        else: 
            print("コインを",trial_num,"回投げ,",add_damage,"×表の数 追加ダメージを与えます")              

        # 表裏の結果を表示
        print(heads_tails_list)                           
        print("表の数は",heads_num,"回")

        # 合計ダメージ
        damage = base_damage + add_damage*heads_num

        return damage            