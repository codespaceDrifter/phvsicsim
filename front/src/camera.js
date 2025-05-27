import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { globals } from './global.js';

// Initialize scene
function createScene() {
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
  //scene.add(gridHelper);

  // Axes helper - made much longer
  const axesHelper = new THREE.AxesHelper(1000);
  scene.add(axesHelper);
  
  return scene;
}

// Initialize camera
function createCamera() {
  const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 1_000_000);
  camera.position.set(100, 100, 100);
  camera.lookAt(0, 0, 0);
  return camera;
}

// Initialize renderer
function createRenderer() {
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(window.devicePixelRatio);
  document.body.appendChild(renderer.domElement);
  return renderer;
}

// Initialize controls
function createControls(camera, renderer) {
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

// Initialize core components
export const scene = createScene();
export const camera = createCamera();
export const renderer = createRenderer();
export const controls = createControls(camera, renderer);

setupResizeHandler(camera, renderer);

export function FindClosestID(map) {
  let closest = null;
  let minDist = Infinity;
  for (const [id, obj] of map.entries()) {
    const dist = obj.position.length();
    if (dist < minDist) {
      minDist = dist;
      closest = id;
    }
  }
  return closest;
}

function teleportToObject(obj) {
  if (!obj) {
    return;
  }
  const geom = obj.geometry;
  if (!geom.boundingSphere) {
    geom.computeBoundingSphere();
  }
  const radius = geom.boundingSphere.radius;
  const offset = new THREE.Vector3(radius * 3, radius * 3, radius * 3);
  camera.position.copy(obj.position).add(offset);
  controls.target.copy(obj.position);
  controls.update();
}

export function LockOnID(map, id) {
  const obj = map.get(id);
  if (!obj) {
    return;
  }
  globals.LockedID = id;
  teleportToObject(obj);
}

