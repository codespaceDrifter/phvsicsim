import { 
  scene,
  camera,
  renderer,
  controls
} from './camera.js';

import { globals } from './global.js';
import './control.js';
import { step } from './playback.js';


const worlds = ["rocketLaunch", "threeBody"]

// Setup window resize handler

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

// Animation loop
function animate() {
  requestAnimationFrame(animate);
  
  // Update controls
  controls.update();
  
  // Render
  renderer.render(scene, camera);
}

// Start animation
animate();

step();

initWorldList();
