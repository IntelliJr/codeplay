document.addEventListener('DOMContentLoaded', function() {
    var button = document.getElementById("readStatsButton");
    var audioPlayed = 0;

    button.addEventListener("click", function() {
        // Reset audioPlayed count when the button is clicked so that when it's clicked again, it plays the audio. 
        audioPlayed = 0;

        var stats = document.getElementById("stats");
        var statsText = stats.innerText;

        if ('speechSynthesis' in window) {
            var utter = new SpeechSynthesisUtterance();
            var speechVoices = speechSynthesis.getVoices();

            // Check if voices are loaded, if not, wait for some time. 
            //(this solved stupid problems where i think it uses the default voice cuz the list didnt load completely.)
            if (speechVoices.length === 0) {
                setTimeout(function() {
                    speechVoices = speechSynthesis.getVoices();
                    utter.voice = speechVoices[114]; 
                    utter.text = statsText;
                    speechSynthesis.speak(utter);
                    audioPlayed++;
                }, 100);
            } else {
                utter.voice = speechVoices[114]; 
                utter.text = statsText;
                speechSynthesis.speak(utter);
                audioPlayed++;
            }
        }
    });
});
