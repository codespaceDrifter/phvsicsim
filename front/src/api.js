export async function fetchRecording(name, chunk) {
  const response = await fetch(
    `http://localhost:8080/recordings/${name}/${chunk}`,
  );
  if (!response.ok) {
    return null;
  }
  const buffer = await response.arrayBuffer();
  return decodeRecording(buffer);
}

function decodeRecording(buffer) {
  const dv = new DataView(buffer);
  let offset = 0;
  offset += 4; // Skip magic
  const secondsPerFrame = dv.getFloat32(offset, true); offset += 4;
  const totalFrames = dv.getUint32(offset, true); offset += 4;
  const frameCount = dv.getUint32(offset, true); offset += 4;
  const frames = {};
  for (let i = 0; i < frameCount; i++) {
    const time = dv.getFloat32(offset, true); offset += 4;
    const objCount = dv.getUint32(offset, true); offset += 4;
    const IDArray = [];
    const PositionArrays = [];
    const VertexArrays = [];
    const IndexArrays = [];
    const ColorArray = [];
    for (let j = 0; j < objCount; j++) {
      let len = dv.getUint32(offset, true); offset += 4;
      const id = new TextDecoder().decode(new Uint8Array(buffer, offset, len));
      offset += len;
      IDArray.push(id);
      const pos = [
        dv.getFloat32(offset, true),
        dv.getFloat32(offset + 4, true),
        dv.getFloat32(offset + 8, true),
      ];
      offset += 12;
      PositionArrays.push(pos);
      len = dv.getUint32(offset, true); offset += 4;
      const verts = new Float32Array(buffer.slice(offset, offset + len * 4));
      offset += len * 4;
      VertexArrays.push(Array.from(verts));
      len = dv.getUint32(offset, true); offset += 4;
      const inds = new Uint32Array(buffer.slice(offset, offset + len * 4));
      offset += len * 4;
      IndexArrays.push(Array.from(inds));
      len = dv.getUint32(offset, true); offset += 4;
      const color = new TextDecoder().decode(new Uint8Array(buffer, offset, len));
      offset += len;
      ColorArray.push(color);
    }
    frames[time.toFixed(3)] = {
      CurTime: time,
      IDArray,
      PositionArrays,
      VertexArrays,
      IndexArrays,
      ColorArray,
    };
  }
  return { SecondsPerFrame: secondsPerFrame, TotalFrames: totalFrames, Frames: frames };
}