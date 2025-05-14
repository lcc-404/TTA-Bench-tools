import json
import os 
import pandas as pd

# prompt文件路径
ACC_PROMPT_PATH = "./prompts/acc_prompt.json"

def load_prompts(prompt_path: str, target_field: str) -> dict:
    """加载prompt文件中的目标字段"""
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompts = json.load(f)
    return {prompt_data['id']: prompt_data[target_field] for prompt_data in prompts}

# 存储每个prompt id到其所属维度的细分属性值的映射，类似"prompt_0001":"dataset"
acc_source_map = load_prompts(ACC_PROMPT_PATH, "source")

def get_prompt_attr(prompt_id: str) -> str:
    """根据prompt编号，去对应的prompt属性字典里取对应值"""
    if 1 <= int(prompt_id) <= 1500:
        return acc_source_map[f"prompt_{prompt_id}"]
    else:
        raise ValueError(f"Invalid prompt ID: {prompt_id}")
    

SYS_NANE=[
    # "S001",  "S002", "S003","S004","S005","S006","S007",
    "S008",
    # "S009","S010"
]

EVAL_DIM=[
    "acc",
]

if __name__ == "__main__":

    outfile_common = "./subjective_results/acc_source_result_common.txt"
    outfile_pro = "./subjective_results/acc_source_result_pro.txt"

    for sys_id in SYS_NANE:
        for eval_dim in EVAL_DIM:
            # 指定系统、指定维度的普通mos.csv和专业mos.csv
            temp = sys_id + '_' + eval_dim
            search_path = f'./preprocess_data/{sys_id}/{eval_dim}/'
            common_mos_file = os.path.join(search_path, "all_mos_common.csv")    
            pro_mos_file = os.path.join(search_path, "all_mos_pro.csv")

            # 读取文件
            df_common = pd.read_csv(common_mos_file)   # \preprocess_data\S006\robustness\all_mos_common.csv
            df_pro = pd.read_csv(pro_mos_file)      # \preprocess_data\S006\robustness\all_mos_pro.csv


            # ============普通组==============
            # 每个大维度维护一个字典存储结果
            # 键是prompt_attr，每个键对应的值是一个包含5种total_mos的字典
            results_common = {}

            # 遍历每一行数据
            for index, row in df_common.iterrows():
                wav_name=row['wav_name']    # S001_P0013.wav
                # 提取prompt编号
                prompt_id = wav_name.split('_')[1].replace('.wav', '').replace("P","")  # "0001"
                # 获取对应的属性
                prompt_attr = get_prompt_attr(prompt_id)
                # print("prompt_id:", prompt_id, ",prompt_attr:", prompt_attr)

                # 每个属性对应一组分数，如果当前属性还没有初始化，初始化它
                if prompt_attr not in results_common:
                    results_common[prompt_attr] = {
                        'total_complexity': 0,
                        'total_enjoyment': 0,
                        'total_quality': 0,
                        'total_alignment': 0,
                        'total_usefulness': 0,
                        'count': 0
                    }

                # 当前属性已经被初始化,累加分数
                results_common[prompt_attr]['total_complexity'] += row['复杂度']
                results_common[prompt_attr]['total_enjoyment'] += row['喜爱度']
                results_common[prompt_attr]['total_quality'] += row['质量']
                results_common[prompt_attr]['total_alignment'] += row['一致性']
                results_common[prompt_attr]['total_usefulness'] += row['实用性']
                results_common[prompt_attr]['count'] += 1

            # 计算平均值,输出结果,并写入文件
            with open(outfile_common, 'a') as f1:
                for attr, data in results_common.items():
                    count = data['count']
                    if count > 0:
                        avg_complexity = data['total_complexity'] / count
                        avg_enjoyment = data['total_enjoyment'] / count
                        avg_quality = data['total_quality'] / count
                        avg_alignment = data['total_alignment'] / count
                        avg_usefulness = data['total_usefulness'] / count
                    else:
                        avg_complexity = avg_enjoyment = avg_quality = avg_alignment = avg_usefulness = 0

                    print(f"====={temp}_{attr}_common=====")
                    print(f"count:{count}")
                    print(f"Average Complexity: {avg_complexity}")
                    print(f"Average Enjoyment: {avg_enjoyment}")
                    print(f"Average Quality: {avg_quality}")
                    print(f"Average Alignment: {avg_alignment}")
                    print(f"Average Usefulness: {avg_usefulness}")
            """
                    # 写入结果到文件
                    f1.write(f"====={temp}_{attr}=====\n")
                    f1.write(f"count: {count}\n")
                    f1.write(f"Average Complexity: {avg_complexity}\n")
                    f1.write(f"Average Enjoyment: {avg_enjoyment}\n")
                    f1.write(f"Average Quality: {avg_quality}\n")
                    f1.write(f"Average Alignment: {avg_alignment}\n")
                    f1.write(f"Average Usefulness: {avg_usefulness}\n")
                    f1.write("\n")  # 添加一个空行分隔不同属性的结果
            """
            
            """
            # ============专业组==============
            # 存储结果：键是prompt_attr，每个键对应的值是一个包含5种total_mos的字典
            results_pro = {}
            # 遍历每一行数据
            for index, row in df_pro.iterrows():
                wav_name=row['wav_name']    # S001_P0013.wav
                # 提取prompt编号
                prompt_id = wav_name.split('_')[1].replace('.wav', '').replace("P","")  # "0001"
                # 获取对应的属性
                prompt_attr = get_prompt_attr(prompt_id)
                print("prompt_id:", prompt_id, ",prompt_attr:", prompt_attr)

                # 每个属性对应一组分数，如果当前属性还没有初始化，初始化它
                if prompt_attr not in results_pro:
                    results_pro[prompt_attr] = {
                        'total_complexity': 0,
                        'total_enjoyment': 0,
                        'total_quality': 0,
                        'total_alignment': 0,
                        'total_usefulness': 0,
                        'count': 0
                    }

                # 当前属性已经被初始化,累加分数
                results_pro[prompt_attr]['total_complexity'] += row['复杂度']
                results_pro[prompt_attr]['total_enjoyment'] += row['喜爱度']
                results_pro[prompt_attr]['total_quality'] += row['质量']
                results_pro[prompt_attr]['total_alignment'] += row['一致性']
                results_pro[prompt_attr]['total_usefulness'] += row['实用性']
                results_pro[prompt_attr]['count'] += 1

            # 计算平均值,输出结果,并写入文件
            with open(outfile_pro, 'a') as f2:
                for attr, data in results_pro.items():
                    count = data['count']
                    if count > 0:
                        avg_complexity = data['total_complexity'] / count
                        avg_enjoyment = data['total_enjoyment'] / count
                        avg_quality = data['total_quality'] / count
                        avg_alignment = data['total_alignment'] / count
                        avg_usefulness = data['total_usefulness'] / count
                    else:
                        avg_complexity = avg_enjoyment = avg_quality = avg_alignment = avg_usefulness = 0

                    print(f"====={temp}_{attr}_pro=====")
                    print(f"count:{count}")
                    print(f"Average Complexity: {avg_complexity}")
                    print(f"Average Enjoyment: {avg_enjoyment}")
                    print(f"Average Quality: {avg_quality}")
                    print(f"Average Alignment: {avg_alignment}")
                    print(f"Average Usefulness: {avg_usefulness}")
                    # 写入结果到文件
                    f2.write(f"====={temp}_{attr}=====\n")
                    f2.write(f"count: {count}\n")
                    f2.write(f"Average Complexity: {avg_complexity}\n")
                    f2.write(f"Average Enjoyment: {avg_enjoyment}\n")
                    f2.write(f"Average Quality: {avg_quality}\n")
                    f2.write(f"Average Alignment: {avg_alignment}\n")
                    f2.write(f"Average Usefulness: {avg_usefulness}\n")
                    f2.write("\n")  # 添加一个空行分隔不同属性的结果
            """
    f1.close()    
    f2.close()