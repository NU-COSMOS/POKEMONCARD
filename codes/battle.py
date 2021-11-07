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


def show(areas,turn_cnt):
    """
    場の状況を表示
    """
    all_area = np.concatenate([np.rot90(areas[0].get_img(), 3), np.rot90(areas[1].get_img(), 1)], axis = 1)

    # 体力ゲージの変化動画, 開始フレーム, 終了フレームを取得 
    # サイズ : 906×386 
    # フレーム数 : 0フレーム(体力最大)～100フレーム(体力0)の101フレーム
    cap_list0, start_frame_list0, end_frame_list0, place_list0 = areas[0].get_cap(turn_cnt, 0)
    cap_list1, start_frame_list1, end_frame_list1, place_list1 = areas[1].get_cap(turn_cnt, 1)

    # 先攻と後攻の動画を1つのリストにまとめる
    cap_list         = cap_list0 + cap_list1 
    start_frame_list = start_frame_list0 + start_frame_list1
    place_list       = place_list0 + place_list1
    end_frame_list   = end_frame_list0 + end_frame_list1

    # 終了フレームの画像を取得 
    end_img_list = []
    for i in range(len(cap_list)):
        end_img = Area.get_frame_img(end_frame_list[i])
        end_img_list.append(end_img)

    # 複数のベンチポケモンを表示する際にどれだけ各ベンチポケモンを移動させるかを決める定数
    bench_h0 = 100
    bench_h1 = 100

    # 開始フレームから動画を開始
    for i in range(len(cap_list)):
        cap_list[i].set(cv2.CAP_PROP_POS_FRAMES, start_frame_list[i])

    x = np.array(start_frame_list)
    y = np.array(end_frame_list)    
    
    # フィールド及び体力ゲージの変化を表示
    for i in range(max(y-x)+1):
        frame_list = []
        for s in range(len(cap_list)):
            ret, frame = cap_list[s].read()
            frame_list.append(frame)
      
        for t in range(len(cap_list)):
            delay = 500
            # 最終フレームに達した動画から静止画に移行
            if i + start_frame_list[t] < end_frame_list[t]:
                Frame = cv2.resize(frame_list[t], (int(906/4),int(386/4)))
            elif i + start_frame_list[t] >= end_frame_list[t]:
                Frame = end_img_list[t]
        
            if place_list[t] == 0:
                all_area[0:int(386/4),100:100+int(906/4)] = Frame
            elif place_list[t] == 1:    
                all_area[0:int(386/4),600:600+int(906/4)] = Frame
            elif 2 <= place_list[t] and place_list[t] <= 6:
                all_area[100+bench_h0*(place_list[t]-2):100+bench_h0*(place_list[t]-2)+int(386/4),0:int(906/4)] = Frame
            elif 7 <= place_list[t]:
                all_area[100+bench_h1*(place_list[t]-7):100+bench_h1*(place_list[t]-7)+int(386/4),700:700+int(906/4)] = Frame                    

        cv2.imshow("Field",all_area) 

        # 全ての動画が最終フレームに達したとき, waitKeyを0にする
        cur_frame_list    = [start_frame + i for start_frame in start_frame_list]
        z = np.array(cur_frame_list)
        if all(diff >= 0 for diff in z-y):
            delay = 0
                    
        if cv2.waitKey(delay) & 0xFF == ord('q'): 
            break
    for u in range(len(cap_list)):               
        cap_list[u].release()
    
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
        show(areas,turn_cnt)

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