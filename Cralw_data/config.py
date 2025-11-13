import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# ==============================
#  Danh sách tất cả RSS chính của Dân Trí
# ==============================
rss_sources = {
    "thoi-su": "https://dantri.com.vn/rss/thoi-su.rss",
    "the-gioi": "https://dantri.com.vn/rss/the-gioi.rss",
    "kinh-doanh": "https://dantri.com.vn/rss/kinh-doanh.rss",
    "giao-duc-khuyen-hoc": "https://dantri.com.vn/rss/giao-duc-khuyen-hoc.rss",
    "the-thao": "https://dantri.com.vn/rss/the-thao.rss",
    "giai-tri": "https://dantri.com.vn/rss/giai-tri.rss",
    "phap-luat": "https://dantri.com.vn/rss/phap-luat.rss",
    "suc-khoe": "https://dantri.com.vn/rss/suc-khoe.rss",
    "o-to-xe-may": "https://dantri.com.vn/rss/o-to-xe-may.rss",
    "van-hoa": "https://dantri.com.vn/rss/van-hoa.rss",
    "nhip-song-tre": "https://dantri.com.vn/rss/nhip-song-tre.rss",
    "du-lich": "https://dantri.com.vn/rss/du-lich.rss",
    "tam-long-nhan-ai": "https://dantri.com.vn/rss/tam-long-nhan-ai.rss",
    "blog": "https://dantri.com.vn/rss/blog.rss",
    "xa-hoi": "https://dantri.com.vn/rss/xa-hoi.rss"
}

# ==============================
#  Hàm lấy nội dung bài viết
# ==============================
def get_article_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.encoding = res.apparent_encoding
        soup = BeautifulSoup(res.text, "html.parser")

        # Nội dung chính nằm trong div#divNewsContent
        paragraphs = soup.select("div#divNewsContent p")
        content = "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
        return content.strip()
    except Exception as e:
        print(f" Lỗi khi lấy nội dung {url}: {e}")
        return None

# ==============================
#  Crawl toàn bộ RSS
# ==============================
all_articles = []

for category, rss_url in rss_sources.items():
    print(f"\n Đang lấy chuyên mục: {category} ...")
    feed = feedparser.parse(rss_url)
    print(f"    Số bài trong RSS: {len(feed.entries)}")

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        summary = entry.summary if "summary" in entry else ""
        published = entry.published if "published" in entry else ""

        content = get_article_content(link)

        all_articles.append({
            "category": category,
            "title": title,
            "link": link,
            "summary": summary,
            "published": published,
            "content": content
        })

        time.sleep(random.uniform(1, 2))  # nghỉ 1–2 giây tránh bị chặn

print(f"\n Hoàn tất! Tổng số bài lấy được: {len(all_articles)}")

# ==============================
#  Lưu ra file CSV
# ==============================
df = pd.DataFrame(all_articles)
df.to_csv("dantri_all_rss.csv", index=False, encoding="utf-8-sig")
print(" Đã lưu dữ liệu vào file: dantri_all_rss.csv")
