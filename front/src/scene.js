/**
 * Three.js scene setup and management.
 * Handles camera, renderer, controls, and resize events.
 */
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// Create scene with lighting
function createScene() {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x000000);

  // Ambient light for base illumination
  const ambientLight = new THREE.AmbientLight(0xffffff);
  scene.add(ambientLight);

  // Directional light for shadows/depth
  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
  directionalLight.position.set(1, 1, 1);
  scene.add(directionalLight);

  // Axes helper for orientation
  const axesHelper = new THREE.AxesHelper(1000);
  scene.add(axesHelper);

  return scene;
}

// Create perspective camera
function createCamera() {
  const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    1,
    1_000_000
  );
  camera.position.set(100, 100, 100);
  camera.lookAt(0, 0, 0);
  return camera;
}

// Create WebGL renderer
function createRenderer() {
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(window.devicePixelRatio);
  document.body.appendChild(renderer.domElement);
  return renderer;
}

// Create orbit controls
function createControls(camera, renderer) {
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.enablePan = true;
  controls.mouseButtons = {
    LEFT: THREE.MOUSE.ROTATE,
    MIDDLE: THREE.MOUSE.DOLLY,
    RIGHT: THREE.MOUSE.PAN,
  };
  return controls;
}

// Setup resize handler
function setupResizeHandler(camera, renderer) {
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });
}

// Initialize and export scene components
export const scene = createScene();
export const camera = createCamera();
export const renderer = createRenderer();
export const controls = createControls(camera, renderer);

setupResizeHandler(camera, renderer);
