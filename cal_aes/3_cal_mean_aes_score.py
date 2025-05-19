import json

SYS_NANE=[
    "audiogen","magnet","stable_audio","make_an_audio","make_an_audio_2",
    "audioldm-l-full","audioldm2-large","auffusion-full","tango-full","tango2-full"
    ]

    
EVAL_DIM=["acc","generalization","robustness","fairness"]

outfile = "./aes_results/result.txt"
f = open(outfile,'w')
for sys_name in SYS_NANE:
    for eval_dim in EVAL_DIM:
        temp = sys_name + '_' + eval_dim
        result_jsonl = f'/home/liucheng/project/tta-benchmark/audiobox-aesthetics/aes_results/{temp}.jsonl'

        total_ce = 0
        total_cu = 0
        total_pc = 0
        total_pq = 0
        count = 0

        with open(result_jsonl, 'r') as file:
            for line in file:
                data = json.loads(line)
                total_ce += data['CE']
                total_cu += data['CU']
                total_pc += data['PC']
                total_pq += data['PQ']
                count += 1

        if count > 0:
            avg_ce = total_ce / count
            avg_cu = total_cu / count
            avg_pc = total_pc / count
            avg_pq = total_pq / count
        else:
            avg_ce = avg_cu = avg_pc = avg_pq = 0

    
        print(f"====={temp}=====")
        print(f"count:{count}")
        print(f"Average CE: {avg_ce}")
        print(f"Average CU: {avg_cu}")
        print(f"Average PC: {avg_pc}")
        print(f"Average PQ: {avg_pq}")
        outline = str(temp) + '\n' + str(avg_ce) + ',' + str(avg_cu) + ',' + str(avg_pc) + ',' + str(avg_pq) + '\n'
        f.write(outline)
f.close()