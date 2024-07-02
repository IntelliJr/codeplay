let minutes = 0;
let seconds = 0;

function stopWatch() {
    seconds++;

    if (seconds == 60) {
        minutes++;
        seconds = 0;
    }

    let minString = minutes;
    let secString = seconds;

    if (minutes < 10) {
        minString = "0" + minString;
    }

    if (seconds < 10) {
        secString = "0" + secString;
    }

    document.getElementById('min').innerHTML = minString;
    document.getElementById('sec').innerHTML = secString;

    setTimeout(stopWatch, 1000);

    sessionStorage.setItem('minutes', minutes);
    sessionStorage.setItem('seconds', seconds);
}

document.addEventListener("DOMContentLoaded", function() {
    stopWatch();
    console.log('Stopwatch script started.');
});
