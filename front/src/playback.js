import { fetchRecording } from './api.js';
import { updateSimulation, objects } from './update.js';
import { globals, cache } from './global.js';
import { scene } from './camera.js';

const FrameInterval = 1000 / 30;
let Timer = null;

export async function step() {

  if (globals.frame > globals.maxFrame) {
    reset();
  }

  if (cache.relativeFrame >= cache.frames.length) {
    globals.chunk += 1;
    await loadChunk();
  }

  if (globals.world !== cache.world || globals.chunk !== cache.chunk) {
    await loadChunk();
  }

  updateSimulation(cache.frames[cache.relativeFrame]);

  cache.relativeFrame += globals.speed;
  globals.frame += globals.speed;




  Timer = setTimeout(step, FrameInterval);
}

async function loadChunk() {
  const rec = await fetchRecording(globals.world, globals.chunk);
  if (!rec || rec.error) {
    throw new Error(`Failed to load recording: ${rec && rec.error ? rec.error : 'Unknown error'}`);
  }
  globals.maxFrame = rec.TotalFrames;
  cache.world = globals.world;
  cache.chunk = globals.chunk;
  cache.relativeFrame = 0;
  cache.frames = Object.values(rec.Frames);
}

export async function reset() {
  const rec = await fetchRecording(globals.world, 0);
  globals.chunk = 0;
  globals.frame = 0;
  for (const Obj of objects.values()) {
    scene.remove(Obj);
  }
  objects.clear();
  globals.LockedID = null;
  cache.chunk = 0;
  cache.relativeFrame = 0;
  cache.frames = Object.values(rec.Frames);
}