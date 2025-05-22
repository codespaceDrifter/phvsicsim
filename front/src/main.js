import { 
  createScene, 
  createCamera, 
  createRenderer, 
  createControls, 
  setupResizeHandler 
} from './camera.js';

import {
  FETCH_INTERVAL,
  fetchSimulationData,
  setupKeyControls
} from './update.js';

let curWorld = "rocketLaunch";

// Initialize core components
const scene = createScene();
const camera = createCamera();
const renderer = createRenderer();
const controls = createControls(camera, renderer);

// Setup window resize handler
setupResizeHandler(camera, renderer);

// Setup keyboard controls
setupKeyControls(curWorld);

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

// Fetch simulation data regularly
setInterval(() => fetchSimulationData(scene, curWorld), FETCH_INTERVAL);