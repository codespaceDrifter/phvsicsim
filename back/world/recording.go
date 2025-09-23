package world

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"os"
	"sort"
	"strconv"
)

type Recording struct {
	Name            string
	World           *World
	SecondsPerFrame float32
	EndSeconds      int
}

type RecordingFile struct {
	SecondsPerFrame float32
	TotalFrames     uint32
	Frames          map[string]Frame
}

func NewRecording(name string, world *World, secondsPerFrame float32, endSeconds int) *Recording {
	return &Recording{Name: name, World: world, SecondsPerFrame: secondsPerFrame, EndSeconds: endSeconds}
}

func (r *Recording) Simulate() {
	fmt.Println("Simulating recording...")

	frames := make(map[string]Frame)
	frameInterval := r.SecondsPerFrame
	totalFrames := int(float32(r.EndSeconds)/r.SecondsPerFrame) + 1

	fmt.Println("Total frames:", totalFrames)

	chunkIndex := 0
	exePath, _ := os.Getwd()
	logDir := fmt.Sprintf("%s/logs/%s", exePath, r.Name)
	os.MkdirAll(logDir, 0755)
	//clear before starting
	//os.RemoveAll(logDir)

	for i := 0; i < totalFrames; i++ {
		fmt.Println("Frame:", i)

		target := float32(i) * frameInterval
		for r.World.CurTime < target {
			r.World.Update()
		}
		frame := r.World.Flatten()
		frames[fmt.Sprintf("%.3f", target)] = frame

		if len(frames) == 1000 || i == totalFrames-1 {
			fileStruct := RecordingFile{
				SecondsPerFrame: r.SecondsPerFrame,
				TotalFrames:     uint32(totalFrames),
				Frames:          frames,
			}

			logPath := fmt.Sprintf("%s/%d.bin", logDir, chunkIndex)
			file, _ := os.Create(logPath)
			data := EncodeRecordingBinary(fileStruct)
			file.Write(data)
			file.Close()

			frames = make(map[string]Frame)
			chunkIndex++
		}
	}
}

func EncodeRecordingBinary(r RecordingFile) []byte {
	buf := &bytes.Buffer{}

	buf.Write([]byte{'S', 'I', 'M', 'B'})
	binary.Write(buf, binary.LittleEndian, r.SecondsPerFrame)
	binary.Write(buf, binary.LittleEndian, r.TotalFrames)

	keys := make([]float64, 0, len(r.Frames))
	for k := range r.Frames {
		f, _ := strconv.ParseFloat(k, 32)
		keys = append(keys, f)
	}
	sort.Float64s(keys)

	binary.Write(buf, binary.LittleEndian, uint32(len(keys)))
	for _, key := range keys {
		t := float32(key)
		binary.Write(buf, binary.LittleEndian, t)

		frame := r.Frames[fmt.Sprintf("%.3f", t)]
		count := uint32(len(frame.IDArray))
		binary.Write(buf, binary.LittleEndian, count)

		for i := 0; i < int(count); i++ {
			id := frame.IDArray[i]
			binary.Write(buf, binary.LittleEndian, uint32(len(id)))
			buf.WriteString(id)

			pos := frame.PositionArrays[i]
			for j := 0; j < 3; j++ {
				binary.Write(buf, binary.LittleEndian, pos[j])
			}

			verts := frame.VertexArrays[i]
			binary.Write(buf, binary.LittleEndian, uint32(len(verts)))
			for _, v := range verts {
				binary.Write(buf, binary.LittleEndian, v)
			}

			inds := frame.IndexArrays[i]
			binary.Write(buf, binary.LittleEndian, uint32(len(inds)))
			for _, ind := range inds {
				binary.Write(buf, binary.LittleEndian, ind)
			}

			color := frame.ColorArray[i]
			binary.Write(buf, binary.LittleEndian, uint32(len(color)))
			buf.WriteString(color)
		}
	}

	return buf.Bytes()
}

func DecodeRecordingBinary(data []byte) RecordingFile {
	buf := bytes.NewReader(data)
	magic := make([]byte, 4)
	buf.Read(magic)

	var spf float32
	binary.Read(buf, binary.LittleEndian, &spf)

	var total uint32
	binary.Read(buf, binary.LittleEndian, &total)

	var frameCount uint32
	binary.Read(buf, binary.LittleEndian, &frameCount)

	frames := make(map[string]Frame)
	for i := 0; i < int(frameCount); i++ {
		var t float32
		binary.Read(buf, binary.LittleEndian, &t)
		var objCount uint32
		binary.Read(buf, binary.LittleEndian, &objCount)

		idArray := make([]string, objCount)
		posArray := make([][]float32, objCount)
		vertArray := make([][]float32, objCount)
		indArray := make([][]uint32, objCount)
		colorArray := make([]string, objCount)

		for j := 0; j < int(objCount); j++ {
			var l uint32
			binary.Read(buf, binary.LittleEndian, &l)
			idBytes := make([]byte, l)
			buf.Read(idBytes)
			idArray[j] = string(idBytes)

			p := make([]float32, 3)
			for k := 0; k < 3; k++ {
				binary.Read(buf, binary.LittleEndian, &p[k])
			}
			posArray[j] = p

			binary.Read(buf, binary.LittleEndian, &l)
			verts := make([]float32, l)
			for k := 0; k < int(l); k++ {
				binary.Read(buf, binary.LittleEndian, &verts[k])
			}
			vertArray[j] = verts

			binary.Read(buf, binary.LittleEndian, &l)
			inds := make([]uint32, l)
			for k := 0; k < int(l); k++ {
				binary.Read(buf, binary.LittleEndian, &inds[k])
			}
			indArray[j] = inds

			binary.Read(buf, binary.LittleEndian, &l)
			colorBytes := make([]byte, l)
			buf.Read(colorBytes)
			colorArray[j] = string(colorBytes)
		}

		frames[fmt.Sprintf("%.3f", t)] = Frame{
			CurTime:        t,
			IDArray:        idArray,
			PositionArrays: posArray,
			VertexArrays:   vertArray,
			IndexArrays:    indArray,
			ColorArray:     colorArray,
		}
	}

	return RecordingFile{SecondsPerFrame: spf, TotalFrames: total, Frames: frames}
}
