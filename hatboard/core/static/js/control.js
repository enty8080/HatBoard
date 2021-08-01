function set_close() {
    var select = document.getElementById('close');
    var value = select.options[select.selectedIndex].value;
    self.close = value;
}

function close_session() {
    document.location.reload();
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", "http://127.0.0.1:8008/sessions?close=" + self.close, false);
    xmlHttp.send(null);
}

function set_command() {
    var select = document.getElementById('command');
    var value = select.options[select.selectedIndex].value;
    self.command = value;
}

function execute_command() {
    var value = document.getElementById("command_value").value;
    var xmlHttp = new XMLHttpRequest();

    document.getElementById("command_value").value = "";
    var url = "http://127.0.0.1:8008/sessions?output=yes&command=" + value + "&id=" + self.command;

    xmlHttp.open('GET', url, false);
    xmlHttp.send(null);

    var output = '<pre>' + xmlHttp.responseText.replaceAll('"', '') + '</pre>';
    document.getElementById("command_output").innerHTML = output.replaceAll('\\n', '<br>');
}
