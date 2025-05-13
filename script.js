async function analyze() {
  const sku = document.getElementById('sku').value.trim();
  const cost = parseInt(document.getElementById('cost').value, 10);
  const resultBox = document.getElementById('result');

  if (!sku || isNaN(cost)) {
    resultBox.innerText = "SKU와 가격을 정확히 입력해주세요.";
    return;
  }

  try {
    const response = await fetch('data.json');
    const data = await response.json();

    const resalePrice = data[sku];
    if (!resalePrice) {
      resultBox.innerText = "해당 SKU의 데이터를 찾을 수 없습니다.";
      return;
    }

    const fee = resalePrice * 0.12;
    const shipping = 18000;
    const netProfit = resalePrice - fee - shipping - cost;

    resultBox.innerText = 
      `eBay 시세: ₩${resalePrice.toLocaleString()}\n` +
      `수수료: ₩${fee.toLocaleString()}\n` +
      `배송비: ₩${shipping.toLocaleString()}\n` +
      `국내가: ₩${cost.toLocaleString()}\n` +
      `예상 순이익: ₩${netProfit.toLocaleString()}`;
  } catch (error) {
    resultBox.innerText = "데이터를 불러올 수 없습니다. 인터넷 연결을 확인해주세요.";
  }
}