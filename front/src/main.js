import { 
  createScene, 
  createCamera, 
  createRenderer, 
  createControls, 
  setupResizeHandler 
} from './camera.js';

import { loadChunk } from './playback.js';
import { globals } from './global.js';
import './control.js';



// Initialize core components
const scene = createScene();
const camera = createCamera();
const renderer = createRenderer();
const controls = createControls(camera, renderer);

const worlds = ["rocketLaunch", "threeBody"]

// Setup window resize handler
setupResizeHandler(camera, renderer);

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

initWorldList();
loadChunk(scene);
