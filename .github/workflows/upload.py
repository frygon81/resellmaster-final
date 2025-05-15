import requests
import json
from datetime import datetime
from github import Github

# 설정값
GITHUB_USERNAME = "frygon81"
REPO_NAME = "resellmaster-final"
BRANCH = "main"
ACCESS_TOKEN = "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"
DATA_FILE = "data.json"

# eBay 가격 크롤링
def fetch_ebay_price(sku):
    url = f"https://www.ebay.com/sch/i.html?_nkw={sku}&LH_Sold=1&LH_Complete=1"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(res.text, "html.parser")
    prices = [
        float(p.text.replace("$", "").replace(",", ""))
        for p in soup.select(".s-item__price") if "$" in p.text
    ]
    return round(sum(prices) / len(prices)) if prices else 0

# SKU 리스트 (매일 자동 수집 대상)
sku_list = [
    "MT580ED2", "IH1321", "U740WN2", "415445-101", "HQ3025-001",
    "FZ6768 100", "JOG-100S", "FJ4151-004", "P6000", "IF3654"
]

# 결과 생성
data = {}
for sku in sku_list:
    price = fetch_ebay_price(sku)
    data[sku] = {
        "ebay_price": price,
        "monthly_sales": 15
    }

# GitHub에 자동 업로드
def upload_to_github(data):
    g = Github(ACCESS_TOKEN)
    repo = g.get_user().get_repo(REPO_NAME)
    contents = repo.get_contents(DATA_FILE, ref=BRANCH)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    message = f"Auto Update ({now})"
    repo.update_file(contents.path, message, json.dumps(data, indent=2), contents.sha, branch=BRANCH)

upload_to_github(data)
print("✅ data.json 자동 크롤링 & GitHub 업로드 완료")
