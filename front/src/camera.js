import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// Initialize scene
export function createScene() {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x000000);
  
  // Lights
  const ambientLight = new THREE.AmbientLight(0xffffff);
  scene.add(ambientLight);

  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
  directionalLight.position.set(1, 1, 1);
  scene.add(directionalLight);

  // Grid helper
  const gridHelper = new THREE.GridHelper(100, 100);
  scene.add(gridHelper);

  // Axes helper - made much longer
  const axesHelper = new THREE.AxesHelper(1000);
  scene.add(axesHelper);
  
  return scene;
}

// Initialize camera
export function createCamera() {
  const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.set(10, 10, 15);
  camera.lookAt(0, 0, 0);
  return camera;
}

// Initialize renderer
export function createRenderer() {
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(window.devicePixelRatio);
  document.body.appendChild(renderer.domElement);
  return renderer;
}

// Initialize controls
export function createControls(camera, renderer) {
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;

  // Configure mouse buttons:
  // LEFT click = rotate
  // RIGHT click = pan (move)
  // MIDDLE click = zoom
  controls.mouseButtons = {
    LEFT: THREE.MOUSE.ROTATE,
    MIDDLE: THREE.MOUSE.DOLLY,
    RIGHT: THREE.MOUSE.PAN
  };

  // Make sure panning is enabled and set some reasonable limits
  controls.enablePan = true;
  
  return controls;
}

// Setup window resize handler
export function setupResizeHandler(camera, renderer) {
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });
}
