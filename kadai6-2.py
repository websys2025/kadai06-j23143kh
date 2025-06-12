import requests
import pandas as pd

# --------------------------------------------------------
# kadai6-2.py
#
# 参照するオープンデータ:
# 名称：気象庁（Japan Meteorological Agency）の天気予報データ（試験提供）
# 概要：本APIは、地点ごとの天気予報や気温予測などの情報をJSON形式で提供する。
# エンドポイント：https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json
# 使用方法：
#   - area_code には地方または都道府県ごとのコードを指定する。
#   - 例：130000 → 東京都
# 提供機能：
#   - 日別の天気予報、最高気温、最低気温、降水確率など
# --------------------------------------------------------

# 東京都（area code: 130000）のデータ取得
area_code = "130000"
url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"

response = requests.get(url)
weather_data = response.json()

# データから日別天気予報と気温の抽出
time_series = weather_data[0]['timeSeries'][0]
dates = time_series['timeDefines']
import requests
import pandas as pd

# --------------------------------------------------------
# kadai6-1.py
#
# 参照するオープンデータ:
# 名称：気象庁（JMA）天気予報オープンデータ
# エンドポイント：https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json
# 地域コード：130000（東京都）
# 提供機能：天気予報、気温、降水確率などを日別に取得可能
# --------------------------------------------------------

area_code = "130000"
url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"

response = requests.get(url)
weather_data = response.json()

# --- 天気予報を取得 ---
time_series_weather = weather_data[0]['timeSeries'][0]
dates = time_series_weather['timeDefines']
weathers = time_series_weather['areas'][0]['weathers']

# --- 気温情報（ある場合のみ取得） ---
temps_max = []
temps_min = []

for ts in weather_data[0]['timeSeries']:
    if 'tempsMax' in ts['areas'][0] and 'tempsMin' in ts['areas'][0]:
        temps_max = ts['areas'][0]['tempsMax']
        temps_min = ts['areas'][0]['tempsMin']
        break

# --- データが不足している場合に備えて補完 ---
max_len = len(dates)
temps_max = temps_max + ["―"] * (max_len - len(temps_max))
temps_min = temps_min + ["―"] * (max_len - len(temps_min))

# --- DataFrameで整形 ---
df = pd.DataFrame({
    '日付': dates,
    '天気予報': weathers,
    '最高気温': temps_max,
    '最低気温': temps_min
})

print(df)

df.columns = [col_replace_dict.get(col, col) for col in df.columns]

# 表示
print(df)

