document.addEventListener("DOMContentLoaded", function () {
  const attrInputs = document.querySelectorAll(".attr-input");
  const totalAttributePointsElement = document.getElementById("total-attribute-points");
  const maxAttributeTotalValue = 15;

  function getAttrPointTotal() {
    let total = 0;
    attrInputs.forEach(input => {
      total += parseInt(input.value);
    });
    return total;
  }

  function updateTotalAttributePoints() {
    let total = 0;
    attrInputs.forEach(input => {
      total += parseInt(input.value);
    });
    totalAttributePointsElement.textContent = total;
  }

  attrInputs.forEach(input => {
    input.addEventListener("input", function (event) {
      let pointTotal = getAttrPointTotal();
      if (pointTotal > maxAttributeTotalValue)
        input.value = input.value - (pointTotal - maxAttributeTotalValue);

      document.getElementById(input.id + "-value").textContent = input.value;

      updateTotalAttributePoints(pointTotal);
    });
  });

  // Initial update of total attribute points and max values
  updateTotalAttributePoints(getAttrPointTotal());
});