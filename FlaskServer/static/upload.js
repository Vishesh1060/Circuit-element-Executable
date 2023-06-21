document.addEventListener('DOMContentLoaded',()=>{
    let upbtnclick=document.getElementById('upbtnclick');

    upbtnclick.addEventListener('click',()=>{
        let image = document.querySelector('uploadimage');
        let formdata = new FormData(image,image.src);
        formdata.append();
        let xhr = new XMLHttpRequest();
        xhr.open['POST','/upload']
        xhr.send(formdata);
     })

});