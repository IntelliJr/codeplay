let editor;

window.onload = function () {
    editor = ace.edit("editor");
    editor.setTheme("ace/theme/dracula");
    editor.session.setMode("ace/mode/java")

    editor.setOptions({
        highlightSelectedWord: true,
        fontFamily: 'monospace',
        fontSize: '12pt',
        enableBasicAutocompletion: true,
        enableLiveAutocompletion: true,
        enableKeyboardAccessibility: true,
        newLineMode: "unix",
    });
}
