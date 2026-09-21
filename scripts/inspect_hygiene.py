import os
import hashlib
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

LOBES = [
    ROOT_DIR / "Guidebooks_and_Notes",
    ROOT_DIR / "BluprintArchitecture",
    ROOT_DIR / "Integra Self-Reflect and Think Forward",
    ROOT_DIR / "CODE"
]

def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def main():
    print(f"Scanning Root: {ROOT_DIR}")
    
    # 1. Check .m4a duplicate
    m4a_lecture = ROOT_DIR / "Audio_Lectures" / "The_neuro-evolutionary_architecture_of_Integra_OS.m4a"
    m4a_reflect = ROOT_DIR / "Integra Self-Reflect and Think Forward" / "The_neuro-evolutionary_architecture_of_Integra_OS.m4a"
    
    print("\n=== 1. AUDIO M4A CHECK ===")
    if m4a_reflect.exists():
        size_reflect = m4a_reflect.stat().st_size
        size_lecture = m4a_lecture.stat().st_size if m4a_lecture.exists() else None
        print(f"Duplicate exists: {m4a_reflect} ({size_reflect} bytes)")
        print(f"Canonical exists: {m4a_lecture} ({size_lecture} bytes)")
        if size_reflect == size_lecture:
            print("=> EXACT SIZE MATCH (Candidate for removal from Integra Self-Reflect and Think Forward)")
    else:
        print(f"No duplicate m4a in {m4a_reflect}")

    # 2. Check 0-byte dummy files
    print("\n=== 2. ZERO-BYTE FILES CHECK ===")
    zero_bytes = []
    for lobe in LOBES:
        if not lobe.exists():
            continue
        for p in lobe.rglob("*"):
            if p.is_file() and p.stat().st_size == 0:
                zero_bytes.append(p)
                print(f"0-byte file: {p.relative_to(ROOT_DIR)}")
    if not zero_bytes:
        print("No 0-byte files found.")

    # 3. Check identical .txt where .md exists
    print("\n=== 3. TXT / MD DUPLICATES CHECK ===")
    txt_md_candidates = []
    for lobe in LOBES:
        if not lobe.exists():
            continue
        txt_files = list(lobe.rglob("*.txt"))
        for txt in txt_files:
            # Check corresponding .md file in same directory
            md_exact = txt.with_suffix(".md")
            if md_exact.exists():
                txt_hash = hash_file(txt)
                md_hash = hash_file(md_exact)
                txt_size = txt.stat().st_size
                md_size = md_exact.stat().st_size
                is_identical = (txt_hash == md_hash)
                print(f"Pair: {txt.relative_to(ROOT_DIR)} ({txt_size}b) vs {md_exact.relative_to(ROOT_DIR)} ({md_size}b) | Identical Hash: {is_identical}")
                txt_md_candidates.append({
                    "txt": txt,
                    "md": md_exact,
                    "identical": is_identical,
                    "txt_size": txt_size,
                    "md_size": md_size
                })

if __name__ == "__main__":
    main()
