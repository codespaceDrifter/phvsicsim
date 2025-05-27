import { fetchRecording } from './api.js';
import { updateSimulation } from './update.js';
import { globals } from './global.js';

const FrameInterval = 1000 / 30;
let Frames = [];
let SceneRef = null;
let Timer = null;
let ChunkOffset = 0;
let TotalFrames = 0;

function sortFrames(map) {
  return Object.keys(map)
    .map((t) => ({ time: parseFloat(t), data: map[t] }))
    .sort((a, b) => a.time - b.time);
}

function step() {
  if (globals.frame >= Frames.length) {
    globals.chunk += 1;
    ChunkOffset += Frames.length;
    loadChunk(SceneRef);
    return;
  }

  const frame = Frames[Math.floor(globals.frame)];
  if (frame) {
    updateSimulation(frame.data, SceneRef, frame.time);
  }
  globals.frame += globals.speed;

  const absolute = ChunkOffset + globals.frame;
  if (TotalFrames && absolute >= TotalFrames) {
    globals.frame = 0;
    globals.chunk = 0;
    ChunkOffset = 0;
    loadChunk(SceneRef);
    return;
  }

  Timer = setTimeout(step, FrameInterval);
}

export function playRecording(scene, recording) {
  SceneRef = scene;
  Frames = sortFrames(recording.Frames);
  if (recording.TotalFrames) {
    TotalFrames = recording.TotalFrames;
  }
  globals.frame = 0;
  step();
}

export function loadChunk(scene) {
  SceneRef = scene;
  fetchRecording(globals.world, globals.chunk).then((rec) => {
    if (!rec) {
      globals.chunk = 0;
      globals.frame = 0;
      ChunkOffset = 0;
      fetchRecording(globals.world, globals.chunk).then((r) => {
        if (r) {
          playRecording(scene, r);
        }
      });
      return;
    }
    playRecording(scene, rec);
  });
}
