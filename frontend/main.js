import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// Scene setup
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x1a1a2e);

// Camera setup
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(10, 10, 15);
camera.lookAt(0, 0, 0);

// Renderer setup
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
document.body.appendChild(renderer.domElement);

// Controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;

// Lights
const ambientLight = new THREE.AmbientLight(0x404040);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
directionalLight.position.set(1, 1, 1);
scene.add(directionalLight);

// Grid helper
const gridHelper = new THREE.GridHelper(20, 20);
scene.add(gridHelper);

// Axes helper
const axesHelper = new THREE.AxesHelper(5);
scene.add(axesHelper);

// Object storage
const objects = new Map();

// Handle window resize
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// Fetch simulation data from server
async function fetchSimulationData() {
  try {
    const response = await fetch('http://localhost:8000/simulation');
    const data = await response.json();
    
    updateSimulation(data);
    
    // Update elapsed time display
    document.getElementById('elapsed-time').textContent = data.elapsedTime.toFixed(2);
    
  } catch (error) {
    console.error('Error fetching simulation data:', error);
  }
}

// Update simulation objects based on data
function updateSimulation(data) {
  // Handle existing objects
  for (const [id, objData] of Object.entries(data.objects)) {
    if (!objects.has(id)) {
      // Create new object if it doesn't exist
      createObject(id, objData);
    } else {
      // Update existing object
      updateObject(id, objData);
    }
  }
  
  // Remove objects that no longer exist in the simulation
  for (const id of objects.keys()) {
    if (!data.objects[id]) {
      scene.remove(objects.get(id).mesh);
      objects.delete(id);
    }
  }
}

// Create a new 3D object
function createObject(id, data) {
  const { position, size } = data;
  
  // Create box geometry based on size
  const geometry = new THREE.BoxGeometry(size[0], size[1], size[2]);
  
  // Create material with random color
  const material = new THREE.MeshStandardMaterial({ 
    color: new THREE.Color(Math.random(), Math.random(), Math.random()),
    roughness: 0.7,
    metalness: 0.3
  });
  
  // Create mesh
  const mesh = new THREE.Mesh(geometry, material);
  mesh.position.set(position[0], position[1], position[2]);
  
  // Add to scene
  scene.add(mesh);
  
  // Store reference
  objects.set(id, { mesh, data });
}

// Update an existing 3D object
function updateObject(id, newData) {
  const object = objects.get(id);
  
  // Update position
  object.mesh.position.set(
    newData.position[0],
    newData.position[1],
    newData.position[2]
  );
  
  // Update data reference
  object.data = newData;
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

// Fetch simulation data regularly
setInterval(fetchSimulationData, 100); // 10 times per second