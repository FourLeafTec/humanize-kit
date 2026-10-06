#!/usr/bin/env python3
"""humanize-kit · 保真度与 AI 痕迹检查器

用法:
  python3 scripts/score.py scan <文本文件>             # 只做痕迹扫描
  python3 scripts/score.py diff <原文> <改稿>          # 保真度 + 痕迹对比
  python3 scripts/score.py diff <原文> <改稿> --json  # 机器可读输出

退出码: 0 = 通过(无硬失败); 1 = 硬失败(数字/日期丢失); 2 = 用法错误

说明:
- 内置词表是精选子集，完整清单见 references/phrases.md。
- 数字提取是启发式的：日期、百分比、金额、普通数字；版本号（如 v2.5.1）
  会被拆出多个数字，属已知噪音，人工复核即可。
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

# 内置精简词表（完整清单见 references/phrases.md；按模式编号标注）
TELLS_ZH = [
    # C12 空泛高频词
    "赋能", "抓手", "闭环", "彰显", "深耕", "破圈", "落地", "凸显", "助力",
    # A4/E/F31 铺垫与套话
    "值得注意的是", "不难发现", "综上所述", "总而言之", "总的来说", "让我们",
    "让我们共同期待", "展望未来", "在当今", "随着", "毋庸置疑",
    # E22 客服腔
    "希望以上内容", "希望这个回答", "问得好",
]
TELLS_EN = [
    # C12 空泛高频词
    "delve", "testament", "landscape", "showcase", "tapestry", "foster",
    "leverage", "seamless", "revolutionize", "game-changer", "cutting-edge",
    "moreover", "furthermore", "it is important to note", "in conclusion",
    "let's dive", "at its core", "let that sink in",
]


def extract_numeric(text: str) -> set[str]:
    """提取数字/日期/百分比/金额（启发式，返回去重集合）。"""
    pats = [
        # 日期：2026-10-06 / 2026/10/6 / 2026年10月6日 / 2026年
        r"\d{4}[-/年.]\d{1,2}(?:[-/月.]\d{1,2}日?)?",
        # 数字：普通整数/小数，可带 % 或货币前缀
        r"(?:¥|\$|￥)?\d+(?:\.\d+)?\s*%?",
    ]
    out: set[str] = set()
    for p in pats:
        out.update(re.findall(p, text))
    return out


def split_sentences(text: str) -> list[str]:
    """按中文句读与换行切句；英文句点后跟空白视为句尾。"""
    t = re.sub(r"\.(?=\s|$)", "。", text)
    return [s.strip() for s in re.split(r"[。！？!?；\n]", t) if s.strip()]


def count_tells(text: str) -> dict[str, int]:
    """统计命中词表的出现次数（长词优先，避免子串重叠双计）。"""
    hits: dict[str, int] = {}
    covered: list[tuple[int, int]] = []
    for w in sorted(TELLS_ZH + TELLS_EN, key=len, reverse=True):
        n = 0
        start = 0
        while True:
            i = text.find(w, start)
            if i < 0:
                break
            if any(i < end and i + len(w) > s for s, end in covered):
                start = i + 1
                continue
            covered.append((i, i + len(w)))
            n += 1
            start = i + len(w)
        if n:
            hits[w] = n
    return hits


def rhythm_std(text: str) -> float:
    """句长标准差：AI 匀速文本偏低，人类文本通常更高（仅信号，非结论）。"""
    lens = [len(s) for s in split_sentences(text)]
    if len(lens) < 2:
        return 0.0
    return round(statistics.stdev(lens), 2)


def passive_zh(text: str) -> int:
    return text.count("被")


def scan_text(text: str) -> dict:
    tells = count_tells(text)
    return {
        "chars": len(text),
        "sentences": len(split_sentences(text)),
        "rhythm_std": rhythm_std(text),
        "passive_zh": passive_zh(text),
        "tells": tells,
        "tells_total": sum(tells.values()),
        "numeric_tokens": sorted(extract_numeric(text)),
    }


def diff_texts(before: str, after: str) -> dict:
    b, a = scan_text(before), scan_text(after)
    missing = sorted(set(b["numeric_tokens"]) - set(a["numeric_tokens"]))
    removed_tells = {w: n for w, n in b["tells"].items() if a["tells"].get(w, 0) < n}
    added_tells = {w: n for w, n in a["tells"].items() if b["tells"].get(w, 0) < n}
    return {
        "before": b,
        "after": a,
        "missing_numbers": missing,
        "removed_tells": removed_tells,
        "added_tells": added_tells,
        "hard_fail": bool(missing),
    }


def print_report(r: dict, json_out: bool) -> int:
    if json_out:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 1 if r["hard_fail"] else 0

    b, a = r["before"], r["after"]
    print("== 原文 ==")
    print(f"  字数 {b['chars']} | 句数 {b['sentences']} | 节奏方差 {b['rhythm_std']} | 被字句 {b['passive_zh']}")
    print(f"  痕迹词 {b['tells_total']} 处: {b['tells'] or '无'}")
    print("== 改稿 ==")
    print(f"  字数 {a['chars']} | 句数 {a['sentences']} | 节奏方差 {a['rhythm_std']} | 被字句 {a['passive_zh']}")
    print(f"  痕迹词 {a['tells_total']} 处: {a['tells'] or '无'}")
    print("== 保真检查 ==")
    if r["missing_numbers"]:
        print(f"  ✗ 硬失败：原文出现但改稿丢失的数字/日期: {r['missing_numbers']}")
    else:
        print("  ✓ 数字/日期全部保留")
    if r["removed_tells"]:
        print(f"  - 清除的痕迹词: {r['removed_tells']}")
    if r["added_tells"]:
        print(f"  + 新增的痕迹词: {r['added_tells']}")
    delta = round((a["chars"] - b["chars"]) / max(b["chars"], 1) * 100, 1)
    print(f"  字数变化 {delta:+.1f}%")
    return 1 if r["hard_fail"] else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="humanize-kit 保真度与 AI 痕迹检查器")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_scan = sub.add_parser("scan", help="只扫描文本的 AI 痕迹")
    p_scan.add_argument("file")
    p_diff = sub.add_parser("diff", help="对比原文与改稿")
    p_diff.add_argument("before")
    p_diff.add_argument("after")
    p_diff.add_argument("--json", action="store_true")
    args = ap.parse_args()

    try:
        if args.cmd == "scan":
            text = Path(args.file).read_text(encoding="utf-8")
            s = scan_text(text)
            print(f"文件 {args.file}")
            print(f"  字数 {s['chars']} | 句数 {s['sentences']} | 节奏方差 {s['rhythm_std']} | 被字句 {s['passive_zh']}")
            print(f"  痕迹词 {s['tells_total']} 处: {s['tells'] or '无'}")
            print(f"  数字/日期: {s['numeric_tokens'] or '无'}")
            return 0
        if args.cmd == "diff":
            before = Path(args.before).read_text(encoding="utf-8")
            after = Path(args.after).read_text(encoding="utf-8")
            return print_report(diff_texts(before, after), args.json)
    except FileNotFoundError as e:
        print(f"错误: 文件不存在 {e.filename}", file=sys.stderr)
        return 2
    except UnicodeDecodeError as e:
        print(f"错误: 文件不是 UTF-8 文本 {e.filename}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    sys.exit(main())
