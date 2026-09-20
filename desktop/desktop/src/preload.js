const { ipcRenderer } = require('electron');

// ── Media Control Bridge ────────────────────────────────────────────
// Routes IPC messages from main process → DOM interactions
// Works by clicking the web app's play/pause/next buttons or
// toggling HTML5 <audio> elements directly.

window.addEventListener('DOMContentLoaded', () => {

    ipcRenderer.on('media-play-pause', () => {
        // Strategy 1: Click the web app's play/pause button
        const playBtn = document.querySelector(
            'button[aria-label="Play"], button[aria-label="Pause"], ' +
            '.play-button, .play-pause-btn, [data-action="play"], [data-action="pause"]'
        );
        if (playBtn) {
            playBtn.click();
            return;
        }

        // Strategy 2: Toggle any <audio> element
        const audio = document.querySelector('audio');
        if (audio) {
            if (audio.paused) {
                audio.play().catch(() => { });
            } else {
                audio.pause();
            }
        }
    });

    ipcRenderer.on('media-next-track', () => {
        const nextBtn = document.querySelector(
            'button[aria-label="Next"], .next-button, .next-station-btn, [data-action="next"]'
        );
        if (nextBtn) nextBtn.click();
    });

    ipcRenderer.on('media-previous-track', () => {
        const prevBtn = document.querySelector(
            'button[aria-label="Previous"], .prev-button, .prev-station-btn, [data-action="previous"]'
        );
        if (prevBtn) prevBtn.click();
    });
});
