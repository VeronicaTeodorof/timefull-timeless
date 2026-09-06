// Toggle visibility of the country choice section based on the
// selected shipping method. The country radios (UK/Romania) are
// only relevant when "Delivery" is chosen, so they stay hidden
// while "Studio Pickup" is selected.

const shippingRadios = document.querySelectorAll('input[name="shipping_method"]');
const countryChoice = document.getElementById('country-choice');

for (let i = 0; i < shippingRadios.length; i++) {
  const radio = shippingRadios[i];

  radio.addEventListener('change', function () {
    if (this.value === 'delivery') {
      countryChoice.style.display = 'block';
    } else {
      countryChoice.style.display = 'none';
    }
  });
}

// Recalculates and displays the cost breakdown (sculpture price, insurance, delivery, total) whenever the shipping method or
// country changes.
// resource for translating DTL into JS:
// - https://adamj.eu/tech/2022/10/06/how-to-safely-pass-data-to-javascript-in-a-django-template/

const costBreakdown = document.getElementById('cost-breakdown');
const sculpturePrice = parseFloat(costBreakdown.dataset.sculpturePrice);
const insuranceCost = parseFloat(costBreakdown.dataset.insuranceCost);
const ukCost = parseFloat(costBreakdown.dataset.ukCost);
const roCost = parseFloat(costBreakdown.dataset.roCost);

function updateTotal() {
  const checkedShipping = document.querySelector('input[name="shipping_method"]:checked');
  const shippingMethod = checkedShipping.value;

  let deliveryCost = 0;

  if (shippingMethod === 'delivery') {
    const checkedCountry = document.querySelector('input[name="country"]:checked');

    if (checkedCountry) {
      if (checkedCountry.value === 'UK') {
        deliveryCost = ukCost;
      } else {
        deliveryCost = roCost;
      }
    }
  }

  const total = sculpturePrice + insuranceCost + deliveryCost;

  document.getElementById('cost-delivery').textContent = '£' + deliveryCost.toFixed(2);
  document.getElementById('cost-total').textContent = '£' + total.toFixed(2);
}

const relevantInputs = document.querySelectorAll('input[name="shipping_method"], input[name="country"]');

for (let i = 0; i < relevantInputs.length; i++) {
  const input = relevantInputs[i];

  input.addEventListener('change', function () {
    updateTotal();
  });
}

updateTotal();