import os
import json

def find_wav_files(directory):
    """
    在指定目录及其子目录中查找所有 .wav 文件。

    :param directory: 要搜索的目录路径
    :return: 包含所有 .wav 文件路径的列表
    """
    wav_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.wav'):
                wav_files.append(os.path.join(root, file))
    return wav_files

def save_to_jsonl(file_list, output_file):
    """
    将文件路径列表保存为 JSONL 文件。

    :param file_list: 包含文件路径的列表
    :param output_file: 输出的 JSONL 文件路径
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for file_path in file_list:
            json_line = json.dumps({"path": file_path})
            f.write(json_line + '\n')

if __name__ == "__main__":
    SAMPLE_PATH= '/home/liucheng/project/tta-benchmark/samples'
    # SYS_NANE=[
    #     "audiogen","magnet","make_an_audio","make_an_audio_2","stable_audio"
    # ]

    SYS_NANE={
        "audioldm-l-full","audioldm2-large","auffusion-full","tango-full","tango2-full"
    }
    
    EVAL_DIM=[
        "acc","generalization","robustness","fairness"
    ]

    for sys_name in SYS_NANE:
        for eval_dim in EVAL_DIM:
            # 指定系统、指定维度的目标音频路径
            search_directory = f'{SAMPLE_PATH}/{sys_name}/{eval_dim}'
            # 输出的 JSONL 文件路径,包含指定系统、指定维度的所有wav文件路径
            output_jsonl_file = f'/home/liucheng/project/tta-benchmark/audiobox-aesthetics/prepared_jsonl/{sys_name}_{eval_dim}.jsonl'

            # 查找所有 .wav 文件
            wav_files = find_wav_files(search_directory)
            print(f"找到 {len(wav_files)} 个 .wav 文件。")

            # 保存为 JSONL 文件
            save_to_jsonl(wav_files, output_jsonl_file)
            print(f"文件路径已保存到 {output_jsonl_file}")