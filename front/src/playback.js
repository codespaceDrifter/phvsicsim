import { fetchRecording } from './api.js';
import { updateSimulation } from './update.js';
import { globals, cache } from './global.js';
import { scene } from './camera.js';

const FrameInterval = 1000 / 30;
let Timer = null;

export async function step() {

  if (globals.maxFrame == 0 || globals.frame >= globals.maxFrame) {
    await reset();
    return;
  }

  if (cache.relativeFrame >= cache.frames.length) {


    globals.chunk += 1;
    cache.relativeFrame = 0;
    await loadChunk();
    return;
  }

  if (globals.world !== cache.world ) {
    cache.world = globals.world;
    await reset();
    return;
  }

  updateSimulation(cache.frames[cache.relativeFrame]);

  cache.relativeFrame += globals.speed;
  globals.frame += globals.speed;



  Timer = setTimeout(step, FrameInterval);
}

async function loadChunk() {
  console.log("loading chunk");
  console.log("cached relative frame", cache.relativeFrame);
  console.log("global world", globals.world);
  console.log("global chunk", globals.chunk);

  const rec = await fetchRecording(globals.world, globals.chunk);
  if (!rec || rec.error) {
    throw new Error(`Failed to load recording: ${rec && rec.error ? rec.error : 'Unknown error'}`);
  }
  cache.frames = Object.values(rec.Frames);
  Timer = setTimeout(step, FrameInterval);
}

export async function reset() {
  const rec = await fetchRecording(globals.world, 0);
  globals.chunk = 0;
  globals.frame = 0;
  cache.relativeFrame = 0;
  cache.frames = Object.values(rec.Frames);
  globals.maxFrame = rec.TotalFrames;
  Timer = setTimeout(step, FrameInterval);
}