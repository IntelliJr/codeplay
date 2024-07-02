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