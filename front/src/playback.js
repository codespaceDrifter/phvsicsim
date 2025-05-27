import { fetchRecording } from './api.js';
import { updateSimulation } from './update.js';
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


  console.log(cache.relativeFrame);
  console.log(cache.frames[cache.relativeFrame]);

  Timer = setTimeout(step, FrameInterval);
}

async function loadChunk() {
  const rec = await fetchRecording(globals.world, globals.chunk);
  globals.maxFrame = rec.TotalFrames;
  cache.world = globals.world;
  cache.chunk = globals.chunk;
  cache.relativeFrame = 0;
  cache.frames = Object.values(rec.Frames);
}

export async function reset() {
  const rec = await fetchRecording(globals.world, 0);
  cache.world = globals.world;
  globals.chunk = 0;
  globals.frame = 0;
  cache.chunk = 0;
  cache.relativeFrame = 0;
  cache.frames = Object.values(rec.Frames);
}