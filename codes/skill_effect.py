#-*- coding:utf-8 -*-
"""
技の特殊効果
"""

from card import Monster

class Calculation:
    """
    特殊ダメージ
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

class Target:
    """
    攻撃対象
    """   

    @staticmethod
    def target(block,areas,turn_cnt):

        if block['target'] == 'bench_opponent':
            print("相手のベンチポケモン一覧")
        elif block['target'] == 'bench_self':   
            print("自分のベンチポケモン一覧") 
            turn_cnt = turn_cnt + 1

        for b in range(len(areas[(turn_cnt+1)%2].bench)):
            print(f'{b}：{areas[(turn_cnt+1)%2].bench[b][-1].name}')

        target = int(input("攻撃するベンチポケモンの番号を入力してください："))  

        return target  