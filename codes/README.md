# USAGE

### カード・デッキの登録
`python edit.py`

### 対戦
未実装  
`python battle.py`

# 情報の保存形式
### カードデータ全体
形式：json
内容：{"cards": [card1, card2, ...]}

### 各カード共通
形式：python, 辞書型
内容：{"name": "名前", "card_type": "種類", "img": "画像パス", ...}

### モンスターカード
形式：python, 辞書型
内容：{"hp": 体力(int), "types": モンスターのタイプ(str), "weaks": 弱点タイプ(str), "resists": 抵抗タイプ(str), ...}