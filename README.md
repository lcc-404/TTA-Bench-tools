# 📦 TTA-Bench-tools

> A comprehensive benchmark for text-to-audio (TTA) generation evaluation.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)]()
[![Paper](https://img.shields.io/badge/Paper-arXiv%3A2501.12345-b31b1b.svg)](https://jiusansan222.github.io/tta-bench/)
[![Project Page](https://img.shields.io/badge/Project-Website-blue.svg)](https://jiusansan222.github.io/tta-bench/)


---

## 📖 Overview

Text-to-Audio (TTA) generation has made rapid progress, but current evaluation methods remain narrow, focusing mainly on perceptual quality while overlooking robustness, generalization, and ethical concerns. We present TTA-Bench, a comprehensive benchmark for evaluating TTA models across functional performance, reliability, and social responsibility. It covers seven dimensions including accuracy, robustness, fairness, and toxicity, and includes 2,999 diverse prompts generated through automated and manual methods. We introduce a unified evaluation protocol that combines objective metrics with over 118,000 human annotations from both experts and general users. Ten state-of-the-art models are benchmarked under this framework, offering detailed insights into their strengths and limitations. TTA-Bench establishes a new standard for holistic and responsible evaluation of TTA systems. The dataset, evaluation tools, and results are available at [TTA-Bench](https://jiusansan222.github.io/tta-bench).

---

## 🚀 Getting Started

### 0. Clone the repository

```bash
git clone https://github.com/lcc-404/TTA-Bench-tools.git
cd ./TTA-Bench-tools
```
###  Prepare input in Audiobox-aesthetic style
```bash
sh prepare_input.sh
```

### 2. Calculate AES scores
```bash
sh cal_aes.sh
```
You will get AES scores both in system-level for both dimension and attributess.


### 3. Calculate CLAP scores
```bash
sh cal_clap.sh
```
You will get AES scores both in system-level for both dimension and attributess.


## 🙏 Acknowledgements

We would like to thank the following projects, datasets, and contributors that made this work possible:

- [Audiobox-aesthetic](https://github.com/facebookresearch/audiobox-aesthetics)
- [CLAP](https://github.com/microsoft/CLAP)


