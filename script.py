#!/usr/bin/env python3
"""
Evaluate transcription models against a gold standard.

Expected directory layout (relative to this script, or pass --root):

    ./GOLD Standard/{NAME}.txt
    ./{MODEL_NAME}/{NAME}.txt
    ./{MODEL_NAME_2}/{NAME}.txt
    ...

For every model folder found next to "GOLD Standard", the script compares
each {NAME}.txt file against the matching gold file and computes:
    - CER (Character Error Rate)
    - WER (Word Error Rate)

Per-file and per-model average scores are printed.

Usage:
    python evaluate_transcriptions.py
    python evaluate_transcriptions.py --root /path/to/folder
    python evaluate_transcriptions.py --gold-dir "GOLD Standard"
"""

import argparse
import os
import sys

try:
    import jiwer
except ImportError:
    sys.exit(
        "Missing dependency 'jiwer'. Install it with:\n"
        "    pip install jiwer --break-system-packages"
    )


# Normalization applied before computing CER/WER.
# Adjust this transform to control how strict the comparison is.
TRANSFORM = jiwer.Compose([
    jiwer.ToLowerCase(),
    jiwer.RemoveMultipleSpaces(),
    jiwer.Strip(),
    jiwer.ReduceToListOfListOfWords(),
])

CER_TRANSFORM = jiwer.Compose([
    jiwer.ToLowerCase(),
    jiwer.RemoveMultipleSpaces(),
    jiwer.Strip(),
    jiwer.ReduceToListOfListOfChars(),
])


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def find_model_dirs(root, gold_dir_name):
    """Return all subdirectories of root except the gold standard directory."""
    model_dirs = []
    for entry in sorted(os.listdir(root)):
        full_path = os.path.join(root, entry)
        if os.path.isdir(full_path) and entry != gold_dir_name:
            model_dirs.append(entry)
    return model_dirs


def find_gold_names(gold_path):
    """Return sorted list of NAME values (without .txt) found in gold dir."""
    names = []
    for entry in sorted(os.listdir(gold_path)):
        if entry.lower().endswith(".txt"):
            names.append(entry[:-4])
    return names


def evaluate(root=".", gold_dir_name="GOLD Standard"):
    gold_path = os.path.join(root, gold_dir_name)
    if not os.path.isdir(gold_path):
        sys.exit(f"Gold standard directory not found: {gold_path}")

    names = find_gold_names(gold_path)
    if not names:
        sys.exit(f"No .txt files found in {gold_path}")

    model_dirs = find_model_dirs(root, gold_dir_name)
    if not model_dirs:
        sys.exit(f"No model directories found alongside {gold_dir_name}")

    results = {}  # model_name -> list of (name, cer, wer)

    for model_name in model_dirs:
        model_path = os.path.join(root, model_name)
        per_file = []

        for name in names:
            gold_file = os.path.join(gold_path, f"{name}.txt")
            test_file = os.path.join(model_path, f"{name}.txt")

            if not os.path.isfile(test_file):
                print(f"[WARNING] Missing file: {test_file} -- skipping")
                continue

            reference = read_text(gold_file)
            hypothesis = read_text(test_file)

            cer = jiwer.cer(reference, hypothesis)
            wer = jiwer.wer(
                reference,
                hypothesis,
                reference_transform=TRANSFORM,
                hypothesis_transform=TRANSFORM,
            )

            per_file.append((name, cer, wer))

        results[model_name] = per_file

    return results


def print_results(results):
    for model_name, per_file in results.items():
        print(f"\n=== Model: {model_name} ===")
        if not per_file:
            print("  No matching files evaluated.")
            continue

        for name, cer, wer in per_file:
            print(f"  {name:30s}  CER: {cer:6.2%}   WER: {wer:6.2%}")

        avg_cer = sum(c for _, c, _ in per_file) / len(per_file)
        avg_wer = sum(w for _, _, w in per_file) / len(per_file)
        print(f"  {'-'*30}  {'-'*6}        {'-'*6}")
        print(f"  {'AVERAGE':30s}  CER: {avg_cer:6.2%}   WER: {avg_wer:6.2%}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", default=".",
        help="Root directory containing the model folders and the gold standard folder (default: current directory)"
    )
    parser.add_argument(
        "--gold-dir", default="GOLD Standard",
        help='Name of the gold standard directory (default: "GOLD Standard")'
    )
    args = parser.parse_args()

    results = evaluate(root=args.root, gold_dir_name=args.gold_dir)
    print_results(results)


if __name__ == "__main__":
    main()