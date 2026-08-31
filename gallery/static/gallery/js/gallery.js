// update file name on file upload when one is selected
// resource https://www.w3tutorials.net/blog/styling-an-input-type-file-button/
const fileUpload =  document.getElementById('id_image');
const fileName = document.getElementById('file-name');

fileUpload.addEventListener('change', (e) => {
  const selectedFile = e.target.files[0];
  if (selectedFile) {
    fileName.textContent = selectedFile.name;
  } else {
    fileName.textContent = 'Upload image (required)';
  }
});

// dynamically add input fields for new_theme when needed
// pattern from:
// https://www.codewithfaraz.com/content/8/how-to-create-form-fields-dynamically-with-javascript
// used with properties instead of attributes:
// https://gomakethings.com/articles/the-difference-between-attributes-and-properties-in-vanilla-js/
document.getElementById("add-new-theme-btn").addEventListener("click", function(){
  const container = document.getElementById("new-theme-fields")
  const newInput = document.createElement('input')
  newInput.type = 'text';
  newInput.name = 'new_theme';
  newInput.className = 'form-control mt-2';
  newInput.placeholder = 'Add another theme';
  container.appendChild(newInput);

})