from msclap import CLAP
import json
from typing import List
import torch
import os
os.environ["CUDA_VISIBLE_DEVICES"]='1'

# prompt file path
ACC_PROMPT_PATH = "/home/liucheng/project/tta-benchmark/prompt/acc_prompt.json"
GENERAL_PROMPT_PATH = "/home/liucheng/project/tta-benchmark/prompt/generalization_prompt.json"
ROBUSTNESS_PROMPT_PATH = "/home/liucheng/project/tta-benchmark/prompt/robustness_prompt.json"
FAIRNESS_PROMPT_PATH = "/home/liucheng/project/tta-benchmark/prompt/fairness_prompt_new.json"

def load_prompts(prompt_path: str) -> dict:
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompts = json.load(f)
    return {prompt['id']: prompt['prompt_text'] for prompt in prompts}

# prompts字典,key:"prompt_0001", value:"text description"
acc_prompts = load_prompts(ACC_PROMPT_PATH)
general_prompts = load_prompts(GENERAL_PROMPT_PATH)
robustness_prompts = load_prompts(ROBUSTNESS_PROMPT_PATH)
fairness_prompts = load_prompts(FAIRNESS_PROMPT_PATH)

def get_prompt_text(prompt_id: str) -> str:
    if 1 <= int(prompt_id) <= 1500:
        return acc_prompts[f"prompt_{prompt_id}"]
    elif 1501 <= int(prompt_id) <= 1800:
        return general_prompts[f"prompt_{prompt_id}"]
    elif 1801 <= int(prompt_id) <= 2100:
        return robustness_prompts[f"prompt_{prompt_id}"]
    elif 2101 <= int(prompt_id) <= 2400:
        return fairness_prompts[f"prompt_{prompt_id}"]
    else:
        raise ValueError(f"Invalid prompt ID: {prompt_id}")

def cal_clap_score_for_jsonl(input_jsonl_path: str, result_jsonl: str):
    clap_model = CLAP(version='2023', use_cuda=True)

    with open(input_jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            file_path = data['path']    
            # "/home/liucheng/project/tta-benchmark/samples/stable_audio/robustness/S008_P2041.wav"
            # get prompt text
            prompt_id = file_path.split('/')[-1].split('_')[1].replace('.wav', '').replace("P","")  # "0001"
            prompt_text = get_prompt_text(prompt_id)
            
            # get audio_embeddings,text_embeddings
            audio_embedding = clap_model.get_audio_embeddings([file_path])
            text_embedding = clap_model.get_text_embeddings([prompt_text])

            similarity_score = torch.nn.functional.cosine_similarity(audio_embedding, text_embedding).item()
            print(f"similarity_score: {similarity_score}")

            # 写output:jsonl, {"CLAP": xxx}
            with open(result_jsonl, 'a', encoding='utf-8') as outfile:
                json.dump({"CLAP":similarity_score}, outfile)
                outfile.write('\n')


if __name__ == "__main__":
    SYS_NANE=[
    "audiogen","magnet","stable_audio","make_an_audio","make_an_audio_2",
    "audioldm-l-full","audioldm2-large","auffusion-full","tango-full","tango2-full"
    ]
    
    EVAL_DIM=[
        "fairness","acc","generalization","robustness",
    ]

    for sys_name in SYS_NANE:
        for eval_dim in EVAL_DIM:
            temp = sys_name + '_' + eval_dim
            input_jsonl = f'/home/liucheng/project/tta-benchmark/audiobox-aesthetics/prepared_jsonl/{temp}.jsonl'
            result_jsonl = f'/home/liucheng/project/tta-benchmark/audiobox-aesthetics/clap_results/{temp}.jsonl'
            print(f"====={temp}=====")
            cal_clap_score_for_jsonl(input_jsonl, result_jsonl)

