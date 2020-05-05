window.onload = function(){
    var box=document.getElementById('box');
    browser_wid=document.documentElement.clientWidth;
    box.style.cssText='width:'+browser_wid+'px;';
        //     $.ajax({
        //     type:'POST',
        //     url:"/hangye/",
        //     data:{
        //         'name' : '子'
        //     },
        //     success:function(data){
        //         console.log(data);
        //         if(data.status == 'ok'){
        //             alert("success");
        //         }
        //     }
        // })
}

