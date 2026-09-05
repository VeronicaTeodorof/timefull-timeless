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