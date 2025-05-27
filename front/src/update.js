import * as THREE from "three";
import { scene } from './camera.js';

// Object storage
export const objects = new Map();




// Update simulation objects based on data
export function updateSimulation(data) {
  const {
    CurTime,
    IDArray,
    PositionArrays,
    VertexArrays,
    IndexArrays,
    ColorArray,
  } = data;

  // Update the elapsed time display
  const elapsedTimeDiv = document.getElementById("elapsed-time");
  if (elapsedTimeDiv && typeof CurTime === "number") {
    elapsedTimeDiv.textContent = `Time: ${(CurTime / 1000).toFixed(2)}s`;
  }

  IDArray.forEach((id, index) => {
    const objData = {
      positions: PositionArrays[index],
      vertexes: VertexArrays[index],
      indices: IndexArrays[index],
      color: ColorArray[index],
    };

    if (!objects.has(id)) {
      createObject(id, objData, scene);
    } else {
      updateObject(id, objData);
    }
  });

  // Remove objects that no longer exist in the simulation
  for (const id of objects.keys()) {
    if (!IDArray.includes(id)) {
      scene.remove(objects.get(id));
      objects.delete(id);
    }
  }
}

// Create a new 3D object
export function createObject(id, objData, scene) {
  var { positions, vertexes, indices, color } = objData;
  vertexes = new Float32Array(vertexes);
  indices = new Uint32Array(indices);

  // Create BufferGeometry
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute(
    "position",
    new THREE.Float32BufferAttribute(vertexes, 3),
  );
  geometry.setIndex(new THREE.BufferAttribute(indices, 1));

  // Create material using provided color or random fallback
  const material = new THREE.MeshStandardMaterial({
    color: color
      ? new THREE.Color(color)
      : new THREE.Color(Math.random(), Math.random(), Math.random()),
    roughness: 0.7,
    metalness: 0.3,
  });

  // Create mesh
  const threeMesh = new THREE.Mesh(geometry, material);
  threeMesh.position.set(positions[0], positions[1], positions[2]);

  // Create edges
  const edges = new THREE.EdgesGeometry(geometry);
  const lineMaterial = new THREE.LineBasicMaterial({ color: 0xffffff });
  const wireframe = new THREE.LineSegments(edges, lineMaterial);

  // Add wireframe to mesh
  threeMesh.add(wireframe);


  // Add to scene
  scene.add(threeMesh);

  // Store reference
  objects.set(id, threeMesh);
}

// Update an existing 3D object
export function updateObject(id, objData) {
  const object = objects.get(id);

  // Update position
  object.position.set(
    objData.positions[0],
    objData.positions[1],
    objData.positions[2],
  );
}

