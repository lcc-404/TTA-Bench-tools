"""
将交付数据整理为如下格式
preprocess_data/
    S001/
        acc/
            all_mos_common.csv 普通组全部人员评分
            all_mos_pro.csv 专业组全部人员评分
        fairness/
            同上
        generalizaiton
        robustness/
    S002/
        acc/
        ...
    ...
    S010/
"""
import os
import csv
from time import sleep
import pandas as pd


def get_dimension(prompt_id: int) -> str:
    """根据prompt编号获取对应的维度"""
    for dim, (start, end) in EVAL_DIM.items():
        if start <= prompt_id <= end:
            return dim
    raise ValueError(f"Invalid prompt ID: {prompt_id}")

def process_csv(input_csv_path: str, suffix: str):
    """
    把csv文件中每行数据归到应该属于的sys/dim/all_mos.csv文件中
    input:  ./音频评测标注_20250423交付/普通人员\result-ruike001.csv
    suffix: pro/common
    """
    # 读取CSV文件
    df = pd.read_csv(input_csv_path)

    # 摘出文件名中的person_id
    person_id = input_csv_path.split('\\')[-1].split('-')[1].split('.')[0]  # 获取 'ruike001'
    # print(person_id)

    # 遍历每一行数据
    for index, row in df.iterrows():
        wav_name = row['name']  # S001_P0001.wav
        system_id = wav_name.replace('.wav', '').split('_')[0]  # S001
        if system_id =="S000":  # 探针
            continue
        prompt_id = wav_name.replace('.wav', '').split('_')[1].replace('P', '')    # 0001
        
        # 获取对应的维度
        dim = get_dimension(int(prompt_id))
        
        # 输出csv路径
        output_csv_path = os.path.join(OUTPUT_DIR, system_id, dim, f'all_mos_{suffix}.csv')
        
        # 如果输出文件不存在，则创建并写入表头
        if not os.path.exists(output_csv_path):
            with open(output_csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['wav_name', 'person_id', '复杂度', '喜爱度', '质量', '一致性', '实用性'])
        
        # 文件已存在，将当前行数据写入对应的输出文件
        with open(output_csv_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([wav_name, person_id, row['复杂度'], row['喜爱度'], row['质量'], row['一致性'], row['实用性']])
    print("已处理", input_csv_path)

if __name__ == "__main__":
    # 各维度的prompt范围
    EVAL_DIM = {
        'acc': (1, 1500),
        'generalization': (1501, 1800),
        'robustness': (1801, 2100),
        'fairness': (2101, 2400)
    }
    SYS_NANE=["S001","S002","S003","S004","S005","S006","S007","S008","S009","S010"]

    # 待处理数据路径
    # INPUT_DIR1 = "./音频评测标注_20250423交付/普通人员"
    # INPUT_DIR2 = "./音频评测标注_20250423交付/专业人员"

    # INPUT_DIR1 = "./音频评测标注_20250428交付_1/普通人员"
    # INPUT_DIR2 = "./音频评测标注_20250428交付_1/专业人员"
    
    # INPUT_DIR1 = "./音频评测标注_20250428交付_2/普通人员"
    # INPUT_DIR2 = "./音频评测标注_20250428交付_2/专业人员"

    # INPUT_DIR1 = "./音乐评测标注_20250507交付_第四批/普通人员/标注结果"
    # INPUT_DIR2 = "./音乐评测标注_20250507交付_第四批/专业人员/标注结果"

    # INPUT_DIR1 = "./音乐评测标注_20250507交付_第五批/普通人员/标注结果"
    # INPUT_DIR2 = "./音乐评测标注_20250507交付_第五批/专业人员/标注结果"

    # INPUT_DIR1 = "./音频评测标注_20250508交付_第六批/普通人员/标注结果"
    # INPUT_DIR2 = "./音频评测标注_20250508交付_第六批/专业人员/标注结果"

    # INPUT_DIR1 = "./音频评测标注_20250509交付/普通人员/"
    # INPUT_DIR2 = "./音频评测标注_20250509交付/专业人员/"

    INPUT_DIR1 = "./音频评测标注_20250514交付/普通人员/"
    INPUT_DIR2 = "./音频评测标注_20250514交付/专业人员/"

    OUTPUT_DIR = './preprocess_data'

    # # 输出文件夹
    # for sys in SYS_NANE:
    #     for dimension in EVAL_DIM.keys():
    #         os.makedirs(os.path.join(OUTPUT_DIR, sys, dimension), exist_ok=True)

    # 处理普通组
    for input_csv_path in os.listdir(INPUT_DIR1):
        process_csv(os.path.join(INPUT_DIR1,input_csv_path),suffix='common')
    # 处理专业组
    for input_csv_path in os.listdir(INPUT_DIR2):
        process_csv(os.path.join(INPUT_DIR2,input_csv_path),suffix='pro')
