/**
 * Main entry point for the physics simulation viewer.
 * Initializes the Three.js render loop and starts playback.
 */
import { scene, camera, renderer, controls } from './scene.js';
import './controls.js';
import { step } from './playback.js';

// Animation loop
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}

// Start
animate();
step();
