function changeFont(font) {
    localStorage.setItem("fontPreference", font);
    applyFont(font);
}

function applyFont(font) {
    let docElements = document.querySelectorAll('*');
    docElements.forEach(function(element) { element.style.fontFamily = font; }); 
}

// wrapper
function applyStoredFont() {
    let storedFont = localStorage.getItem("fontPreference");
    applyFont(storedFont);
}

// checkbox function
function toggleFont() { 
    if (document.getElementById('font_checkbox').checked === true) {
      changeFont('Open-Dyslexic');
    } else {
      changeFont('monospace');
    }
}

// only for the dashboard (dashboard.html)
function restoreToggleState() {
  let storedFont = localStorage.getItem("fontPreference");
  if (storedFont === "Open-Dyslexic") {
    document.getElementById('font_checkbox').checked = true;
  } else if (storedFont === "monospace") {
    document.getElementById('font_checkbox').checked = false;
  }
}

function applyStoredFontSize() {
  if (localStorage.getItem("fontDiff") === null || localStorage.getItem("fontDiff") == 0) { return; }

  let fontDiff = Number(localStorage.getItem("fontDiff"));
  let textElements = document.querySelectorAll('.adjust-font');
  textElements.forEach(function(element) {
    let elemStyle = window.getComputedStyle(element);
    let currentFontSize = parseFloat(elemStyle.getPropertyValue('font-size'));
    let newFontSize = currentFontSize + fontDiff;
    element.style.fontSize = newFontSize + "px";
  });
}