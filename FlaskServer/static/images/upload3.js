// Get the form element
var form = document.getElementById("upload-form");

// Add an event listener to handle the form submission
form.addEventListener("submit", function(event) {
  // Prevent the default form action
  event.preventDefault();

  // Create a FormData object to store the file data
  var formData = new FormData();

  // Get the file input element
  var fileInput = document.getElementById("image-file");

  // Get the selected file
  var file = fileInput.files[0];

  // Append the file to the FormData object
  formData.append("image-file", file);

  // Create a XMLHttpRequest object to send the request
  var xhr = new XMLHttpRequest();

  // Open the request with the POST method and the upload URL
  xhr.open("POST", "http://127.0.0.1:5000//upload");

  // Send the request with the FormData object
  xhr.send(formData);
});
