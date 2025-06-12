import requests
import pandas as pd

# 個人のAPI Key
APP_ID = "8d813ed77283c8a9ff5ed74468de13179addcb78"

# e-Stat API URL
API_URL = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

# パラメータ
params = {
    "appId": APP_ID,
    "lang": "J",
    "statsDataId": "0003235424",  # 労働務統計
    "dataFormat": "J",
    "metaGetFlg": "Y",
    "explanationGetFlg": "Y",
    "annotationGetFlg": "Y",
    "replaceSpChars": 0,
    "cntGetFlg": "N",
    "sectionHeaderFlg": 1
}

# データ取得
response = requests.get(API_URL, params=params)
data = response.json()

# VALUE部分を抽出
values = data['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']['VALUE']
df = pd.DataFrame(values)

# 各クラスIDと名前の対応を作成
meta_info = data['GET_STATS_DATA']['STATISTICAL_DATA']['CLASS_INF']['CLASS_OBJ']

for class_obj in meta_info:
    column_name = '@' + class_obj['@id']
    id_to_name_dict = {}

    if isinstance(class_obj['CLASS'], list):
        for obj in class_obj['CLASS']:
            id_to_name_dict[obj['@code']] = obj['@name']
    else:
        obj = class_obj['CLASS']
        id_to_name_dict[obj['@code']] = obj['@name']

    if column_name in df.columns:
        df[column_name] = df[column_name].replace(id_to_name_dict)

# 列名をわかりやすいものに置換
col_replace_dict = {'@unit': '単位', '$': '値'}
for class_obj in meta_info:
    org_col = '@' + class_obj['@id']
    new_col = class_obj['@name']
    col_replace_dict[org_col] = new_col

df.columns = [col_replace_dict.get(col, col) for col in df.columns]

# 表示
print(df)

