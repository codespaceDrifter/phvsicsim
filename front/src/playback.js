/**
 * Playback controller module.
 * Manages frame-by-frame playback of recorded simulations.
 */
import { fetchRecording } from './api.js';
import { updateSimulation } from './objects.js';
import { playback, cache, FRAME_INTERVAL_MS } from './state.js';

/**
 * Main playback step function.
 * Called repeatedly via setTimeout to advance frames.
 */
export async function step() {
  // If we've reached the end, reset
  if (playback.maxFrame === 0 || playback.frame >= playback.maxFrame) {
    await reset();
    return;
  }

  // If we've exhausted the current chunk, load the next one
  if (cache.relativeFrame >= cache.frames.length) {
    playback.chunk += 1;
    cache.relativeFrame = 0;
    await loadChunk();
    return;
  }

  // If world changed, reset playback
  if (playback.world !== cache.world) {
    cache.world = playback.world;
    await reset();
    return;
  }

  // Render current frame
  updateSimulation(cache.frames[cache.relativeFrame]);

  // Advance frame counters
  cache.relativeFrame += playback.speed;
  playback.frame += playback.speed;

  // Schedule next step
  playback.timer = setTimeout(step, FRAME_INTERVAL_MS);
}

/**
 * Load the next chunk of recording data.
 */
async function loadChunk() {
  if (playback.timer) {
    clearTimeout(playback.timer);
  }

  const recording = await fetchRecording(playback.world, playback.chunk);
  if (!recording) {
    console.error(`Failed to load chunk ${playback.chunk} for world ${playback.world}`);
    return;
  }

  cache.frames = Object.values(recording.frames);
  playback.timer = setTimeout(step, FRAME_INTERVAL_MS);
}

/**
 * Reset playback to the beginning.
 */
export async function reset() {
  if (playback.timer) {
    clearTimeout(playback.timer);
  }

  const recording = await fetchRecording(playback.world, 0);
  if (!recording) {
    console.error(`Failed to load initial recording for world ${playback.world}`);
    return;
  }

  playback.chunk = 0;
  playback.frame = 0;
  cache.relativeFrame = 0;
  cache.frames = Object.values(recording.frames);
  playback.maxFrame = recording.totalFrames;

  playback.timer = setTimeout(step, FRAME_INTERVAL_MS);
}
