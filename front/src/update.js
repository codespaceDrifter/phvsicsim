import * as THREE from "three";
import { scene, camera, controls } from './camera.js';
import { globals } from './global.js';

// Object storage
export const objects = new Map();

export function FindClosestID() {
  let Closest = null;
  let MinDist = Infinity;
  for (const [CurID, Obj] of objects.entries()) {
    const Dist = Obj.position.length();
    if (Dist < MinDist) {
      MinDist = Dist;
      Closest = CurID;
    }
  }
  return Closest;
}

export function TeleportToID(id) {
  const Obj = objects.get(id);
  if (!Obj) {
    return;
  }
  const Geometry = Obj.geometry;
  if (Geometry && !Geometry.boundingSphere) {
    Geometry.computeBoundingSphere();
  }
  const Radius = Geometry && Geometry.boundingSphere
    ? Geometry.boundingSphere.radius
    : 10;
  const Offset = new THREE.Vector3(Radius * 3, Radius * 3, Radius * 3);
  camera.position.copy(Obj.position).add(Offset);
  controls.target.copy(Obj.position);
}

export function LockOnID(id) {
  if (globals.LockedID && objects.has(globals.LockedID)) {
    const PrevObj = objects.get(globals.LockedID);
    if (PrevObj.userData.wireframe) {
      PrevObj.userData.wireframe.material.color.set(0xffffff);
    }
  }

  globals.LockedID = id;

  if (objects.has(id)) {
    const NewObj = objects.get(id);
    if (NewObj.userData.wireframe) {
      NewObj.userData.wireframe.material.color.set(0xffa500);
    }
  }

  TeleportToID(id);
}




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
      if (globals.LockedID === id) {
        globals.LockedID = null;
      }
      objects.delete(id);
    }
  }

  if (!globals.LockedID) {
    const Closest = FindClosestID();
    if (Closest) {
      LockOnID(Closest);
    }
  }

  if (globals.LockedID && objects.has(globals.LockedID)) {
    controls.target.copy(objects.get(globals.LockedID).position);
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
  threeMesh.userData.wireframe = wireframe;
  if (globals.LockedID === id) {
    wireframe.material.color.set(0xffa500);
  }


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

