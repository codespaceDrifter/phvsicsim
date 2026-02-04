/**
 * User input controls module.
 * Handles keyboard input and world selection UI.
 */
import { playback, availableWorlds } from './state.js';
import { reset } from './playback.js';

const speedDisplay = document.getElementById('play-speed');

// Keyboard controls
window.addEventListener('keydown', (event) => {
  switch (event.key) {
    case 'ArrowRight':
      playback.speed += 1;
      break;
    case 'ArrowLeft':
      playback.speed = Math.max(1, playback.speed - 1);
      break;
    case 'r':
      reset();
      break;
  }
  speedDisplay.textContent = `Speed: ${playback.speed}x`;
});

// Initialize world selection buttons
function initWorldList() {
  const listDiv = document.getElementById('world-list');
  availableWorlds.forEach((worldName) => {
    const button = document.createElement('div');
    button.textContent = worldName;
    button.className = 'world-button';
    button.addEventListener('click', () => {
      playback.world = worldName;
      reset();
    });
    listDiv.appendChild(button);
  });
}

initWorldList();
