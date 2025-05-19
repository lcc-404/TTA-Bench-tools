import json
# prompt file path
ACC_PROMPT_PATH = "/home/liucheng/project/tta-benchmark/prompt/acc_prompt.json"
GENERAL_PROMPT_PATH = "/home/liucheng/project/tta-benchmark/prompt/generalization_prompt.json"
ROBUSTNESS_PROMPT_PATH = "/home/liucheng/project/tta-benchmark/prompt/robustness_prompt.json"
FAIRNESS_PROMPT_PATH = "/home/liucheng/project/tta-benchmark/prompt/fairness_prompt_new.json"

def load_prompts(prompt_path: str, target_field: str) -> dict:
    """加载prompt文件中的目标字段"""
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompts = json.load(f)
    return {prompt_data['id']: prompt_data[target_field] for prompt_data in prompts}

# key:prompt_id, value:attribute of dimension, e.g. "prompt_0001":"2" / "prompt_1801":"uppercase"
acc_event_count_map = load_prompts(ACC_PROMPT_PATH, "event_count")
acc_event_relation_map = load_prompts(ACC_PROMPT_PATH, "event_relation")
general_event_count_map = load_prompts(GENERAL_PROMPT_PATH, "event_count")
robustness_type_map = load_prompts(ROBUSTNESS_PROMPT_PATH, "perturbation_type")
fairness_type_map = load_prompts(FAIRNESS_PROMPT_PATH, "notes")

def get_prompt_attr(prompt_id: str) -> str:
    if 1 <= int(prompt_id) <= 1500:
        return acc_event_count_map[f"prompt_{prompt_id}"], acc_event_relation_map[f"prompt_{prompt_id}"]
    elif 1501 <= int(prompt_id) <= 1800:
        return general_event_count_map[f"prompt_{prompt_id}"]
    elif 1801 <= int(prompt_id) <= 2100:
        return robustness_type_map[f"prompt_{prompt_id}"]
    elif 2101 <= int(prompt_id) <= 2400:
        return fairness_type_map[f"prompt_{prompt_id}"]
    else:
        raise ValueError(f"Invalid prompt ID: {prompt_id}")
    
SYS_NANE=[
    "audiogen",
    "magnet","stable_audio","make_an_audio","make_an_audio_2",
    "audioldm-l-full","audioldm2-large","auffusion-full","tango-full","tango2-full"
]
EVAL_DIM=[
    "acc",
    "generalization",
    "robustness",
    "fairness"
]

output_txt = f'/home/liucheng/project/tta-benchmark/audiobox-aesthetics/clap_results/clap_attribute_results.txt'  # 输出文件路径

if __name__ == "__main__":

    for sys_name in SYS_NANE:
        for eval_dim in EVAL_DIM:
            temp = sys_name + '_' + eval_dim
            """
            e.g.
            audiogen_acc
            audioldm_robustness
            """
            input_jsonl = f'/home/liucheng/project/tta-benchmark/audiobox-aesthetics/prepared_jsonl/{temp}.jsonl'
            score_jsonl = f'/home/liucheng/project/tta-benchmark/audiobox-aesthetics/clap_results/{temp}.jsonl'

            results = {}
            # key:prompt_attr
            # value: dict{key:total_clap'/'count', value: int}

            with open(input_jsonl, 'r') as input_file, open(score_jsonl, 'r') as score_file:
                for input_line, score_line in zip(input_file, score_file):
                    input_data = json.loads(input_line)  # {"path": "/home/liucheng/project/tta-benchmark/samples/audiogen/acc/S001_P0422.wav"}
                    score_data = json.loads(score_line)  # {"CLAP": 18.195480346679688}

                    file_path = input_data['path']

                    prompt_id = file_path.split('/')[-1].split('_')[1].replace('.wav', '').replace("P","")  # "0001"
                    prompt_attr = get_prompt_attr(prompt_id)
                    # print("prompt_id:", prompt_id, ",prompt_attr:", prompt_attr)

                    if prompt_attr not in results:
                        results[prompt_attr] = {
                            'total_clap': 0,
                            'count': 0
                        }

                    results[prompt_attr]['total_clap'] += score_data['CLAP']
                    results[prompt_attr]['count'] += 1

            with open(output_txt, 'a') as output_file:
                for attr, data in results.items():
                    count = data['count']
                    if count > 0:
                        avg_clap = data['total_clap'] / count
                    else:
                        avg_clap = 0

                    print(f"====={temp}_{attr}=====")
                    print(f"count:{count}")
                    print(f"Average CLAP: {avg_clap}")

                    output_file.write(f"====={temp}_{attr}=====\n")
                    output_file.write(f"count: {count}\n")
                    output_file.write(f"Average CLAP: {avg_clap}\n")
                    output_file.write("\n")
