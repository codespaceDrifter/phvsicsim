import { 
  scene,
  camera,
  renderer,
  controls
} from './camera.js';

import { globals } from './global.js';
import './control.js';
import { step } from './playback.js';



// Setup window resize handler

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

