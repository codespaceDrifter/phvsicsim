import { globals } from './global.js';
import { reset } from './playback.js';

const speedDiv = document.getElementById('play-speed');

window.addEventListener('keydown', (event) => {
  if (event.key === 'ArrowRight') {
    globals.speed += 1;
  } else if (event.key === 'ArrowLeft') {
    globals.speed -= 1;
    if (globals.speed < 1) {
      globals.speed = 1;
    }
  } else if (event.key === 'r') {
    reset();
  }
  speedDiv.textContent = `Speed: ${globals.speed}x`;
});

const worlds = ["rocketLaunch", "threeBody"]

function initWorldList() {
  const listDiv = document.getElementById('world-list');
  worlds.forEach((w) => {
    const item = document.createElement('div');
    item.textContent = w;
    item.className = 'world-button';
    item.style.cursor = 'pointer';
    listDiv.appendChild(item);
  });
}

initWorldList();


document.querySelectorAll('.world-button').forEach(item => {
  item.addEventListener('click', (event) => {
    const worldName = event.target.textContent;
    globals.world = worldName;
    reset();
  });
});