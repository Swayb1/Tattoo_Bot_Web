function playAudio(style) {
    const audio = new Audio(`/play_audio/${style}`);
    audio.play();
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('TattooBot is ready!');
});
