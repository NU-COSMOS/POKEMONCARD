#-*- coding:utf-8 -*-
"""
試合する
"""
import pickle

from player import Player
from area import Area
from action import Action


def load_deck(deck_name):
    """
    デッキデータの読み込み
    """
    with open(f"../{deck_name}.pkl", "r") as file:
        deck = pickle.load(file)

    return deck


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

    areas = ready(areas)

    return areas


def ready(areas):
    """
    試合開始の準備を整える
    """
    for area in areas:
        # 手札を用意
        area.set_hands(5)
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
    ・次の手番のプレイヤーの山札が0枚
    """
    return True


def turn(areas, turn_cnt):
    """
    手番
    """
    print(f"{turn_cnt+1}ターン目")
    print(f"{areas[turn_cnt%2].player_name}のターンです")

    # ターン開始時にはカードを1枚引く
    areas[turn_cnt%2].draw(1)

    while(1):
        act = int(input("行動を選択して下さい\n1:攻撃\n2:終了\n"))
        
        # 攻撃技を使用
        if act == 1:
            areas = Action.attack(areas, turn_cnt)
            # 技を使用したらターン終了
            break

        # ターン終了
        elif act == 2:
            break

    # 状態異常のダメージ等、ターン終了時の処理

    # 瀕死のポケモンがいたらサイドをとる

    return areas


def progress(areas):
    """
    各プレイヤーが交互に手番を行う
    """
    turn_cnt = 0
    while(1):
        areas = turn(areas, turn_cnt)

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
    for area in areas:
        winner = area.name

    return winner


def main():
    # 場を用意
    areas = set_area()

    # 勝負
    areas = progress(areas)

    # 勝敗判定
    judge(areas)


if __name__ == "__main__":
    main()