
document.getElementById("form").addEventListener("submit", async function(e) {
  e.preventDefault();
  const sku = document.getElementById("sku").value.trim();
  const domestic = parseInt(document.getElementById("domestic").value.trim());

  if (!sku || isNaN(domestic)) {
    document.getElementById("result").textContent = "SKU와 국내가를 정확히 입력해주세요.";
    return;
  }

  try {
    const response = await fetch("https://raw.githubusercontent.com/lukastock/data/main/data.json");
    const json = await response.json();
    const item = json[sku];

    if (!item) {
      document.getElementById("result").textContent = "해당 SKU는 아직 등록되지 않았습니다.";
      return;
    }

    const ebay = item.ebayPrice;
    const stockx = item.stockxPrice;
    const sales = item.monthlySales;

    const fee = Math.round(ebay * 0.12);
    const ship = 18000;
    const profit = ebay - fee - ship - domestic;

    let mark = "❌ 제외";
    if (profit >= 10000 && sales >= 15) mark = "✔ 추천";
    else if (profit >= 1000) mark = "⚠ 테스트";

    document.getElementById("result").innerHTML = `
      <b>eBay 평균가:</b> ₩${ebay.toLocaleString()}<br>
      <b>StockX 시세:</b> ₩${stockx.toLocaleString()}<br>
      <b>월 판매량:</b> ${sales}개<br>
      <b>수수료:</b> ₩${fee.toLocaleString()}<br>
      <b>배송비:</b> ₩${ship.toLocaleString()}<br>
      <b>국내가:</b> ₩${domestic.toLocaleString()}<br>
      <b>순이익:</b> ₩${profit.toLocaleString()}<br>
      <b>판단:</b> ${mark}
    `;
  } catch (err) {
    document.getElementById("result").textContent = "데이터를 불러올 수 없습니다.";
  }
});
