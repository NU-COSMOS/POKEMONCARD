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
        self.status = ["None", "毒", "まひ", "眠り", "氷", "やけど", "こんらん"]
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

        # 技に必要なエネルギーを確認
        for skill in card["skills"]:
            for e in skill["energy"]:
                res.append(e in self.types)
                messages.append(self.message['type_error'])

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
            return len(list) == 1
        else:
            return True

    def print_error(self, res, messages):
        for i, m in zip(res, messages):
            if not i:
                print(m)

    def damage(self, dmg):
        """
        ダメージの値をチェック
        """
        return type(dmg) == int and dmg % 10 == 0


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
                # new_card["chara"] = input("特性名：")
                new_card["skills"] = Skill.regist(input("技名(例：なきごえ,たいあたり)：").split(","))
                new_card["before"] = input("進化前(たね or ポケモン名)：")

                # 入力内容をチェック
                if checker.monster(new_card):
                    break
                print("モンスターの入力内容に誤りがあるのでもう一度やり直してください")

        # サポートカードの入力内容
        elif new_card["card_type"] == "Support":
            new_card["skills"] = Skill.construct()

        # グッズカードの入力内容
        elif new_card["card_type"] == "Goods":
            pass

        # エネルギーカードの入力内容
        elif new_card["card_type"] == "Energy":
            while(1):
                print("属性一覧：{}".format(checker.types))
                new_card["color"] = input("エネルギーカードの属性：")

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
                    card_data = {"cards": [new_card]}
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
                json.dump(card_data, f, indent = 4, ensure_ascii = False)
            print("登録しました")
        else:
            print("入力を破棄しました")
        print("操作を終了します")

    def inquiry(save_path):
        """
        カードのID照会
        """
        with open(save_path, 'r') as f:
            card_data = json.load(f)

        name_part        = input("アクセスするカードの名前(一部でも可)を入力し, IDを取得してください:")

        # 入力したカード名のヒット件数 初期値:0
        hits_num         = 0

        # 入力したカード名の照会
        for card in card_data['cards']:
            if name_part in card['name']:
                if hits_num == 0:
                    name_ID_dict = {card['name']:card['main_id']}
                else:
                    name_ID_dict[card['name']] = card['main_id']
                hits_num = hits_num + 1

        print(hits_num,"件ヒットしました")  

        # ヒットしたカード名とIDの出力
        for k, v in name_ID_dict.items():
            print(k,"ID:",v)

    def delete(save_path):
        """
        登録済みのカードデータを削除
        """ 

        Data.inquiry("../card_data.json")

        with open(save_path, 'r') as f:
            card_data = json.load(f)        

        main_id     = int(input("情報を削除するカードのIDを入力してください：")) 

        # カードデータの削除
        card_data["cards"].pop(main_id) 
 
        # 削除後のカード枚数
        card_num = len(card_data['cards'])

        # 削除したカードのIDより大きいカードのID変更
        for card in card_data['cards'][main_id:card_num]:
            card['main_id'] = card['main_id']-1
            card['sub_id']  = card['sub_id']-1    

        # 実行確認フェーズ
        y_n = input("本当に削除してよろしいですか？(y/n)")
        if y_n == "y":
            with open(save_path, 'w') as f:
                json.dump(card_data, f, indent = 4)
            print("カードデータの削除完了") 
        else:
             print("入力を破棄しました")
        print("操作を終了します") 
    
    def update(save_path):
        """
        登録済みのカードデータの内容を更新
        """

        # 入力内容のチェッカー
        checker = Checker() 

        Data.inquiry("../card_data.json")

        with open(save_path, 'r') as f:
            card_data = json.load(f) 

        main_id     = int(input("情報を更新するカードのIDを入力してください："))
        card_type   = input("修正後のカードタイプを入力してください\n修正しない場合は修正前のタイプを入力してください\n(Monster, Support, Accessory, Energy, Stadium, Goods):")
        
        if card_type == "Monster":
            print("0:カード名 1:画像パス 2:体力 3:モンスターのタイプ 4:弱点属性 5:抵抗属性 6:逃げるのに必要なエネルギー 7:特性名 8:技名 9:進化前")
            update_list_int = list(map(int, input("修正する項目を数字で選択してください(複数可) (例：0,1):").split(",")))

            for update_num in update_list_int:
                while(1):
                    if update_num == 0:
                        card_data["cards"][main_id]["name"]      = input("カード名：")
                    elif update_num == 1:
                        card_data["cards"][main_id]["img"]       = input("カードイラストのパス：")
                    elif update_num == 2:
                        card_data["cards"][main_id]["hp"]        = int(input("モンスターの体力：")) 
                    elif update_num == 3: 
                        card_data["cards"][main_id]["types"]     = input("モンスターのタイプ(例：炎,水)：").split(",")         
                    elif update_num == 4: 
                        card_data["cards"][main_id]["weaks"]     = input("モンスターの弱点属性(例：炎,水)：").split(",")
                    elif update_num == 5:
                        card_data["cards"][main_id]["resists"]   = input("モンスターの抵抗属性(例：炎,水)：").split(",")
                    elif update_num == 6:
                        card_data["cards"][main_id]["escape"]    = input("モンスターが逃げるのに必要なエネルギー(例：炎,炎)：").split(",")
                    elif update_num == 7:
                        card_data["cards"][main_id]["chara"]     = input("特性名：")
                    elif update_num == 8:
                        card_data["cards"][main_id]["skills"]    = Skill.regist(input("技名(例：なきごえ,たいあたり)：").split(","))
                    elif update_num == 9:
                        card_data["cards"][main_id]["before"]   = input("進化前(たね or ポケモン名)：")

                    if 0 <= update_num <= 1:
                        if checker.common(card_data["cards"][main_id]):
                            break
                        print("入力内容に誤りがあるのでもう一度やり直してください") 
                    elif 2 <= update_num <= 9:
                        if checker.monster(card_data["cards"][main_id]):
                            break
                        print("モンスターの入力内容に誤りがあるのでもう一度やり直してください")                    

        elif card_type == "Support":  
            pass  
        elif card_type == "Goods":
            pass
        elif card_type == "Energy": 
            pass
        elif card_type == "Accessory":  
            pass
        elif card_type == "Stadium":
            pass 

        # 登録内容の確認フェーズ
        print("\n登録内容")
        print(card_data["cards"][main_id])
        y_n = input("この内容でよろしいですか？(y/n)")

        if y_n == "y":
            # 修正されたカードデータを保存
            with open(save_path, 'w') as f:
                json.dump(card_data, f, indent = 4)
            print("修正内容を登録しました") 
        else:
             print("入力を破棄しました")
        print("操作を終了します")                                                            

    def search():
        """
        カードデータの検索
        """

    def show(save_path):
        """
        カードデータの閲覧
        """
        Data.inquiry("../card_data.json")

        with open(save_path, 'r') as f:
            card_data = json.load(f)        

        main_id_list = list(map(int, input("閲覧するカードのIDを入力してください(複数可) (例：0,1):").split(","))) 

        for main_id in main_id_list:
            print(card_data["cards"][main_id])      


class Skill:
    """
    カードの効果を構成
    """
    def regist(skills):
        """
        カード効果を組み立てる
        """
        skill_list = []
        for skill_name in skills:
            skill = {}
            print(skill_name, "の内容")
            skill["name"] = skill_name
            skill["block"] = Skill.construct()
            skill["energy"] = Skill.need_energy()
            skill_list.append(skill)

        return skill_list

    def construct():
        """
        スキルブロックを積み上げる
        """
        checker = Checker()
        blocks = []
        while(1):
            block_type = input("選択肢(damage, status)：")
            block = {}
            block["block type"] = block_type

            if block_type == "damage":
                damage_type = input("ダメージの種類を選択してください 選択肢(normal, coin, side, energy):") 

                if damage_type == "normal":
                    block["damage type"] = damage_type
                    while(1):
                        block["damage"] = int(input("ダメージを入力してください:")) 
                        if checker.damage(block["damage"]):
                            break
                        print("ダメージの入力が不正です") 
                    blocks.append(block) 
                     
                elif damage_type == "coin" or damage_type == "side" or damage_type == "energy":
                    block["damage type"] = damage_type
                    if damage_type == "coin":
                        block["trial_num"]   = input("コインを投げる回数の上限を入力してください　無限の場合はIと入力してください:")                     
                    while(1):
                        block["base damage"] = int(input("基本ダメージを入力してください:")) 
                        block["add damage"]  = int(input("追加ダメージを入力してください:"))
                        if checker.damage(block["base damage"]) and checker.damage(block["add damage"]):
                            break
                        print("ダメージの入力が不正です")
                    blocks.append(block)                                           

            elif block_type == "status":              
                while(1):
                    block["status"] = input("状態異常を入力してください(None, 毒, まひ, 眠り, 氷, やけど, こんらん)：")
                    if block["status"] in checker.status:
                        break
                    print("存在しない状態異常が入力されました")
                blocks.append(block)

            if block_type != "Q":
                target = input("技の対象を選択してください 選択肢(battle_self, battle_opponent, bench_self, bench_opponent)：")
                block["target"] = target

            elif block_type == "Q":
                break

            print("終了する場合はQ")

        return blocks

    def need_energy():
        """
        技を使うのに必要なエネルギーカードを登録する
        """
        energies = input("技を使うのに必要なエネルギー(例：炎,炎)：").split(",")
        return energies
