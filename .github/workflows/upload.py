import json
import requests
from bs4 import BeautifulSoup

def fetch_price(sku):
    try:
        url = f"https://www.ebay.com/sch/i.html?_nkw={sku}&LH_Sold=1&LH_Complete=1"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")
        prices = [
            float(price.text.replace("$", "").replace(",", ""))
            for price in soup.select(".s-item__price")
            if "$" in price.text
        ]
        avg_price = sum(prices) / len(prices) if prices else 0
        return round(avg_price)
    except Exception as e:
        print(f"Error fetching {sku}: {e}")
        return 0

sku_list = [
    "MT580ED2", "IH1321", "U740WN2", "415445-101", "HQ3025-001", "FZ6768 100",
    "JOG-100S", "FJ4151-004", "P6000", "IF3654"
]

data = {}

for sku in sku_list:
    price = fetch_price(sku)
    data[sku] = {
        "ebay_price": price,
        "monthly_sales": 15  # 기본값
    }

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ data.json 자동 생성 완료")
