package common

import "math"

type Vector3 struct {
	X float32
	Y float32
	Z float32
}

func VecAddVec(V1 Vector3, V2 Vector3) Vector3 {
	return Vector3{X: V1.X + V2.X, Y: V1.Y + V2.Y, Z: V1.Z + V2.Z}
}

func VecSubVec(V1 Vector3, V2 Vector3) Vector3 {
	return Vector3{X: V1.X - V2.X, Y: V1.Y - V2.Y, Z: V1.Z - V2.Z}
}

func VecMulVec(V1 Vector3, V2 Vector3) Vector3 {
	return Vector3{X: V1.X * V2.X, Y: V1.Y * V2.Y, Z: V1.Z * V2.Z}
}

func VecDivVec(V1 Vector3, V2 Vector3) Vector3 {
	return Vector3{X: V1.X / V2.X, Y: V1.Y / V2.Y, Z: V1.Z / V2.Z}
}

func VecAddScalar(V Vector3, s float32) Vector3 {
	return Vector3{X: V.X + s, Y: V.Y + s, Z: V.Z + s}
}

func VecSubScalar(V Vector3, s float32) Vector3 {
	return Vector3{X: V.X - s, Y: V.Y - s, Z: V.Z - s}
}

func VecMulScalar(V Vector3, s float32) Vector3 {
	return Vector3{X: V.X * s, Y: V.Y * s, Z: V.Z * s}
}

func VecDivScalar(V Vector3, s float32) Vector3 {
	return Vector3{X: V.X / s, Y: V.Y / s, Z: V.Z / s}
}

func NegVec(V Vector3) Vector3 {
	return Vector3{X: -V.X, Y: -V.Y, Z: -V.Z}
}

func ClampSmall(V Vector3) Vector3 {
	if math.Abs(float64(V.X)) < 1e-6 {
		V.X = 0
	}
	if math.Abs(float64(V.Y)) < 1e-6 {
		V.Y = 0
	}
	if math.Abs(float64(V.Z)) < 1e-6 {
		V.Z = 0
	}
	return V
}

func VecDotVec(V1 Vector3, V2 Vector3) float32 {
	return V1.X*V2.X + V1.Y*V2.Y + V1.Z*V2.Z
}

func VecCrossVec(V1 Vector3, V2 Vector3) Vector3 {
	return Vector3{
		X: V1.Y*V2.Z - V1.Z*V2.Y,
		Y: V1.Z*V2.X - V1.X*V2.Z,
		Z: V1.X*V2.Y - V1.Y*V2.X,
	}
}

func SegmentIntersectsTriangle(p0, p1, v0, v1, v2 Vector3) bool {
	e1 := VecSubVec(v1, v0)
	e2 := VecSubVec(v2, v0)
	d := VecSubVec(p1, p0) // segment direction
	pvec := VecCrossVec(d, e2)
	det := VecDotVec(e1, pvec)

	// Cull degenerate triangle or back-facing
	if det > -1e-6 && det < 1e-6 {
		return false
	}
	invDet := 1.0 / det

	
	tvec := VecSubVec(p0, v0)
	u := VecDotVec(tvec, pvec) * invDet
	if u < 0 || u > 1 {
		return false
	}

	qvec := VecCrossVec(tvec, e1)
	v := VecDotVec(d, qvec) * invDet
	if v < 0 || u+v > 1 {
		return false
	}

	t := VecDotVec(e2, qvec) * invDet
	return t >= 0 && t <= 1 // t in [0,1] → within segment
}
