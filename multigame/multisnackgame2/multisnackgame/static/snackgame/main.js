function send(methed,url,message,func,Content_type='application/x-www-form-urlencoded'){
    if(XMLHttpRequest){
        var xhr = new XMLHttpRequest();
    }else{
        var xhr = new ActiveXObject('Microsoft.XMLHTTP');
    }
    xhr.onreadystatechange=function(){
        if(this.status==200 && this.readyState==4){
            func(xhr)
        }
    }
    if(methed=='post'){
        xhr.open(methed,url,true)
        xhr.setRequestHeader('Content-Type',Content_type)
        xhr.send(message)
    }else if(methed=='get'){
        url=url+'?'+message
        xhr.open(methed,url,true)
        xhr.send()
    }else{
        return
    }
}
window.onresize = function(){
    offsetheight=document.body.offsetHeight
    offsetwidth=document.body.offsetWidth
}
window.onload = function(){
    let newdiv = document.getElementById('newdiv')
    let start = document.getElementById('start')
    let text = document.getElementById('name')
    start.onclick=function(){
        if(text.value){
            if(text.value.length>10){
                alert('Please input 1 to 10 letters')
            }else{
                send('post','addsnack/','name='+text.value,function(xhr){
                    console.log(xhr.response)
                })
                send('post','getinfor/','',function(xhr){
                    console.log(xhr.response)
                })
            }
        }else{
            alert('Please input your name!')
        }
    }
}
var mycanvas = document.getElementById('myCanvas')
var ctx = mycanvas.getContext('2d')
var offsetheight = document.body.offsetHeight
var offsetwidth = document.body.offsetWidth
mycanvas.width = offsetwidth
mycanvas.height = offsetheight
mycanvas.style.visibility='hidden'// visible