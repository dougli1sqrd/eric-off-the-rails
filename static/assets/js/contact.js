function sendMessage() {
    document.getElementById("status").innerHTML = "";
    document.getElementById("name").checkValidity();

    var formElements = [document.getElementById("name"), document.getElementById("emailfield"), document.getElementById("subject"), document.getElementById("message")];

    if (!formValid(formElements)) {
        return
    }

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // document.getElementById("hello-text").innerHTML = "hello world";
            window.location.href = "/pages/contact-thanks";
        } else if (this.status >= 400) {
            document.getElementById("status").innerHTML = "Could not send message!<br>Try opening an issue for the <a href='https://github.com/dougli1sqrd/eric-off-the-rails'>blog on github</a>";
            enableForm()
        }
    };
    var name = document.getElementById("name").value;
    var email = document.getElementById("emailfield").value;
    var subject = document.getElementById("subject").value;
    var message = document.getElementById("message").value;

    xhttp.open("POST", "/cgi-bin/contact.py", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send(`name=${name}&email=${email}&subject=${subject}&message=${message}`);
    document.getElementById("status").innerHTML = "Sending...";
    disableForm()
}

function enableForm() {
    document.getElementById("name").disabled = false;
    document.getElementById("emailfield").disabled = false;
    document.getElementById("subject").disabled = false;
    document.getElementById("message").disabled = false;
    document.getElementById("send").disabled = false;
}

function disableForm() {
    document.getElementById("name").disabled = true;
    document.getElementById("emailfield").disabled = true;
    document.getElementById("subject").disabled = true;
    document.getElementById("message").disabled = true;
    document.getElementById("send").disabled = true;
}

function formValid(elements) {
    var valid = true;
    elements.forEach(function (el, i) {
        if (!el.checkValidity()) {
            valid = false;
        }
    });
    return valid;
}
