function showPassword(number) {
  if (number === 0) {
    var input = document.getElementById(`password`);
    var img = document.getElementById(`icon-eye`)
  } else {
    var input = document.getElementById(`password${number}`);
    var img = document.getElementById(`icon-eye${number}`)
  }
  if (input.type === "password") {
    input.type = "text";
    img.src = "/static/images/icons/eye.png";
  } else {
    input.type = "password";
    img.src = "/static/images/icons/eye-crossed.png";
  }
}

function copyPostLink(url) {
  link = location.protocol + '//' + location.host + '/post/' + url;
  navigator.clipboard.writeText(link);
}