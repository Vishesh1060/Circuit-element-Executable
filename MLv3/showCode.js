const imageInput = localStorage.getItem('imgInput');
const outimg = document.getElementById('imageOutput');
if(!outimg){
    console.log('not found')
}

if (imageInput) {
    outimg.setAttribute('src', imageInput);
} else {
    outimg.setAttribute('src', '');
}
