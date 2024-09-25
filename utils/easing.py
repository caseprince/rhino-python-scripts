import math

# time, beginning, change, duration

def easeInOutCirc(t, b, c, d):
	t /= d/2
	if t < 1:
		return -c/2 * (math.sqrt(1 - t*t) - 1) + b
	t -= 2
	return c/2 * (math.sqrt(1 - t*t) + 1) + b

def easeInOutQuad(t, b, c, d):
	t /= d/2
	if t < 1:
		return c/2*t*t + b
	t-=1
	return -c/2 * (t*(t-2) - 1) + b

def easeInSine(t, b, c, d):
	return -c * math.cos(t/d * (math.pi/2)) + c + b

def easeOutSine(t, b, c, d):
	return c * math.sin(t/d * (math.pi/2)) + b

def easeInOutSine(t, b, c, d):
	return -c/2 * (math.cos(math.pi*t/d) - 1) + b