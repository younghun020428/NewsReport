from scripts.config import get_now_kst
import os

print("--- Timezone Verification ---")
now_kst = get_now_kst()
print(f"Current KST Time: {now_kst}")
print(f"Today String (KST): {now_kst.strftime('%Y%m%d')}")

print("\n--- Model Verification (Checking scripts) ---")
scripts = ["02_filter_summarize.py", "05_generate_macro_report.py"]
for script in scripts:
    path = os.path.join("scripts", script)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        if "gemini-2.0-flash" in content:
            print(f"{script}: Model updated to gemini-2.0-flash")
        elif "gemini-2.5-flash" in content:
            print(f"{script}: Model is STILL gemini-2.5-flash (FAIL)")
        else:
            print(f"{script}: gemini-2.0-flash not found (Check manually)")
