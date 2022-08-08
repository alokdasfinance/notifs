
function setup() {
  var wshShell = new ActiveXObject("WScript.Shell");
  submit = document.getElementById('newbutton');
  username = document.getElementById('username').value;
  password = document.getElementById('password').value;
}

function draw() {

}

function verify() {
  if (username == "5" && password == "5") {
    wshShell.Run("C:\Users\wonde\Algo\auto.bat");
  }

}
