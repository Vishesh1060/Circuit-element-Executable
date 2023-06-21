// Get the image element from the upload window
const image = document.querySelector('.uploadimage');

// Get the upload button element
const uploadBtn = document.querySelector(".upbtn");

// Add an event listener to the upload button
uploadBtn.addEventListener('click', () => {
  // Convert the image to base64 string
  const canvas = document.createElement('canvas');
  canvas.width = image.width;
  canvas.height = image.height;
  const context = canvas.getContext('2d');
  context.drawImage(image, 0, 0);
  const imageData = canvas.toDataURL();

  // Create a payload object with the image data
  const payload = {
    image: imageData
  };
  const payloadJSON = JSON.stringify(payload);
  console.log(image)
  // Send a POST request to the flask backend with the payload
  fetch('http://127.0.0.1:5000/upload', {
    method: 'POST',
    //headers: {'Content-Type': 'application/json'},
    body: payloadJSON
  })
    .then(response => response.json())
    .then(data => {
      // Handle the response data
      console.log(data);
    })
    .catch(error => {
      // Handle the error
      console.error(error);
    });
});