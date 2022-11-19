let darkMode = localStorage.getItem('darkMode'); 

const themeToggle = document.querySelector('#theme-toggle');

const enableDarkMode = () => {
  document.getElementById('darkModeCss').href = "/static/css/themes/darkmode.css"
  themeToggle.src = "/static/images/icons/sun.png";
  localStorage.setItem('darkMode', 'enabled');
}

const disableDarkMode = () => {
  document.getElementById('darkModeCss').href = "/static/css/themes/lightmode.css";
  themeToggle.src = "/static/images/icons/moon.png";
  localStorage.setItem('darkMode', 'disabled');
}

if (darkMode === 'enabled') {
  enableDarkMode();
}

function toggleTheme(button) {
  darkMode = localStorage.getItem('darkMode'); 
  if (darkMode !== 'enabled') {
    button.src = "/static/images/icons/sun.png";
    enableDarkMode();
  } 
  else {
    button.src = "/static/images/icons/moon.png";
    disableDarkMode(); 
  }
}