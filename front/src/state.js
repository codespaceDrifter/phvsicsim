/**
 * Centralized application state management.
 * All state is managed here with clear separation of concerns.
 */

// Playback state - controls simulation playback
export const playback = {
  world: 'threeBody',
  frame: 0,
  chunk: 0,
  speed: 1,
  maxFrame: 0,
  timer: null,
};

// Cache state - stores loaded recording data
export const cache = {
  frames: [],
  world: null,
  relativeFrame: 0,
};

// Available worlds (recording names)
export const availableWorlds = ['threeBody', 'billardBall'];

// Frame timing
export const FRAME_INTERVAL_MS = 1000 / 30;
