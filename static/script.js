var input_1 = document.getElementById("player-1");
var input_2 = document.getElementById("player-2");
var find = document.getElementById("find");

if (input_1.value === "")
  input_1.focus();
else if (input_2.value === "")
  input_2.focus();

String.prototype.remove = function() {
  var str = this;
  for (var i = 0; i < arguments.length; i++)
    str = str.split(arguments[i]).join("");
  return str;
}

function submit() {
  var player_1 = input_1.value.remove("/", "\\").trim();
  var player_2 = input_2.value.remove("/", "\\").trim();

  input_1.value = player_1;
  input_2.value = player_2;

  if (player_1 === "")
    input_1.focus();
  else if (player_2 === "")
    input_2.focus();
  else if (player_1 === "Paul Morphy")
    window.location.href = "/find/" + player_2 + "/";
  else
    window.location.href = "/find/" + player_1 + "/" + player_2 + "/";
}

function onkeydown(e) {
  if (e.keyCode == 13 && !e.repeat)
    submit();
};

input_1.addEventListener("keydown", onkeydown);
input_2.addEventListener("keydown", onkeydown);
find.addEventListener("click", submit);
