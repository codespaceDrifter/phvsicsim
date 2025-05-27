import { globals } from './global.js';

window.addEventListener('keydown', (event) => {
  if (event.key === 'ArrowRight') {
    globals.speed += 1;
  } else if (event.key === 'ArrowLeft') {
    globals.speed -= 1;
    if (globals.speed < 1) {
      globals.speed = 1;
    }
  } else if (event.key === 'r') {
    globals.frame = 0;
    globals.chunk = 0;
  }
  speedDiv.textContent = `Speed: ${globals.speed}x`;
});

document.querySelectorAll('.world-button').forEach(item => {
  item.addEventListener('click', (event) => {
    const worldName = event.target.textContent;
    globals.world = worldName;
    globals.frame = 0;
    globals.chunk = 0;
  });
});