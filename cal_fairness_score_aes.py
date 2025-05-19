import numpy as np
import itertools
import re
import time
def compute_fairness_score(A):
    """
    计算公平性得分。
    
    参数:
        A: list or numpy array, 每个子群体的得分 A(i)
    
    返回:
        fairness_score: float
    """
    A = np.array(A)
    Ns = len(A)
    if Ns < 2:
        return 0.0  # 少于两个子群体无法计算公平性

    total = 0.0
    count = 0

    for i, j in itertools.combinations(range(Ns), 2):
        diff = abs(A[i] - A[j])
        max_val = max(A[i], A[j])
        if max_val > 0:
            total += (100 * diff) / max_val
        count += 1

    fairness_score = total / count if count > 0 else 0.0
    return fairness_score


if __name__ == "__main__":

    # 定义系统名称和属性名称
    sysnames = [
        "audiogen", "magnet", "stable_audio", "make_an_audio", "make_an_audio_2",
        "audioldm-l-full", "audioldm2-large", "auffusion-full", "tango-full", "tango2-full"
    ]
    attributes = ["gender", "age", "language"]

    # 初始化结果列表
    results = []

    # 打开并读取文件
    filename = "/home/liucheng/project/tta-benchmark/audiobox-aesthetics/aes_results/aes_attribute_results.txt"  # 替换为你的文件名
    with open(filename, "r") as file:
        content = file.read()

    # 按段落分割内容（每段之间有一个空行）
    sections = content.strip().split("\n\n")

    # 遍历每个段落
    for section in sections:
        # time.sleep(10)
        # 使用正则表达式匹配段落中的关键信息
        match = re.search(
            r"=====(?P<sysname>[a-zA-Z0-9_-]+)_fairness_(?P<attribute>\w+)=====\s*"
            r"count: \d+\s*"
            r"Average CE: \d+\.\d+\s*"
            r"Average CU: \d+\.\d+\s*"
            r"Average PC: \d+\.\d+\s*"
            r"Average PQ: (?P<pq_value>\d+\.\d+)",
            section
        )
        # print(match)
        if match:
            # print(section)
            sysname = match.group("sysname")
            attribute = match.group("attribute")
            pq_value = float(match.group("pq_value"))
            
            # 将结果存储到列表中
            results.append((sysname, attribute, pq_value))

    # 打印结果
    for result in results:
        print(result)

    # 初始化一个字典，用于存储每个系统的分数
    system_scores = {}

    # 遍历结果列表
    for sysname, attribute, pq_value in results:
        if sysname not in system_scores:
            system_scores[sysname] = {
                'gender_scores':[],
                'age_scores': [],
                'language_scores': []
            }
        
        if attribute in ['male', 'female']:
            system_scores[sysname]['gender_scores'].append(pq_value)
        elif attribute in ['old', 'middle', 'youth', 'child']:
            system_scores[sysname]['age_scores'].append(pq_value)
        elif attribute in ['en', 'zh', 'other']:
            system_scores[sysname]['language_scores'].append(pq_value)

    # 打印结果
    for sysname, scores in system_scores.items():
        print(f"System: {sysname}")
        # print("Gender Scores:", scores['gender_scores'])
        # print("Age Scores:", scores['age_scores'])
        # print("Language Scores:", scores['language_scores'])
        # print()
        fairness1 = compute_fairness_score(scores['gender_scores'])
        fairness2 = compute_fairness_score(scores['age_scores'])
        fairness3 = compute_fairness_score(scores['language_scores'])

        print(f"Gender Fairness Score: {fairness1:.2f}")
        print(f"Age Fairness Score: {fairness2:.2f}")
        print(f"Language Fairness Score: {fairness3:.2f}")

        # 如果需要，可以将结果存储到一个文件中
        with open("fs_result_aes.txt", "a") as output_file:
            output_file.write(f"{sysname}, '\n', {fairness1}, {fairness2}, {fairness3}\n")