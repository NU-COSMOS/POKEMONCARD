#-*- coding:utf-8 -*-
"""
試合する
"""
import cv2
import numpy as np

from player import Player
from area import Area
from action import Action
from deck import Deck
from check import Check


def load_deck(deck_name):
    """
    デッキデータの読み込み
    """
    return Deck(f"../{deck_name}.pkl")


def create_players():
    """
    プレイヤーインスタンスの生成
    """
    players = []

    for p in range(2):
        name = input(f"プレイヤー{p+1}の名前を入力してください：")
        deck = load_deck(input(f"{name}が使用するデッキ名を入力してください："))
        players.append(Player(name, deck))

    return players


def set_area():
    """
    試合を開始するためにプレイゾーンを設定
    """
    # プレイヤーを用意
    players = create_players()

    areas = []
    # プレイエリアインスタンスの生成
    for player in players:
        areas.append(Area(player))

    # エリアの初期状態を設定
    areas = ready(areas)

    return areas


def ready(areas):
    """
    試合開始の準備を整える
    """
    for area in areas:
        print(f'\n{area.player_name}の番')
        # 手札を用意
        area.set_hands()
        # サイドを用意
        area.set_sides()
        # たねポケモンを場に出す
        area.set_monster()

    return areas


def check_end(areas):
    """
    試合が終了したかどうかを判定
    終了条件
    ・片方のエリアのサイドが0枚
    ・片方のプレイヤーの山札が0枚
    ・片方のバトル場にポケモンがいない
    """
    for area in areas:
        # 山札の残り枚数が0枚
        if not area.deck.can_draw():
            print("山札がなくなりました")
            return True

        # 残りサイド枚数が0枚
        if len(area.sides) == 0:
            print("サイドをすべてとりました")
            return True

        if len(area.battle) == 0:
            print("バトル場に出せるポケモンがいませんでした")
            return True

    return False

def turn(areas, turn_cnt):
    """
    手番
    """
    print(f"\n{turn_cnt+1}ターン目")
    print(f"{areas[turn_cnt%2].player_name}のターンです")

    # ターン開始時にはカードを1枚引く
    areas[turn_cnt%2].draw(1)

    # 行動フラグ
    # 手番に一度しか行えない行動を管理
    energy_flag = False

    while(1):
        act = int(input("行動を選択して下さい\
                        \n1:攻撃 \
                        \n2:手札からたねポケモンを場に出す \
                        \n3:エネルギーカードをつける \
                        \n4:ポケモンを進化させる \
                        \n5:終了 \
                        \n"))
        
        # 攻撃技を使用
        if act == 1:
            areas = Action.attack(areas, turn_cnt)
            # 技を使用したらターン終了
            break

        # 手札から種ポケモンを場に出す
        elif act == 2:
            areas = Action.set_bench(areas, turn_cnt)

        # 手札からエネルギーカードを場のポケモンにつける
        # 自分のターンに一回しか使用不可
        elif act == 3:
            if energy_flag:
                print('その行動はもう行いました')

            else:
                energy_flag, areas = Action.set_energy(areas, turn_cnt)

        # 場のポケモンを進化させる
        elif act == 4:
            areas = Action.evolve(areas, turn_cnt)

        # ターン終了
        elif act == 5:
            break

    # ターン終了時の処理
    areas = end(areas, turn_cnt)

    return areas


def end(areas, turn_cnt):
    """
    ターン終了時の処理
    """

    #ポケモンチェック
    Check.pokemon_check(areas, turn_cnt)

    # 相手のバトルポケモンを瀕死にさせた場合
    if areas[(turn_cnt+1)%2].battle[-1].cur_hp <= 0:

        # 自分はサイドを1枚引く
        areas[turn_cnt%2].draw_side(1)

        # 相手はバトル場のポケモンをトラッシュに移す
        areas[(turn_cnt+1)%2].battle2trash()

        # 相手はベンチポケモン1体をバトル場に移す
        if len(areas[(turn_cnt+1)%2].bench) != 0:
            areas[(turn_cnt+1)%2].bench2battle()

    return areas


def show(areas):
    """
    場の状況を表示
    """
    all_area = np.concatenate([np.rot90(areas[0].get_img(), 3), np.rot90(areas[1].get_img(), 1)], axis = 1)
    cv2.imshow('Field', all_area)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def progress(areas):
    """
    各プレイヤーが交互に手番を行う
    """
    turn_cnt = 0
    while(1):
        # プレイヤーの手番
        areas = turn(areas, turn_cnt)

        # 場の状況を表示
        show(areas)

        # 試合終了判定
        if check_end(areas):
            print("試合終了")
            break

        turn_cnt += 1

    return areas


def judge(areas):
    """
    勝敗の判定
    """
    winner = check_winner(areas)
    print(winner, "の勝利!")


def check_winner(areas):
    """
    勝者を調べる
    """
    for a in range(len(areas)):
        # 山札がない場合, 相手の勝利
        if not areas[a].deck.can_draw():
            return areas[a+1].player_name

        # サイドがない場合, 自分の勝利
        if len(areas[a].sides) == 0:
            return areas[a].player_name

        # バトル場にポケモンがいない場合, 相手の勝利
        if len(areas[a].battle) == 0:
            return areas[a+1].player_name
    

def main():
    # 場を用意
    areas = set_area()

    # 勝負
    areas = progress(areas)

    # 勝敗判定
    judge(areas)


if __name__ == "__main__":
    main()