from msclap import CLAP
import json
from typing import List
import torch
import os
os.environ["CUDA_VISIBLE_DEVICES"]='1'

# prompt文件路径
ACC_PROMPT_PATH = "/home/liucheng/project/tta-benchmark/prompt/acc_prompt.json"
GENERAL_PROMPT_PATH = "/home/liucheng/project/tta-benchmark/prompt/generalization_prompt.json"
ROBUSTNESS_PROMPT_PATH = "/home/liucheng/project/tta-benchmark/prompt/robustness_prompt.json"
FAIRNESS_PROMPT_PATH = "/home/liucheng/project/tta-benchmark/prompt/fairness_prompt_new.json"

def load_prompts(prompt_path: str) -> dict:
    """加载prompt文件"""
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompts = json.load(f)
    return {prompt['id']: prompt['prompt_text'] for prompt in prompts}

# prompts字典,key:"prompt_0001", value:"text description"
acc_prompts = load_prompts(ACC_PROMPT_PATH)
general_prompts = load_prompts(GENERAL_PROMPT_PATH)
robustness_prompts = load_prompts(ROBUSTNESS_PROMPT_PATH)
fairness_prompts = load_prompts(FAIRNESS_PROMPT_PATH)

def get_prompt_text(prompt_id: str) -> str:
    """根据prompt编号获取对应的prompt文本"""
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

    # 按行读取jsonl文件
    with open(input_jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            file_path = data['path']    # "/home/liucheng/project/tta-benchmark/samples/stable_audio/robustness/S008_P2041.wav"
            # 提取prompt编号
            prompt_id = file_path.split('/')[-1].split('_')[1].replace('.wav', '').replace("P","")  # "0001"
            # 获取对应的prompt文本
            prompt_text = get_prompt_text(prompt_id)
            
            # 计算audio_embeddings
            audio_embedding = clap_model.get_audio_embeddings([file_path])
            # 计算text_embeddings
            text_embedding = clap_model.get_text_embeddings([prompt_text])
            # 计算相似度
            similarity_score = torch.nn.functional.cosine_similarity(audio_embedding, text_embedding).item()
            print(f"similarity_score: {similarity_score}")

            # 写jsonl，每行形如{"CLAP": xxx}
            # 模式为'a'，如果需要重跑，则需要先把所有文件删除
            with open(result_jsonl, 'a', encoding='utf-8') as outfile:
                json.dump({"CLAP":similarity_score}, outfile)
                outfile.write('\n')  # 每行结束后换行


if __name__ == "__main__":
    SYS_NANE=[
    "audiogen","magnet","stable_audio","make_an_audio","make_an_audio_2",
    "audioldm-l-full","audioldm2-large","auffusion-full","tango-full","tango2-full"
    ]
    
    EVAL_DIM=[
        "fairness","acc","generalization","robustness",
    ]

    # Load model (Choose between versions '2022' or '2023')
    # The model weight will be downloaded automatically if `model_fp` is not specified

    for sys_name in SYS_NANE:
        for eval_dim in EVAL_DIM:
            # 包含指定系统、指定维度的所有wav文件路径的JSONL 文件
            temp = sys_name + '_' + eval_dim
            input_jsonl = f'/home/liucheng/project/tta-benchmark/audiobox-aesthetics/prepared_jsonl/{temp}.jsonl'
            result_jsonl = f'/home/liucheng/project/tta-benchmark/audiobox-aesthetics/clap_results/{temp}.jsonl'
            print(f"====={temp}=====")
            cal_clap_score_for_jsonl(input_jsonl, result_jsonl)

