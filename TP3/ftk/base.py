# -*- coding: utf-8 -*-
"""
Created on 

@author: sistemas
"""

#!/usr/bin/env python3
import re
import sys
import argparse
from typing import List, Dict, Tuple, Optional

def tokenize(text: str) -> List[str]:
    # Tokeniza palabras y símbolos, con soporte para guiones
    pattern = r'\w+(?:-\w+)*|[^\w\s]+'
    return re.findall(pattern, text)

def count_tokens(tokens: List[str]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for token in tokens:
        counts[token] = counts.get(token, 0) + 1
    return counts

def sum_counts(c1: Dict[str, int], c2: Dict[str, int]) -> Dict[str, int]:
    result = c1.copy()
    for k, v in c2.items():
        result[k] = result.get(k, 0) + v
    return result

def subtract_counts(c1: Dict[str, int], c2: Dict[str, int]) -> Dict[str, int]:
    result = c1.copy()
    for k, v in c2.items():
        result[k] = result.get(k, 0) - v
        if result[k] <= 0:
            del result[k]
    return result

def frequencies(counts: Dict[str, int], total: Optional[int] = None) -> Dict[str, Tuple[int, float]]:
    if total is None:
        total = sum(counts.values())
    if total == 0:
        return {k: (v, 0.0) for k, v in counts.items()}
    return {k: (v, v / total) for k, v in counts.items()}

def ratio(freq1: Dict[str, Tuple[int, float]],
          freq2: Dict[str, Tuple[int, float]],
          smoothing: float = 1e-3) -> Dict[str, float]:
    all_tokens = set(freq1.keys()).union(freq2.keys())
    ratios: Dict[str, float] = {}
    for token in all_tokens:
        f1 = freq1.get(token, (0, smoothing))[1]
        f2 = freq2.get(token, (0, smoothing))[1]
        ratios[token] = f1 / f2 if f2 > 0 else float('inf')
    return ratios

def pretty_print(freq: Dict[str, Tuple[int, float]], 
                 sort_by: str = "count",
                 limit: Optional[int] = None,
                 show_relative: bool = True,
                 show_absolute: bool = True) -> None:
    # Ordenar por frecuencia absoluta o relativa
    if sort_by == "count":
        items = sorted(freq.items(), key=lambda x: x[1][0], reverse=True)
    else:
        items = sorted(freq.items(), key=lambda x: x[1][1], reverse=True)
    
    if limit is not None:
        items = items[:limit]
    
    print(f"{'Token':<20} {'Count':>10} {'RelFreq':>12}")
    print("-" * 44)
    for token, (count, relfreq) in items:
        abs_str = f"{count:>10}" if show_absolute else ""
        rel_str = f"{relfreq:>12.6f}" if show_relative else ""
        print(f"{token:<20} {abs_str} {rel_str}")

def load_texts(paths: List[str]) -> str:
    texts = []
    if not paths:
        texts.append(sys.stdin.read())
    else:
        for p in paths:
            with open(p, encoding='utf-8') as f:
                texts.append(f.read())
    return "\n".join(texts)

def main():
    parser = argparse.ArgumentParser(description="Token frequency analyzer")
    parser.add_argument('files', nargs='*', help='Input text files (default: stdin)')
    parser.add_argument('-a', '--absolute', action='store_true', help='Show absolute frequencies')
    parser.add_argument('-r', '--relative', action='store_true', help='Show relative frequencies')
    parser.add_argument('-s', '--sort', choices=['count', 'relative'], default='count', help='Sort by count or relative frequency')
    parser.add_argument('-l', '--limit', type=int, help='Limit output to top N tokens')
    parser.add_argument('--add', nargs=2, metavar=('FILE1', 'FILE2'), help='Add counts from two files and show combined frequencies')
    parser.add_argument('--subtract', nargs=2, metavar=('FILE1', 'FILE2'), help='Subtract counts of second file from first')
    parser.add_argument('--ratio', nargs=2, metavar=('FILE1', 'FILE2'), help='Show frequency ratio between two files')
    args = parser.parse_args()

    # Si alguna operación compuesta
    if args.add:
        text1 = load_texts([args.add[0]])
        text2 = load_texts([args.add[1]])
        c1 = count_tokens(tokenize(text1))
        c2 = count_tokens(tokenize(text2))
        c_sum = sum_counts(c1, c2)
        freq = frequencies(c_sum)
        pretty_print(freq, sort_by=args.sort, limit=args.limit, show_absolute=args.absolute or not args.relative, show_relative=args.relative)
        return

    if args.subtract:
        text1 = load_texts([args.subtract[0]])
        text2 = load_texts([args.subtract[1]])
        c1 = count_tokens(tokenize(text1))
        c2 = count_tokens(tokenize(text2))
        c_sub = subtract_counts(c1, c2)
        freq = frequencies(c_sub)
        pretty_print(freq, sort_by=args.sort, limit=args.limit, show_absolute=args.absolute or not args.relative, show_relative=args.relative)
        return

    if args.ratio:
        text1 = load_texts([args.ratio[0]])
        text2 = load_texts([args.ratio[1]])
        c1 = count_tokens(tokenize(text1))
        c2 = count_tokens(tokenize(text2))
        f1 = frequencies(c1)
        f2 = frequencies(c2)
        r = ratio(f1, f2)
        print(f"{'Token':<20} {'Ratio':>10}")
        print("-" * 31)
        for token, val in sorted(r.items(), key=lambda x: x[1], reverse=True):
            print(f"{token:<20} {val:>10.6f}")
        return

    # Caso normal: contar tokens de archivos o stdin
    text = load_texts(args.files)
    tokens = tokenize(text)
    counts = count_tokens(tokens)
    freq = frequencies(counts)
    pretty_print(freq, sort_by=args.sort, limit=args.limit, show_absolute=args.absolute or not args.relative, show_relative=args.relative)

if __name__ == "__main__":
    main()
