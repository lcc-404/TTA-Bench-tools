import os
import json

def find_wav_files(directory):
    wav_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.wav'):
                wav_files.append(os.path.join(root, file))
    return wav_files

def save_to_jsonl(file_list, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for file_path in file_list:
            json_line = json.dumps({"path": file_path})
            f.write(json_line + '\n')

if __name__ == "__main__":
    SAMPLE_PATH= '/home/liucheng/project/tta-benchmark/samples'

    SYS_NANE={
        "audioldm-l-full","audioldm2-large","auffusion-full","tango-full","tango2-full"
    }
    
    EVAL_DIM=[
        "acc","generalization","robustness","fairness"
    ]

    for sys_name in SYS_NANE:
        for eval_dim in EVAL_DIM:
            search_directory = f'{SAMPLE_PATH}/{sys_name}/{eval_dim}'
            # The output JSONL file path contains all wav file paths of the specified system and specified dimensions
            output_jsonl_file = f'/home/liucheng/project/tta-benchmark/audiobox-aesthetics/prepared_jsonl/{sys_name}_{eval_dim}.jsonl'

            wav_files = find_wav_files(search_directory)
            print(f"Found {len(wav_files)} files.")

            # 保存为 JSONL 文件
            save_to_jsonl(wav_files, output_jsonl_file)
            print(f"Files are saved at {output_jsonl_file}")