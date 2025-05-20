# -*- coding: utf-8 -*-
"""
Created on 

@author: sistemas
"""

import sys
import os
import argparse

def process_lines(lines, consider_spaces, comment_empty, remove_empty):
    seen = set()
    output_lines = []

    for line in lines:
        # Guardar línea original para salida si es única
        original_line = line
        # Procesar línea para comparación
        if consider_spaces:
            cmp_line = line.rstrip('\n')  # conserva espacios
        else:
            cmp_line = line.strip()  # elimina espacios y saltos para comparación
        
        if cmp_line == '':
            # Línea vacía
            if remove_empty:
                continue  # ignorar línea vacía
            elif comment_empty:
                output_lines.append('#\n')
            else:
                output_lines.append('\n')
            continue

        if cmp_line not in seen:
            seen.add(cmp_line)
            output_lines.append(original_line)

    return output_lines

def save_output(output_dir, input_path, lines):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    base_name = os.path.basename(input_path) if input_path else 'stdin'
    output_path = os.path.join(output_dir, f"filtered_{base_name}")
    with open(output_path, 'w') as f:
        f.writelines(lines)
    print(f"[INFO] Archivo guardado en: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Remover líneas repetidas de un archivo o stdin.")
    parser.add_argument('input_file', nargs='?', help="Archivo de entrada (por defecto stdin)")
    parser.add_argument('-s', '--spaces', action='store_true',
                        help="Considerar espacios en comparación de líneas")
    parser.add_argument('-p', '--comment-empty', action='store_true',
                        help="Comentar líneas vacías con '#'")
    parser.add_argument('-e', '--remove-empty', action='store_true',
                        help="Eliminar líneas vacías")
    parser.add_argument('-o', '--output-dir', default=os.path.expanduser('~/.local/bin'),
                        help="Directorio donde guardar archivo filtrado (default: ~/.local/bin)")

    args = parser.parse_args()

    if args.input_file:
        try:
            with open(args.input_file, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"[ERROR] Archivo no encontrado: {args.input_file}", file=sys.stderr)
            sys.exit(1)
    else:
        lines = sys.stdin.readlines()

    filtered_lines = process_lines(lines, args.spaces, args.comment_empty, args.remove_empty)

    # Imprimir salida a stdout
    print(''.join(filtered_lines), end='')

    # Guardar archivo si hay input_file
    if args.input_file:
        save_output(args.output_dir, args.input_file, filtered_lines)
    else:
        # Para stdin, guardar en archivo genérico
        save_output(args.output_dir, None, filtered_lines)

if __name__ == '__main__':
    main()

