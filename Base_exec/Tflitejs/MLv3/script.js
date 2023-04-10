const input = document.getElementById('imageInput');

input.addEventListener('change', (event) => {
  const imginp = event.target.files[0];
  const reader = new FileReader();
  reader.readAsDataURL(imginp);
  localStorage.setItem('imageInput', reader.result);
});



/*
const tfliteModel = await tflite.loadTFLiteModel('Tensorflowjs\model.tflite');

const img = tf.browser.fromPixels(document.getElementById('image'));


const input = tf.sub(tf.div(tf.expandDims(img), 127.5), 1);

let outputTensor = tfliteModel.predict(input); //as tf.Tensor;


const scores = output[0].dataSync();
const classes = output[1].dataSync();
const boxes = output[2].dataSync();

const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
ctx.drawImage(document.getElementById('image'), 0, 0);
ctx.strokeStyle = 'red';
ctx.lineWidth = 4;


for (let i = 0; i < scores.length; i++) {
  if (scores[i] > 0.5) {
    const [ymin, xmin, ymax, xmax] = boxes.subarray(i * 4, i * 4 + 4);
    const [width, height] = [canvas.width, canvas.height];
    ctx.strokeRect(xmin * width, ymin * height, (xmax - xmin) * width, (ymax - ymin) * height);
  }
}
console.log(outputTensor.dataSync());
*/