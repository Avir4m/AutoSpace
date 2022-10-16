let darkMode = localStorage.getItem('darkMode'); 

const darkModeToggle = document.querySelector('#dark-mode-toggle');

const enableDarkMode = () => {
  document.getElementById('darkModeCss').href = "/static/css/darkmode.css"
  document.getElementById('dark-mode-toggle').src = "/static/images/icons/sun.png";
  localStorage.setItem('darkMode', 'enabled');
}

const disableDarkMode = () => {
  document.getElementById('darkModeCss').href = "/static/css/lightmode.css";
  document.getElementById('dark-mode-toggle').src = "/static/images/icons/moon.png";
  localStorage.setItem('darkMode', 'disabled');
}

if (darkMode === 'enabled') {
  enableDarkMode();
}


darkModeToggle.addEventListener('click', () => {
  darkMode = localStorage.getItem('darkMode'); 
  if (darkMode !== 'enabled') {
    enableDarkMode();
  } 
  else {  
    disableDarkMode(); 
  }});