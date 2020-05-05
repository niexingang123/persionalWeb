window.onload = function(){
    var box=document.getElementById('box');
    var browser_wid=document.documentElement.clientWidth;
    box.style.cssText='width:'+browser_wid+'px;';
    var main=document.getElementsByClassName('main');
    for (var i=0; i< main.length;i++) {
        main[i].style.cssText='width:'+(browser_wid-30)/2+'px;';
    }
    $.ajax({
        type:'GET',
        url:"/hangye_ajax/",
        data:{
            'name' : '银'
        },
        success:function(response){
            data=JSON.parse(response);
            for (i in data) {
                console.log(data[1]);
            }
        }
    })
}

