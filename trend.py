import pandas as pd
import numpy as np

# 读取数据（假设数据已加载为df）
# 此处以用户提供的表格数据为例，实际可能需要pd.read_csv()

csv_file = 'nba-players-stats/Seasons_Stats.csv'  # 替换为你的CSV文件路径
df = pd.read_csv(csv_file)
# 计算PPG（场均得分），需排除G=0的无效数据
df['PPG'] = df['PTS'] / df['G'].replace(0, np.nan)

# 计算各命中率（处理分母为0的情况）
df['FG%'] = df['FG'] / df['FGA'].replace(0, np.nan)
df['3P%'] = df['3P'] / df['3PA'].replace(0, np.nan)
df['2P%'] = df['2P'] / df['2PA'].replace(0, np.nan)

# 若TS%列是百分比小数则直接使用，否则按公式计算：
# df['TS%'] = df['PTS'] / (2 * (df['FGA'] + 0.44 * df['FTA']))

# 按年份分组计算平均值
result = df.groupby('Year').agg({
    'PPG': 'mean',
    'FG%': 'mean',
    '3P%': 'mean',
    '2P%': 'mean',
    'TS%': 'mean'
}).round(3).reset_index()

# 重命名列名
result.columns = ['年份', '平均PPG', '平均投篮命中率', '平均三分命中率', '平均两分命中率', '平均真实命中率']

# result = df.groupby('Year').agg(...)  # 用户原有的分组聚合逻辑

# 写入CSV文件
result.to_csv('results.csv', index=False, encoding='utf-8-sig')
print(result)