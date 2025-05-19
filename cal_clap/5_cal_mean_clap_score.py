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
        temp = sys_name + '_' + eval_dim
        result_jsonl = f'/home/liucheng/project/tta-benchmark/audiobox-aesthetics/clap_results/{temp}.jsonl'
        print(f"====={temp}=====")

        total_clap = 0
        count = 0

        with open(result_jsonl, 'r') as file:
            for line in file:
                # print(line)
                data = json.loads(line)
                total_clap += data['CLAP']
                count += 1

        if count > 0:
            avg_clap = total_clap / count
        else:
            avg_clap = 0

        print(f"count:{count}")
        print(f"Average CLAP: {avg_clap}")
        outline = str(temp) + '\n' + str(avg_clap) + '\n'
        f.write(outline)

f.close()