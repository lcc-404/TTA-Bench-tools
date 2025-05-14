import os
import pandas as pd

EVAL_DIM = {
        'acc': (1, 1500),
        # 'generalization': (1501, 1800),
        # 'robustness': (1801, 2100),
        # 'fairness': (2101, 2400)
    }
SYS_ID=[
    # "S001","S002", "S003","S004","S005","S006","S007",
    "S008",
    # "S009","S010"
]

if __name__ == "__main__":
    outfile_common = "./subjective_results/result_common.txt"
    outfile_pro = "./subjective_results/result_pro.txt"
    f1 = open(outfile_common,'a')
    f2 = open(outfile_pro,'a')
    for sys_id in SYS_ID:
        for eval_dim in EVAL_DIM:
            # 指定系统、指定维度的人工评测wav文件的mos结果路径
            temp = sys_id + '_' + eval_dim
            search_path = f'./preprocess_data/{sys_id}/{eval_dim}/'
            common_mos_file = os.path.join(search_path, "all_mos_common.csv")    
            pro_mos_file = os.path.join(search_path, "all_mos_pro.csv")

            # 读取文件
            df_common = pd.read_csv(common_mos_file)   # \preprocess_data\S006\robustness\all_mos_common.csv
            df_pro = pd.read_csv(pro_mos_file)      # \preprocess_data\S006\robustness\all_mos_pro.csv

            # ============普通组==============
            # 初始化变量
            total_complexity_common = 0    # 复杂度,complexity
            total_enjoyment_common = 0     # 喜爱度,enjoyment
            total_quality_common = 0       # 质量,quality
            total_alignment_common = 0     # 一致性,alignment
            total_usefulness_common = 0    # 实用性,usefulness
            count_common = 0

            # 遍历每一行数据
            for index, row in df_common.iterrows():
                wav_complexity = row['复杂度']
                wav_enjoyment = row['喜爱度']
                wav_quality = row['质量']
                wav_alignment = row['一致性']
                wav_usefulness = row['实用性']
                total_complexity_common += wav_complexity
                total_enjoyment_common += wav_enjoyment
                total_quality_common += wav_quality
                total_alignment_common += wav_alignment
                total_usefulness_common += wav_usefulness
                count_common += 1

            # 计算平均值
            if count_common > 0:
                avg_complexity_common = total_complexity_common / count_common
                avg_enjoyment_common = total_enjoyment_common / count_common
                avg_quality_common = total_quality_common / count_common
                avg_alignment_common = total_alignment_common / count_common
                avg_usefulness_common = total_usefulness_common / count_common
            else:
                avg_complexity_common = avg_enjoyment_common = avg_quality_common = avg_alignment_common = avg_usefulness_common = 0

            # 输出结果
            print(f"====={temp}_common_mos=====")
            print(f"count:{count_common}")
            print(f"Average complexity: {avg_complexity_common}")
            print(f"Average enjoyment: {avg_enjoyment_common}")
            print(f"Average quality: {avg_quality_common}")
            print(f"Average alignment: {avg_alignment_common}")
            print(f"Average usefulness: {avg_usefulness_common}")
            """
            outline1 = str(temp) + '\n' + str(avg_complexity_common) + ',' + str(avg_enjoyment_common) + ',' + str(avg_quality_common) + ',' + str(avg_alignment_common) + ',' + str(avg_usefulness_common) + '\n'
            f1.write(outline1)
            """
            """
            # ============专业组==============
            # 初始化变量
            total_complexity_pro = 0    # 复杂度,complexity
            total_enjoyment_pro = 0     # 喜爱度,enjoyment
            total_quality_pro = 0       # 质量,quality
            total_alignment_pro = 0     # 一致性,alignment
            total_usefulness_pro = 0    # 实用性,usefulness
            count_pro = 0

            # 遍历每一行数据
            for index, row in df_pro.iterrows():
                wav_complexity = row['复杂度']
                wav_enjoyment = row['喜爱度']
                wav_quality = row['质量']
                wav_alignment = row['一致性']
                wav_usefulness = row['实用性']
                total_complexity_pro += wav_complexity
                total_enjoyment_pro += wav_enjoyment
                total_quality_pro += wav_quality
                total_alignment_pro += wav_alignment
                total_usefulness_pro += wav_usefulness
                count_pro += 1

            # 计算平均值
            if count_pro > 0:
                avg_complexity_pro = total_complexity_pro / count_pro
                avg_enjoyment_pro = total_enjoyment_pro / count_pro
                avg_quality_pro = total_quality_pro / count_pro
                avg_alignment_pro = total_alignment_pro / count_pro
                avg_usefulness_pro = total_usefulness_pro / count_pro
            else:
                avg_complexity_pro = avg_enjoyment_pro = avg_quality_pro = avg_alignment_pro = avg_usefulness_pro = 0

            # 输出结果
            print(f"====={temp}_pro_mos=====")
            print(f"count:{count_pro}")
            print(f"Average complexity: {avg_complexity_pro}")
            print(f"Average enjoyment: {avg_enjoyment_pro}")
            print(f"Average quality: {avg_quality_pro}")
            print(f"Average alignment: {avg_alignment_pro}")
            print(f"Average usefulness: {avg_usefulness_pro}")
            outline2 = str(temp) + '\n' + str(avg_complexity_pro) + ',' + str(avg_enjoyment_pro) + ',' + str(avg_quality_pro) + ',' + str(avg_alignment_pro) + ',' + str(avg_usefulness_pro) + '\n'
            f2.write(outline2)
"""
    f1.close()    
    f2.close()