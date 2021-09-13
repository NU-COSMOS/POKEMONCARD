#-*- codoing:utf-8 -*-

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
            if areas[(turn_cnt+turn)%2].battle[-1].status_effect(areas[(turn_cnt+turn)%2].player_name) == "毒":
                areas[(turn_cnt+turn)%2].battle[-1].change_cur_hp(10) 