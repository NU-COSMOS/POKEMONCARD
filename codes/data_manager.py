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
        self.card_types = ["Monster", "Trainer", "Accessory", "Energy", "Stadium"]
        self.types = ["炎", "水", "電気", "無", "闘", "悪", "鋼", "超", "草", "妖", "竜", "None"]

    def common(self, card):
        """
        共通項目
        """
        res = []
        # カード名が文字列かどうかチェック
        res.append(type(card["name"]) == str)

        # カードタイプが存在するものかどうかチェック
        res.append(card["card_type"] in self.card_types)

        # イラストが存在するかチェック
        res.append(os.path.isfile(card["img"]))

        return all(res)

    def monster(self, card):
        """
        モンスター
        """
        res = []
        # 体力が10の倍数かつ0以下でないか
        res.append(card["hp"] % 10 == 0 and card["hp"] <= 0)

        # タイプに存在するものが入力されているか
        for t in card["types"]:
            res.append(t in self.types)

        # タイプにNoneが含まれていないか
        res.append("None" not in card["types"])

        # 弱点属性に存在するものが入力されているか
        for weak in card["weaks"]:
            res.append(weak in self.types)

        # 弱点属性にNoneが含まれている場合, Noneだけか
        res.append(self.none_only(card["weaks"]))

        # 抵抗属性に存在するものが入力されているか
        for resist in card["resists"]:
            res.append(resist in self.types)

        # 抵抗属性にNoneが含まれている場合, Noneだけか
        res.append(self.none_only(card["resists"]))

        # 逃げるためのエネルギーは存在するものが入力されているか
        for escape in card["escape"]:
            res.append(escape in self.types)

        # 逃げるエネルギーにNoneが含まれている場合, Noneだけか
        res.append(self.none_only(card["escape"]))

        # 特性名はstrか
        res.append(type(card["chara"]) == str)

        # 技名を一つずつ確認
        for skill in card["skills"]:
            res.append(type(skill) == str)

        # 進化前orたねがstrで入力されているか
        res.append(type(card["before"]) == str)

        return all(res)

    def trainer(self, card):
        """
        トレーナー
        """

    def accessory(self, card):
        """
        持ち物
        """

    def energy(self, card):
        """
        エネルギーカード
        """
        res = []
        # 存在する属性が入力されているか
        res.append(card["color"] in self.types)

    def stadium(self, card):
        """
        スタジアムカード
        """

    def none_only(list):
        """
        Noneの文字列が入っていた場合、それだけしか入っていないことを確認
        """
        if "None" in list:
            return len(list == 1)
        else:
            return True


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
            new_card["card_type"] = input("カードの種類(Monster, Trainer, Accessory, Energy, Stadium)：")
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

        # トレーナーカードの入力内容
        elif new_card["card_type"] == "Trainer":
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
            # 初めての登録の場合
            if not os.path.exists(save_path):
                with open(save_path, 'w') as f:
                    print("レポートが見つからないので新しく作成します")
                    card_data = {"cards": [new_card], "skills": [], "charas": []}
                    json.dump(card_data, f, indent = 4)
            else:
                with open(save_path, 'r') as f:
                    card_data = json.load(f)
                    print(card_data)
                    card_data["cards"].append(new_card)

            # データを保存
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
        登録済みのカードデータを変更
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