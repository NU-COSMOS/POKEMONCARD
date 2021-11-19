#-*- codoing:utf-8 -*-

from card import Monster
from skill_effect import Calculation
from skill_effect import Target

class Action:
    """
    エリアの状態を変化させる行動
    """
    @staticmethod
    def attack(areas, turn_cnt):
        """
        バトルポケモンの技を使用する
        """
        # カードの持っている技を表示
        for n, skill in enumerate(areas[turn_cnt%2].battle[-1].skills):
            print(f"{n}：{skill['name']}")
        skill_num = int(input("使用する技の番号を入力してください："))

        areas = Action.activate(areas[turn_cnt%2].battle[-1].skills[skill_num]['name'], 
                                areas[turn_cnt%2].battle[-1].skills[skill_num]['block'], 
                                areas, turn_cnt)

        return areas

    @staticmethod
    def activate(name, blocks, areas, turn_cnt):
        """
        スキルを発動させる
        """
        print(f'{name}を使用')

        for block in blocks:
            areas = Action.execute(block, areas, turn_cnt)

        return areas

    @staticmethod
    def execute(block, areas, turn_cnt):
        """
        スキルの効果を実行する
        """
        # ポケモンの体力を変化させる
        if block['block type'] == 'damage':
            if block['damage type'] == 'normal':
                damage = block['damage']       
            elif block['damage type'] == 'coin':
                damage = Calculation.damage_cal_coin(block['trial_num'], block['base damage'], block['add damage']) 

            # 対象となるポケモンに技の効果を発揮する
            if block['target'] == 'battle_opponent':           
                areas[(turn_cnt+1)%2].battle[-1].change_cur_hp(damage, turn_cnt)
            elif block['target'] == 'battle_self': 
                areas[(turn_cnt)%2].battle[-1].change_cur_hp(damage, turn_cnt)
            elif block['target'] == 'bench_opponent':
                target = Target.target(block,areas,turn_cnt) 
                areas[(turn_cnt+1)%2].bench[target][-1].change_cur_hp(damage, turn_cnt) 
            elif block['target'] == 'bench_self':
                target = Target.target(block,areas,turn_cnt) 
                areas[(turn_cnt)%2].bench[target][-1].change_cur_hp(damage, turn_cnt) 

        # 相手のバトルポケモンに状態異常を付与する
        elif block['block type'] == 'status':
            areas[(turn_cnt+1)%2].battle[-1].change_status(block['status'])

        return areas
    
    @staticmethod
    def set_bench(areas, turn_cnt):
        """
        手札からベンチに種ポケモンを出す
        """
        areas[turn_cnt%2].set_bench()

        return areas

    @staticmethod
    def set_energy(areas, turn_cnt):
        """
        手札のエネルギーカードを場のポケモンにつける
        """
        flag = areas[turn_cnt%2].set_energy()

        return flag, areas

    @staticmethod
    def evolve(areas, turn_cnt):
        """
        場のポケモンを進化させる
        """
        areas[turn_cnt%2].evolve()

        return areas
