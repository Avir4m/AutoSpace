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

function timeSince(date) {
  var seconds = Math.floor((new Date() - date) / 1000);
  var interval = Math.floor(seconds / 31536000);

  if (interval > 1) {
      return interval + " years";
  }
  interval = Math.floor(seconds / 2592000);
  if (interval > 1) {
      return interval + " months";
  }
  interval = Math.floor(seconds / 86400);
  if (interval > 1) {
      return interval + " days";
  }
  interval = Math.floor(seconds / 3600);
  if (interval > 1) {
      return interval + " hours";
  }
  interval = Math.floor(seconds / 60);
  if (interval > 1) {
      return interval + " minutes";
  }
  return Math.floor(seconds) + " seconds";
}

function changeDate() {
  var dates = document.getElementsByClassName('date');

  for (var i = 0; i < dates.length; i++) {
    var date = new Date(dates[i].textContent);
    dates[i].innerHTML = timeSince(date) + " ago";
  }
}

changeDate();