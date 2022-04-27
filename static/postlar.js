console.log("hello world!")
click = (e) => {
    return () => { console.log(e) }
}
function htmlToElement(html) {
    var template = document.createElement('template');
    html = html.trim(); // Never return a text node of whitespace as the result
    template.innerHTML = html;
    return template.content.firstChild;
}
createComment = (param) => {
    response = ""
    if (param.response !== undefined)
        response = `
        <div class="response" id="${param.response.id}">
            <div class="text"> ${param.response.content}</div>
            <div class="ppnicklogos">
              <div class="ppnick">
                <img src="${param.response.pp}" alt="profile photos" class="pp" width="32" height="32">
                <div class="name"> ${param.response.name}</div>
              </div>
            </div>
        </div>
    `
    return htmlToElement(`
    <div class="holder" id='${param.id}' onclick="yanitla(this)">
      ${response}
      <div class="text">
          ${param.content}
      </div>
      <div class="ppnicklogos">
        <div class="ppnick">
          <img src="${param.pp}" alt="profile photos" class="pp" width="32" height="32">
          <div class="name">${param.name}</div>
          </div>
          <img onclick="deleteComment('${param.id}')" src="static/icon/remove.png" alt="" class="logos" width="32" height="32">
          </div>
          </div>
          `)
}
yanitlayabilir = true
inputfield = document.getElementById("message")
if (inputfield !== null) {
    inputfield.onkeydown = function (e) {
        if (e.key === 'Enter') {
            yanitlayabilir = true
            var headId = document.getElementsByClassName("holder")[0].id
            var responseId = 0
            girdi = document.getElementById("girdi")
            responded = girdi.children[0].id !== undefined && girdi.children[0].id !== "";
            if (responded) responseId = girdi.children[0].id
            fetch('/addComment?content=' + encodeURIComponent(inputfield.value) + "&headId=" + headId + "&responseId=" + responseId)
                .then(response => response.json())
                .then(data => {
                    element = createComment(data);
                    if (data.response !== undefined) girdi.removeChild(girdi.children[0])
                    postlar = document.getElementsByClassName("postlar")
                    postlar[0].insertBefore(element, holders[holders.length - 1]);
                    document.getElementById("message").focus()
                    inputfield.value = ''
                    setTimeout(() => {
                        holders = document.getElementsByClassName("holder")
                        holders[holders.length - 2].scrollIntoView({ behavior: "smooth", block: "center", inline: "nearest" });
                        console.log("oldu!")
                    }, 1)
                })
        }
    }
}

yanitla = (e) => {
    setTimeout(() => {
        if (yanitlayabilir) {
            element = e.cloneNode(true);
            if (element.children[0].className == "response") {
                element.removeChild(element.children[0])
            }
            else console.log("response ddeğil")
            element.className = "response"
            girdi = document.getElementById("girdi")
            girdi.prepend(element)
            document.getElementById("message").focus()
            setTimeout(() => {
                holders = document.getElementsByClassName("holder")
                holders[holders.length - 2].scrollIntoView({ behavior: "smooth", block: "start", inline: "nearest" });
                console.log("oldu!")
            }, 300)
            yanitlayabilir = false;
        }
    }, 100)
}

if (window.location.pathname === "/post") {
    if (inputfield !== null) document.getElementById("message").focus()
    holders = document.getElementsByClassName("holder")
    holders[holders.length - 2].scrollIntoView({ behavior: "smooth", block: "center", inline: "nearest" });
}

responses = document.getElementsByClassName("response")
for (var i = 0; i < responses.length; i++) {
    responses[i].click = click(responses[i])
}
canGoHeadline = true
deleteHeadline = (id) => {
    console.log("deleteHeadline ", id)
    canGoHeadline = false
    fetch('/deleteHeadline?id=' + encodeURIComponent(id))
        .then(response => response.text())
        .then(data => {
            console.log("data: ", data)
            canGoHeadline = true
            window.location.href = "/";

        })
}

deleteComment = (id) => {
    yanitlayabilir = false
    fetch('/delComment?id=' + encodeURIComponent(id))
        .then(response => response.json())
        .then(data => {
            console.log("data: ", data)

            try {
                document.getElementById("postlar").removeChild(document.getElementById(id))
            } catch (error) {
                console.log(error)
            }

            setTimeout(() => {
                yanitlayabilir = true
            }, 500)
        })
}

goHeadline = (id) => {
    setTimeout(() => {

        if (canGoHeadline) window.location = '/post?id=' + id;
    }, 100)
}

changeCanComment = (id, val) => {
    canGoHeadline = false
    fetch('/canComment?id=' + encodeURIComponent(id) + "&val=" + encodeURIComponent(val))
        .then(response => response.text())
        .then(data => {
            console.log("data: ", data)
            setTimeout(() => {
                canGoHeadline = true
            }, 110)
            
            if(window.location.pathname == "/post") window.location.href = window.location.pathname + "?id="+id;
            else window.location.href = window.location.pathname + "?id="+id;

        })
}