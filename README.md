# humanize-kit · 去 AI 味 · 让 AI 文本读起来像人写的

把 AI 生成的文本改写成"读起来像正常人类写的"：清理套话、铺垫、拔高和模板句式，**不改事实、不编数据、保留作者口气与确定程度**。中英双语，中文优先。既是一个可直接使用的 Agent Skill（`SKILL.md`），也是一套带评测闭环的项目骨架。

> 定位：编辑工具，不是检测工具，也不承诺绕过任何 AI 检测器。目标读者是「想要稿子更耐读」的人。

## 设计原则（从 10 个参考项目提炼）

1. **先保信息，再谈风格。** 数字、日期、条件、否定、情态、归属、承诺是硬边界，风格处理永远在其后。（shuorenhua、Humanizer-zh）
2. **不编造。** 原文没有的细节不能补；缺事实就问，不靠润色脑补。（humanizer、De-AI）
3. **保留确定程度。** "可能"不变"确定"，"计划"不变"已经"；否定与条件范围不动。（Humanizer-zh）
4. **模式是提醒，不是规则。** 编辑按内容判断，不按词语命中次数替换；真实术语、引语、刻意排比可保留。（Humanizer-zh v2、shuorenhua v2.5）
5. **正常文本可以不改。** 不需要每次调用都产生修改。（shuorenhua）
6. **声音可校准。** 提供作者样本时按样本的节奏、用词、标点习惯改写，但不搬样本的经历与观点。（humanizer voice matching → `references/style-dna.md`）
7. **评测闭环。** 保真硬检查 + 盲测 + 误改率门槛，缺一不可。（shuorenhua 评测门槛、HC3 语料基线、stop-slop 评分法）

## 调研：10 个参考仓库 → 本项目吸收了什么

| 项目                                                                                                                                | 定位                                                                | 本项目吸收                                                                                         |
| ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| [blader/humanizer](https://github.com/blader/humanizer)（54k★）                                                                     | 英文去 AI 味 skill，基于 Wikipedia「Signs of AI writing」的 26 模式 | 模式分类骨架 A–E（`patterns.md`）、工作流（诊断→起草→校验→终稿）、不编造原则、声音匹配             |
| [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh)（19k★）                                                               | humanizer 汉化，31 检查点，含中文特有 F 类                          | F 类 26–31（长定语 / 进行+动词 / 被字句堆叠 / 四字词排比 / 万能背景 / 套话收尾）、保留边界体系     |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop)（18k★）                                                         | 英文反 slop：禁用词、结构套路、句式级规则 + 5 维评分                | 5 维评分法（<35/50 重写，见 `eval/criteria.md`）、句式规则（无 Wh- 句首、主动语态）、结构清单      |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)（93k★）                                                             | 反 slop「品味」框架（前端向）                                       | 反平庸理念；「可调参数」思想 → 本项目的改动范围档位                                                |
| [hylarucoder/ai-flavor-remover](https://github.com/hylarucoder/ai-flavor-remover)（1.2k★）                                          | 中文 AI 味去除提示词（推理模型）                                    | 角色化工作流与输出格式（诊断→策略→亮点→成稿）                                                      |
| [MrGeDiao/shuorenhua](https://github.com/MrGeDiao/shuorenhua)（2k★）                                                                | 中文优先保真改写 skill，场景化 + 评测闭环                           | 保真优先级、改动范围四档（structural/bounded/in-place/只标问题）、发布门槛（硬失败=0、误改率<10%） |
| [alchaincyf/nuwa-skill](https://github.com/alchaincyf/nuwa-skill)（34k★）                                                           | 思维/表达蒸馏                                                       | 表达 DNA 分层（怎么说话/怎么想/怎么判断/什么不做）→ `style-dna.md`                                 |
| [dongbeixiaohuo/writing-agent](https://github.com/dongbeixiaohuo/writing-agent)（435★）                                             | 多智能体写作，15 维风格建模                                         | 15 维风格模型 → `style-dna.md`                                                                     |
| [Hello-SimpleAI/chatgpt-comparison-detection](https://github.com/Hello-SimpleAI/chatgpt-comparison-detection)（1.5k★）              | HC3 人类/机器对照语料 + 检测器                                      | 评测基线：indicating words 特征词、人类/机器对照语料                                               |
| [OUBIGFA/De-AI-Prompt-Enhancer-Writer-Booster-SKILL](https://github.com/OUBIGFA/De-AI-Prompt-Enhancer-Writer-Booster-SKILL)（850★） | 中文去 AI 味提示词包，24 项痕迹检测 + 风格复现                      | 24 项痕迹体系、保真改写护栏、七大铁律、风格审计脚本思想                                            |

## 目录结构

```
humanize-kit/
├── README.md                 # 本文件：定位、原则、调研表
├── LICENSE                   # MIT 许可证（主体）
├── NOTICE                    # 第三方版权声明与 CC BY-SA 例外
├── SKILL.md                  # 核心技能：31 项模式 + 原则 + 工作流 + 模式档位（可直接装为 skill）
├── references/
│   ├── patterns.md           # 31 项模式详解：识别/例子/改法/保留边界
│   ├── phrases.md            # 中英高频 AI 词表（含「何时保留」）
│   ├── structures.md         # ≥10 种结构套路
│   ├── examples.md           # 8 组改写对照 + 1 组「不该改」反例
│   ├── style-dna.md          # 风格 DNA 提炼：分层 + 工作流 + 风格卡模板
│   └── scene-guardrails.md   # 场景护栏：改动范围档位 + 9 类场景
├── eval/
│   ├── README.md             # 评测方法论（硬失败/盲测/误改率）
│   ├── criteria.md           # 5 维评分 + 保真清单
│   └── cases/
│       ├── positive.md       # 待改善的 AI 味文本
│       └── negative.md       # 正常人类文本（误改率基线）
└── scripts/
    └── score.py              # 保真度硬检查 + AI 痕迹扫描 + 节奏统计
```

## 快速开始

### 安装 Skill

```bash
# 通用（Agent Skills 协议，支持 Claude Code / Codex / Cursor 等 50+ runtime）
npx skills add https://github.com/FourLeafTec/humanize-kit

# 或手动：把仓库复制到 runtime 的 skills 目录（如 ~/.claude/skills/humanize-kit/）
```

### 用法

```
请用 humanize-kit 清理这段的 AI 味：[粘贴文本]
只标问题，不改写：[文本]
改 references/README.md 里的正文，保留结构：structural
按我的样本口气改写：[样本 2-3 段] + [待改文本]
```

默认只交付最终稿。不需要修改时返回原文。代码块、命令、路径、链接目标、YAML、数据默认不动。

### 跑检查脚本

```bash
python3 scripts/score.py scan eval/cases/positive.md    # 扫描 AI 痕迹
python3 scripts/score.py diff 原文.txt 改稿.txt          # 保真度 + 痕迹对比
```

## 评测

见 [eval/README.md](eval/README.md)。当前为骨架：方法、判据与样例已就位，等待首轮模型改写评测；`score.py` 提供自动化的保真硬检查（数字/日期丢失即失败）。

## 参考项目许可

参考项目按许可证分三类，引用内容已在各文件注明来源：

- **MIT（7 个）**：blader/humanizer、op7418/Humanizer-zh、hardikpandya/stop-slop、Leonxlnx/taste-skill、MrGeDiao/shuorenhua、alchaincyf/nuwa-skill、dongbeixiaohuo/writing-agent。本项目改编自其思路/内容的部分随仓库以 MIT 发布；第三方版权声明见 [NOTICE](NOTICE)。
- **CC BY-SA 4.0（1 个）**：Hello-SimpleAI/chatgpt-comparison-detection（HC3 语料）。`references/phrases.md` 第三节的摘录以 CC BY-SA 4.0 授权，**不属于本仓库的 MIT 部分**。
- **未声明许可证（2 个）**：hylarucoder/ai-flavor-remover、OUBIGFA/De-AI-Prompt-Enhancer-Writer-Booster-SKILL（默认保留所有权利）。本项目仅借鉴其思想与常见短语，未复制其原创表达。

本项目主体以 **MIT** 发布，见 [LICENSE](LICENSE)。
