import os
os.environ["CUDA_VISIBLE_DEVICES"]='0'

if __name__ == "__main__":
    SYS_NANE=[
    "audiogen","magnet","stable_audio","make_an_audio","make_an_audio_2",
    "audioldm-l-full","audioldm2-large","auffusion-full","tango-full","tango2-full"
    ]
    
    EVAL_DIM=[
        "acc","generalization","robustness","fairness"
    ]

    for sys_name in SYS_NANE:
        for eval_dim in EVAL_DIM:

            temp = sys_name + '_' + eval_dim
            input_jsonl = f'/home/liucheng/project/tta-benchmark/audiobox-aesthetics/prepared_jsonl/{temp}.jsonl'
            result_jsonl = f'/home/liucheng/project/tta-benchmark/audiobox-aesthetics/aes_results/{temp}.jsonl'

            os.system(f'audio-aes {input_jsonl} --batch-size 50 > {result_jsonl}')
            print(f"AES results of {temp} are saved at {result_jsonl}")
