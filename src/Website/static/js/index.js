function showPassword(number) {
    if (number === 0) {
      const input = document.getElementById(`password`);
      const img = document.getElementById(`icon-eye`)
    } else {
      const input = document.getElementById(`password${number}`);
      const img = document.getElementById(`icon-eye${number}`)
    }
    if (input.type === "password") {
      input.type = "text";
      img.src = "/static/images/icons/eye.png";
    } else {
      input.type = "password";
      img.src = "/static/images/icons/eye-crossed.png";
    }
}

function alertClose() {
  const messages = document.querySelector(".messages");
  messages.remove();
}

let images = document.images;
lazyload(images);