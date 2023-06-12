document.addEventListener('DOMContentLoaded',()=>{
    const uploadbuttonclick=document.querySelector('upbtnclick');
    
    uploadbuttonclick.addEventListener('click',()=>{
        let image = document.querySelector('uploadimage');
        let formdata = new FormData(image,image.src);
        formdata.append();
        let xhr = new XMLHttpRequest();
        xhr.open['POST','/upload']
        xhr.send(formdata);
     })

});