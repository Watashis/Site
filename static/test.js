
 /* Данная функция создаёт кроссбраузерный объект XMLHTTP */
 function getXmlHttp() {
    var xmlhttp;
    try {
      xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
    } catch (e) {
    try {
      xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    } catch (E) {
      xmlhttp = false;
    }
    }
    if (!xmlhttp && typeof XMLHttpRequest!='undefined') {
      xmlhttp = new XMLHttpRequest();
    }
    return xmlhttp;
  }
  function create() {
    var name = document.getElementById("Name").value; // Считываем значение a
    var ava = document.getElementById("Avatar").value; // Считываем значение b
    var text = document.getElementById("Text").value; // Считываем значение a
    var date = document.getElementById("Date").value; // Считываем значение b
    var xmlhttp = getXmlHttp(); // Создаём объект XMLHTTP
    xmlhttp.open('POST', '/quotes', true); // Открываем асинхронное соединение
    xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded'); // Отправляем кодировку
    xmlhttp.send("base64=true&name=" + encodeURIComponent(name) + "&ava=" + encodeURIComponent(ava) +"&text=" + encodeURIComponent(text) + "&date=" + encodeURIComponent(date)); // Отправляем POST-запрос
    xmlhttp.onreadystatechange = function() { // Ждём ответа от сервера
      if (xmlhttp.readyState == 4) { // Ответ пришёл
        if(xmlhttp.status == 200) { // Сервер вернул код 200 (что хорошо)
            console.log('все ок')
            var result = ('data:image/png;base64,' + xmlhttp.responseText);
            document.getElementById('quoteimg').src =result;
            document.getElementById('downloadimg').href =result;
        }
      }
    };
  }
