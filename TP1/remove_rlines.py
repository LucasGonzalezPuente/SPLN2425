# -*- coding: utf-8 -*-
"""
Created on 

@author: sistemas
"""

import sys
from itertools import groupby

def main():
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file, 'r') as f:
            lines = f.readlines()
        # agrupar líneas consecutivas iguales
        filtered_lines = []
        for line, group in groupby(lines):
            if line == '\n':
                # Mantener todas las líneas vacías tal cual
                filtered_lines.extend(list(group))
            else:
                # Añadir solo una vez por grupo consecutivo
                filtered_lines.append(line)
        output_file = input_file.replace('.txt', '_filtered.txt')
        with open(output_file, 'w') as f:
            f.writelines(filtered_lines)
        print(''.join(filtered_lines), end='')
    else:
        lines = sys.stdin.readlines()
        filtered_lines = []
        for line, group in groupby(lines):
            if line == '\n':
                filtered_lines.extend(list(group))
            else:
                filtered_lines.append(line)
        print(''.join(filtered_lines), end='')

if __name__ == "__main__":
    main()
