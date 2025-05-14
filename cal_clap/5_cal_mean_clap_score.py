import json

SYS_NANE=[
    "audiogen","magnet","stable_audio","make_an_audio","make_an_audio_2",
    "audioldm-l-full","audioldm2-large","auffusion-full","tango-full","tango2-full"
    ]
EVAL_DIM=["acc","generalization","robustness","fairness"]

outfile = "./clap_results/result.txt"

f = open(outfile,'w')
for sys_name in SYS_NANE:
    for eval_dim in EVAL_DIM:
        # 指定系统、指定维度的所有wav文件的AES结果路径
        temp = sys_name + '_' + eval_dim
        result_jsonl = f'/home/liucheng/project/tta-benchmark/audiobox-aesthetics/clap_results/{temp}.jsonl'
        print(f"====={temp}=====")

        # 初始化变量
        total_clap = 0
        count = 0

        # 读取文件并计算总和
        with open(result_jsonl, 'r') as file:
            for line in file:
                # print(line)
                data = json.loads(line)  # 解析每一行的 JSON 数据
                total_clap += data['CLAP']
                count += 1

        # 计算平均值
        if count > 0:
            avg_clap = total_clap / count
        else:
            avg_clap = 0

        # 输出结果
        print(f"count:{count}")
        print(f"Average CLAP: {avg_clap}")
        outline = str(temp) + '\n' + str(avg_clap) + '\n'
        f.write(outline)

f.close()