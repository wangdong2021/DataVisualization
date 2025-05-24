import csv
from collections import defaultdict

def process_nba_data(csv_file):
    # 创建字典来存储球员数据，结构为：{name: {year: [pts]}}
    players = defaultdict(lambda: defaultdict(list))
    
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # 跳过标题行
        
        # 创建列名到索引的映射
        col_indices = {header: idx for idx, header in enumerate(headers)}
        
        for row in reader:
            try:
                year = int(row[col_indices['Year']])
                player_name = row[col_indices['Player']]
                pts = float(row[col_indices['PTS']])
                
                # 添加到球员数据
                players[player_name][year].append(pts)
            except (ValueError, KeyError) as e:
                # 跳过格式错误或缺少必要字段的行
                continue
    
    # 转换为所需的输出格式
    result = []
    for name, yearly_data in players.items():
        # 对每个球员，处理其每年的数据
        merged_years = []
        merged_pts = []
        
        # 先按年份排序
        sorted_years = sorted(yearly_data.keys())
        
        for year in sorted_years:
            # 合并同一年份的所有PTS（通常应该只有一个值，但如果有则求和）
            pts_list = yearly_data[year]
            total_pts = sum(pts_list)  # 如果同一年有多个记录，求和
            merged_years.append(year)
            merged_pts.append(total_pts)
        
        result.append({
            'name': name,
            'PTS': merged_pts,
            'year': merged_years
        })
    
    return result

# 使用示例
csv_file = 'nba-players-stats/Seasons_Stats.csv'  # 替换为你的CSV文件路径
player_stats = process_nba_data(csv_file)
import json
# 打印前几个球员作为示例
for player in player_stats[:5]:
    print(player)
with open("a.json", "w") as f:
    json.dump(player_stats, f, indent=2)