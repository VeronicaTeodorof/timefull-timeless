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