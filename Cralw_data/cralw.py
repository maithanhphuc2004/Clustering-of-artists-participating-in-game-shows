# -*- coding: utf-8 -*-
import json, re, time
from pathlib import Path
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd  # 🔹 thêm pandas để đọc Excel

# ==== CẤU HÌNH ====
INPUT_XLSX = r"D:\MangXaHoi\gameshow_vietnam\linkgameshow.xlsx"  
SHEET_NAME = 0           
LINK_COL   = "link"      
OUTPUT_DIR = Path("output_rows")
TIMEOUT    = 20
HEADLESS   = True
# ===================

# === Đọc danh sách URL từ Excel ===
try:
    df = pd.read_excel(INPUT_XLSX, sheet_name=SHEET_NAME)
except Exception as e:
    raise RuntimeError(f"Lỗi đọc file Excel: {e}")

if LINK_COL not in df.columns:
    raise ValueError(f"Không tìm thấy cột '{LINK_COL}' trong file Excel!")

URLS = [str(u).strip() for u in df[LINK_COL].dropna() if str(u).strip()]
print(f" Đã đọc {len(URLS)} link từ file Excel: {INPUT_XLSX}")

# ===================================

def slugify(s, maxlen=60):
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE).replace(" ", "_")
    return (s or "table")[:maxlen]

def make_driver(headless=True):
    opts = webdriver.ChromeOptions()
    if headless: 
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1400,900")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-logging"])
    d = webdriver.Chrome(options=opts)
    d.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                      {"source":"Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"})
    return d

def extract_rows_from_wikitable(tbl):
    rows = tbl.find_elements(By.CSS_SELECTOR, "tr")

    # 1) tìm header
    header = []
    header_row_idx = None
    for i, r in enumerate(rows):
        ths = r.find_elements(By.CSS_SELECTOR, "th")
        if ths:
            header = [c.text.strip() or f"col_{j+1}" for j, c in enumerate(ths)]
            header_row_idx = i
            break

    # fallback nếu không có th
    if not header:
        longest = max((len(r.find_elements(By.CSS_SELECTOR, "td")), idx)
                      for idx, r in enumerate(rows))[1]
        header = [f"col_{j+1}" for j in range(len(rows[longest].find_elements(By.CSS_SELECTOR, "td")))]
        header_row_idx = longest

    # 2) duyệt các hàng dữ liệu sau header
    records = []
    for i, r in enumerate(rows):
        if i <= header_row_idx:
            continue
        cells = r.find_elements(By.CSS_SELECTOR, "td")
        if not cells:
            continue
        vals = [c.text.strip() for c in cells]
        if len(vals) < len(header):
            vals += [""] * (len(header) - len(vals))
        elif len(vals) > len(header):
            header += [f"col_{len(header)+j+1}" for j in range(len(vals)-len(header))]
        rec = {header[j]: vals[j] for j in range(len(header))}
        if any(v for v in rec.values()):
            records.append(rec)
    return records, header

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    d = make_driver(HEADLESS)
    try:
        for url in URLS:
            d.get(url)
            WebDriverWait(d, TIMEOUT).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table.wikitable"))
            )
            time.sleep(0.3)
            title = d.title.replace(" – Wikipedia tiếng Việt", "").strip()
            base = slugify(title) or slugify(urlparse(url).path.split("/")[-1])

            tables = d.find_elements(By.CSS_SELECTOR, "table.wikitable")
            for k, tbl in enumerate(tables, start=1):
                rows, header = extract_rows_from_wikitable(tbl)
                out_path = OUTPUT_DIR / f"{base}_table_{k:02d}.jsonl"
                with out_path.open("w", encoding="utf-8") as f:
                    for rec in rows:
                        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                print(f"[OK] {url} → {out_path}  ({len(rows)} rows)")

    finally:
        d.quit()

if __name__ == "__main__":
    main() 
