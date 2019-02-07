function getXmlHttp() {
    let xmlhttp
    
    try {
      xmlhttp = new ActiveXObject("Msxml2.XMLHTTP")
    } catch (e) {
        try {
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP")
        } catch (E) {
            xmlhttp = false
        }
    }
    
    if (!xmlhttp && XMLHttpRequest === void 0) {
      xmlhttp = new XMLHttpRequest()
    }
    
    return xmlhttp
}

function create() {
    const name = document.getElementById("Name").value
    const ava = document.getElementById("Avatar").value
    const text = document.getElementById("Text").value
    const date = document.getElementById("Date").value

    let xmlhttp = getXmlHttp()

    xmlhttp.open('POST', '/quotes', true)
    xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
    xmlhttp.send("base64=true&name=" + encodeURIComponent(name) + "&ava=" + encodeURIComponent(ava) +"&text=" + encodeURIComponent(text) + "&date=" + encodeURIComponent(date))
    xmlhttp.onreadystatechange = function() {
      if (xmlhttp.readyState == 4) {
        if (xmlhttp.status == 200) {
            console.log('все ок')
            var result = ('data:image/png;base64,' + xmlhttp.responseText);
            document.getElementById('quoteimg').src =result;
            document.getElementById('downloadimg').href =result;
       }
     }
   }
}
