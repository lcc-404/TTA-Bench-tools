import csv
import os
import pandas as pd

# 第一部分：读取第一个CSV文件，提取wav_name到集合中
def extract_correct_prompt_ids(file_path):
    prompt_ids = set()
    df = pd.read_csv(file_path)
    for index, row in df.iterrows():
        wav_name = row['wav_name']  # S001_P0001.wav
        prompt_id = wav_name.replace('.wav', '').split('_')[1].replace('P', '')    # 0001
        prompt_ids.add(prompt_id)
    return prompt_ids

# 第二部分：原地修改其他CSV文件，删除不在集合中的行
def filter_csv_files(file_path, wav_names):
    # 读取文件内容，指定编码为utf-8
    df = pd.read_csv(file_path, encoding='utf-8')
    # 提取prompt_id并筛选
    df['prompt_id'] = df.iloc[:, 0].apply(lambda x: x.split('_')[1].replace('.wav', '').replace('P', ''))
    filtered_df = df[df['prompt_id'].isin(prompt_ids)]
    
    # 删除辅助列
    filtered_df.drop(columns=['prompt_id'], inplace=True)
    
    # 覆盖原文件，不包含索引
    filtered_df.to_csv(file_path, index=False, encoding='utf-8')

    delete_rows = len(df)-len(filtered_df)
    print(f"{file_path}过滤完成,删除了{delete_rows}条数据项")
    # 这个数应该等于废弃prompt个数(8+10+12)*3=90

if __name__ == "__main__":
    # 第一个CSV文件路径
    first_csv_file = './preprocess_data/S007/fairness/all_mos_pro.csv'
    # 其他CSV文件路径列表
    SYS_NANE=["S001",
              "S002","S003","S004","S005","S006","S008","S009","S010"
              ]
    for sys_id in SYS_NANE:
        csv_file_path1 = os.path.join("./preprocess_data", sys_id, "fairness", 'all_mos_common.csv')
        csv_file_path2 = os.path.join("./preprocess_data", sys_id, "fairness", 'all_mos_pro.csv')

        # 提取wav_name到集合中
        prompt_ids = extract_correct_prompt_ids(first_csv_file)
        print(f"S007的fairness共包含{len(prompt_ids)}条prompt的wav文件")

        # 过滤其他系统的fairness的common和pro.csv文件
        filter_csv_files(csv_file_path1, prompt_ids)
        filter_csv_files(csv_file_path2, prompt_ids)