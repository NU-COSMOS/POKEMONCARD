#-*- codoing:utf-8 -*-

from card import Monster

class Check:
    """
    モンスターの状態をチェック
    """
    @staticmethod
    def pokemon_check(areas, turn_cnt):
        """
        特殊状態のポケモンをチェック
        """
        for turn in range(2):
            status = areas[(turn_cnt+turn)%2].battle[-1].status_effect(areas[(turn_cnt+turn)%2].player_name)
            if status != None:
                if "毒" in status:
                    areas[(turn_cnt+turn)%2].battle[-1].change_cur_hp(10) 
                if "やけど" in status:
                    areas[(turn_cnt+turn)%2].battle[-1].change_cur_hp(20)
                    heads_tails_list,heads_num = Monster.coin_toss(1)
                    if heads_num == 1:
                        areas[(turn_cnt+turn)%2].battle[-1].change_status("やけど回復")
                if "ねむり" in status:
                    heads_tails_list,heads_num = Monster.coin_toss(1)
                    if heads_num == 1:
                        areas[(turn_cnt+turn)%2].battle[-1].change_status("眠り回復")                            
