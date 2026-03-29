#!/usr/bin/env python3
"""
닉네임 정규화 스크립트
======================
CSV에서 '아저씨'가 포함된 모든 summoner_name을 '감귤 아저씨'로 통일합니다.

Usage:
    python normalize_names.py <input_csv> [output_csv]

    output_csv 를 생략하면 원본 파일을 덮어씁니다.
"""

import csv
import sys
import shutil
from pathlib import Path

# TARGET_NAME  = "감귤 아저씨"   # 통일할 최종 닉네임
# MATCH_KEYWORD = "아저씨"       # 이 단어가 포함된 summoner_name 을 모두 교체
TARGET_NAME  = "행복한욕조견"   # 통일할 최종 닉네임
MATCH_KEYWORD = "행복한"

def normalize(input_path: Path, output_path: Path) -> int:
    """CSV를 읽어 닉네임을 정규화하고 저장합니다. 교체된 행 수를 반환합니다."""

    with open(input_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    changed = 0
    for row in rows:
        name = row.get("summoner_name", "")
        if MATCH_KEYWORD in name and name != TARGET_NAME:
            print(f"  변경: '{name}'  →  '{TARGET_NAME}'")
            row["summoner_name"] = TARGET_NAME
            changed += 1

    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return changed


def main():
    if len(sys.argv) < 2:
        print("Usage: python normalize_names.py <input_csv> [output_csv]")
        sys.exit(1)

    input_path  = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) >= 3 else input_path

    if not input_path.exists():
        print(f"오류: 파일을 찾을 수 없습니다 → {input_path}")
        sys.exit(1)

    # 원본 덮어쓰기 전 백업
    if output_path == input_path:
        backup = input_path.with_suffix(".bak.csv")
        shutil.copy2(input_path, backup)
        print(f"백업 생성: {backup}")

    print(f"\n'{MATCH_KEYWORD}' 포함 닉네임을 '{TARGET_NAME}'으로 통일합니다...\n")
    changed = normalize(input_path, output_path)

    print(f"\n완료: {changed}개 행 변경 → {output_path}")


if __name__ == "__main__":
    main()
