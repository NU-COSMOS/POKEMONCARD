#-*- coding:utf-8 -*-
"""
カード情報の管理
"""
import os
import json


class Checker:
    """
    各項目の入力内容をチェック
    """
    def __init__(self):
        self.card_types = ["Monster", "Support", "Accessory", "Energy", "Stadium", "Goods"]
        self.types = ["炎", "水", "電気", "無", "闘", "悪", "鋼", "超", "草", "妖", "竜", "None"]
        self.message = {'type_error': '存在しない属性が入力されています', 
                        'none_error': 'Noneを選択した場合、その項目に別の属性を入力しないでください', 
                        'hp_error': '体力の数値が不正です', 
                        'path_error': '指定されたパスは存在しません', 
                        'dtype_error': '入力値が想定と異なります'}

    def common(self, card):
        """
        共通項目
        """
        res = []
        messages = []
        # カード名が文字列かどうかチェック
        res.append(type(card["name"]) == str)
        messages.append(self.message['dtype_error'])

        # カードタイプが存在するものかどうかチェック
        res.append(card["card_type"] in self.card_types)
        messages.append(self.message['type_error'])

        # イラストが存在するかチェック
        res.append(os.path.isfile(card["img"]))
        messages.append(self.message['path_error'])

        # エラー文を表示
        self.print_error(res, messages)

        return all(res)

    def monster(self, card):
        """
        モンスター
        """
        res = []
        messages = []
        # 体力が10の倍数かつ0以下でないか
        res.append(card["hp"] % 10 == 0 and card["hp"] > 0)
        messages.append(self.message['hp_error'])

        # タイプに存在するものが入力されているか
        for t in card["types"]:
            res.append(t in self.types)
            messages.append(self.message['type_error'])

        # タイプにNoneが含まれていないか
        res.append("None" not in card["types"])
        messages.append(self.message['none_error'])

        # 弱点属性に存在するものが入力されているか
        for weak in card["weaks"]:
            res.append(weak in self.types)
            messages.append(self.message['type_error'])

        # 弱点属性にNoneが含まれている場合, Noneだけか
        res.append(self.none_only(card["weaks"]))
        messages.append(self.message['none_error'])

        # 抵抗属性に存在するものが入力されているか
        for resist in card["resists"]:
            res.append(resist in self.types)
            messages.append(self.message['type_error'])

        # 抵抗属性にNoneが含まれている場合, Noneだけか
        res.append(self.none_only(card["resists"]))
        messages.append(self.message['none_error'])

        # 逃げるためのエネルギーは存在するものが入力されているか
        for escape in card["escape"]:
            res.append(escape in self.types)
            messages.append(self.message['type_error'])

        # 逃げるエネルギーにNoneが含まれている場合, Noneだけか
        res.append(self.none_only(card["escape"]))
        messages.append(self.message['none_error'])

        # 特性名はstrか
        res.append(type(card["chara"]) == str)
        messages.append(self.message['dtype_error'])

        # 技名を一つずつ確認
        for skill in card["skills"]:
            res.append(type(skill) == str)
            messages.append(self.message['dtype_error'])

        # 進化前orたねがstrで入力されているか
        res.append(type(card["before"]) == str)
        messages.append(self.message['dtype_error'])

        # エラー文を表示
        self.print_error(res, messages)

        return all(res)

    def support(self, card):
        """
        トレーナー
        """

    def accessory(self, card):
        """
        持ち物
        """

    def goods(self, card):
        """
        グッズカード
        """

    def energy(self, card):
        """
        エネルギーカード
        """
        res = []
        messages = []
        # 存在する属性が入力されているか
        res.append(card["color"] in self.types)
        messages.append(self.message['type_error'])

        # エラー文を表示
        self.print_error(res, messages)

        return all(res)

    def stadium(self, card):
        """
        スタジアムカード
        """

    def none_only(self, list):
        """
        Noneの文字列が入っていた場合、それだけしか入っていないことを確認
        """
        if "None" in list:
            return len(list == 1)
        else:
            return True

    def print_error(self, res, messages):
        for i, m in zip(res, messages):
            if not i:
                print(m)


class Data:
    """
    データ操作オブジェクト
    """
    def regist(save_path):
        """
        新しいカードデータを登録
        """
        # 新しいカードを辞書型で登録
        new_card = {}

        # 入力内容のチェッカー
        checker = Checker()

        # 共通項目を入力
        while(1):
            new_card["name"] = input("カード名：")
            new_card["card_type"] = input("カードの種類(Monster, Support, Accessory, Energy, Stadium, Goods)：")
            new_card["img"] = input("カードイラストのパス：")

            # 入力内容をチェック
            if checker.common(new_card):
                break
            print("入力内容に誤りがあるのでもう一度やり直してください")

        # 各カードタイプごとの情報を入力
        # モンスターカードの入力内容
        if new_card["card_type"] == "Monster":
            while(1):
                new_card["hp"] = int(input("モンスターの体力："))
                print("属性一覧：{}".format(checker.types))
                new_card["types"] = input("モンスターのタイプ(例：炎,水)：").split(",")
                new_card["weaks"] = input("モンスターの弱点属性(例：炎,水)：").split(",")
                new_card["resists"] = input("モンスターの抵抗属性(例：炎,水)：").split(",")
                new_card["escape"] = input("モンスターが逃げるのに必要なエネルギー(例：炎,炎)：").split(",")
                new_card["chara"] = input("特性名：")
                new_card["skills"] = input("技名(例：なきごえ,たいあたり)：").split(",")
                new_card["before"] = input("進化前(たね or ポケモン名)：")

                # 入力内容をチェック
                if checker.monster(new_card):
                    break
                print("モンスターの入力内容に誤りがあるのでもう一度やり直してください")

        # サポートカードの入力内容
        elif new_card["card_type"] == "Support":
            pass

        # グッズカードの入力内容
        elif new_card["card_type"] == "Goods":
            pass

        # エネルギーカードの入力内容
        elif new_card["card_type"] == "Energy":
            while(1):
                print("属性一覧：{}".format(checker.types))
                new_card["color"] == input("エネルギーカードの属性：")

                # 入力内容をチェック
                if checker.energy(new_card):
                    break
                print("エネルギーカードの入力内容に誤りがあるのでもう一度やりなおしてください")

        # 持ち物カードの入力内容
        elif new_card["card_type"] == "Accessory":
            pass

        # スタジアムカードの入力内容
        elif new_card["card_type"] == "Stadium":
            pass

        # 登録内容の確認フェーズ
        print("\n登録内容")
        print(new_card)
        y_n = input("この内容でよろしいですか？(y/n)")
        if y_n == "y":

            # カードデータの更新
            # 初めての登録の場合
            if not os.path.exists(save_path):
                print("レポートが見つからないので新しく作成します")
                with open(save_path, 'w') as f:
                    new_card['main_id'] = 0
                    new_card['sub_id'] = 0
                    card_data = {"cards": [new_card], "skills": [], "charas": []}
                    json.dump(card_data, f, indent = 4)

            # 二回目以降
            else:
                with open(save_path, 'r') as f:
                    card_data = json.load(f)

                    # main_idはカードの枚数分存在
                    new_card['main_id'] = len(card_data['cards'])

                    # 付与すべきsub_idを検索
                    flag = False
                    max_sub_id = 0
                    for card in card_data['cards']:
                        if card['sub_id'] == max_sub_id:
                            max_sub_id = card['sub_id'] + 1
                        if card['name'] == new_card['name']:
                            new_card['sub_id'] = card['sub_id']
                            flag = True
                            break
                    if not flag:
                        new_card['sub_id'] = max_sub_id

                    # カードデータを更新
                    card_data["cards"].append(new_card)

            # 更新されたカードデータを保存
            with open(save_path, 'w') as f:
                json.dump(card_data, f, indent = 4)
            print("登録しました")
        else:
            print("入力を破棄しました")
        print("操作を終了します")

    def delete():
        """
        登録済みのカードデータを削除
        """
    
    def update():
        """
        登録済みのカードデータの内容を更新
        """
    
    def search():
        """
        カードデータの検索
        """

    def show():
        """
        カードデータの閲覧
        """

Data.regist("../card_data.json")