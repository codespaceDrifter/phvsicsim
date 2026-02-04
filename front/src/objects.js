/**
 * Object management module.
 * Handles creation, update, and removal of Three.js meshes from simulation data.
 *
 * Frame data format (from api.js):
 * {
 *   curTime: number,
 *   idArray: string[],
 *   positionArrays: number[][],      // [x, y, z] per object
 *   rotationArrays: number[][],      // 9 floats row-major 3x3 matrix per object
 *   vertexArrays: number[][],        // flat vertex positions per object
 *   indexArrays: number[][],         // triangle indices per object
 *   colorArray: string[],            // hex color per object
 * }
 */
import * as THREE from 'three';
import { scene } from './scene.js';

// Map of object ID -> Three.js Mesh
const objects = new Map();

/**
 * Update the simulation display with new frame data.
 * @param {Object} frameData - Decoded frame data from api.js
 */
export function updateSimulation(frameData) {
  const {
    curTime,
    idArray,
    positionArrays,
    rotationArrays,
    vertexArrays,
    indexArrays,
    colorArray,
  } = frameData;

  // Update time display
  const elapsedTimeDiv = document.getElementById('elapsed-time');
  if (elapsedTimeDiv && typeof curTime === 'number') {
    elapsedTimeDiv.textContent = `Time: ${(curTime / 1000).toFixed(2)}s`;
  }

  // Update or create each object
  idArray.forEach((id, index) => {
    const objectData = {
      position: positionArrays[index],
      rotation: rotationArrays[index],
      vertices: vertexArrays[index],
      indices: indexArrays[index],
      color: colorArray[index],
    };

    if (objects.has(id)) {
      updateObject(id, objectData);
    } else {
      createObject(id, objectData);
    }
  });

  // Remove objects that no longer exist
  for (const id of objects.keys()) {
    if (!idArray.includes(id)) {
      removeObject(id);
    }
  }
}

/**
 * Create a new Three.js mesh for a physics object.
 * @param {string} id - Object identifier
 * @param {Object} data - Object data (position, rotation, vertices, indices, color)
 */
function createObject(id, data) {
  const { position, rotation, vertices, indices, color } = data;

  // Create geometry from vertices and indices
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute(
    'position',
    new THREE.Float32BufferAttribute(new Float32Array(vertices), 3)
  );
  geometry.setIndex(new THREE.BufferAttribute(new Uint32Array(indices), 1));

  // Create material with object color
  const material = new THREE.MeshStandardMaterial({
    color: color ? new THREE.Color(color) : new THREE.Color(0xffffff),
    roughness: 0.7,
    metalness: 0.3,
  });

  // Create mesh and set position
  const mesh = new THREE.Mesh(geometry, material);
  mesh.position.set(position[0], position[1], position[2]);

  // Apply rotation matrix (9 floats row-major -> Matrix4 column-major)
  if (rotation && rotation.length === 9) {
    applyRotationMatrix(mesh, rotation);
  }

  // Add wireframe edges
  const edges = new THREE.EdgesGeometry(geometry);
  const lineMaterial = new THREE.LineBasicMaterial({ color: 0xffffff });
  const wireframe = new THREE.LineSegments(edges, lineMaterial);
  mesh.add(wireframe);
  mesh.userData.wireframe = wireframe;

  // Add to scene and store reference
  scene.add(mesh);
  objects.set(id, mesh);
}

/**
 * Update an existing mesh with new data.
 * @param {string} id - Object identifier
 * @param {Object} data - Object data (position, rotation)
 */
function updateObject(id, data) {
  const mesh = objects.get(id);
  if (!mesh) return;

  // Update position
  mesh.position.set(data.position[0], data.position[1], data.position[2]);

  // Update rotation if provided
  if (data.rotation && data.rotation.length === 9) {
    applyRotationMatrix(mesh, data.rotation);
  }
}

/**
 * Remove an object from the scene.
 * @param {string} id - Object identifier
 */
function removeObject(id) {
  const mesh = objects.get(id);
  if (mesh) {
    scene.remove(mesh);
    objects.delete(id);
  }
}

/**
 * Apply a row-major 3x3 rotation matrix to a mesh.
 * @param {THREE.Mesh} mesh - Target mesh
 * @param {number[]} rotation - 9 floats representing row-major 3x3 matrix
 */
function applyRotationMatrix(mesh, rotation) {
  // Convert row-major 3x3 to column-major 4x4 (Three.js format)
  const matrix = new THREE.Matrix4();
  matrix.set(
    rotation[0], rotation[1], rotation[2], 0,
    rotation[3], rotation[4], rotation[5], 0,
    rotation[6], rotation[7], rotation[8], 0,
    0, 0, 0, 1
  );
  mesh.rotation.setFromRotationMatrix(matrix);
}

/**
 * Clear all objects from the scene.
 */
export function clearObjects() {
  for (const [id, mesh] of objects.entries()) {
    scene.remove(mesh);
  }
  objects.clear();
}
