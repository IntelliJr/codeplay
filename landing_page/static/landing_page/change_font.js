function changeFont(font) {
    localStorage.setItem("fontPreference", font);
    applyFont(font);
}

function applyFont(font) {
    let docElements = document.querySelectorAll('*');
    docElements.forEach(function(element) { element.style.fontFamily = font; }); 
}

// wrapper-y
function applyStoredFont() {
    let storedFont = localStorage.getItem("fontPreference");
    applyFont(storedFont);
}

function applyMonospace() {
    let docElements = document.querySelectorAll('*');
    docElements.forEach(function(element) { element.style.fontFamily = 'monospace' });
}

function applyFontDiffZero() {
    if (localStorage.getItem("fontDiff") === null || localStorage.getItem("fontDiff") == 0) { return; }

    localStorage.setItem("fontDiff", 0);
    let textElements = document.querySelectorAll('.adjust-font');
    textElements.forEach(function(element) {
        let elemStyle = window.getComputedStyle(element);
        let currentFontSize = parseFloat(elemStyle.getPropertyValue('font-size'));
        let newFontSize = currentFontSize + fontDiff;
        element.style.fontSize = newFontSize + "px";
    });
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