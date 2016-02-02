import re
from urllib.request import urlopen

def replaced(text):
	TEXT = text.replace("&gt;", ">").replace("&lt;", "<").replace("&#8217;", "'")
	return TEXT

def change(text):
	head = text.split("(")[0]
	body = text.split("(")[1:]
	body = "".join(body).split(")")[0]

	body = body.split(",")

	result = ""
	for x in body:
		ind = body.index(x) + 1

		if body.index(x) != len(body) - 1:
			x = "${%s:%s}, " % (ind, replaced(x.strip()))
		else:
			x = "${%s:%s}" % (ind, replaced(x.strip()))

		result += x
	result = head + "(" + result + ")"
	return (result)


def make(link):
	alls = []
	text = urlopen(link).read().decode("utf-8")
	A = re.findall(r'<div class="line"><span class="signature">(.*?) -&gt; .*?</div>', text)
	A = sorted(set(A))

	for x in A:
		if x.endswith(")"):
			x = change(x)

		alls.append(x)

	return alls

ln1 = "{\n\t\"scope\": \"source.python\",\n\t\"completions\":\n\t[\n"
ln2 = "\t\t{\"trigger\": \"%s\\tpygame(%s) \", \"contents\": \"pygame.%s.%s\"},\n"
ln3 = "\t]\n}"


url = "http://www.pygame.org/docs/ref/%s.html"
head = ["BufferProxy", "cdrom", "Color", "cursors", "display", "draw", "event", "examples", "font", "freetype", "gfxdraw", "image", "joystick", "key", "locals", "mixer", "music", "mouse", "Overlay", "PixelArray", "Rect", "scrap", "sndarray", "sprite", "Surface", "surfarray", "tests", "time", "transform"]

links = []
for x in head:
	y = url % x.strip().lower()
	print(y)
	with open("%s.sublime-completions" % x, "w") as obj:
		obj.write(ln1)
		for z in make(y):
			obj.write(ln2 % (z.split("(")[0], x, x, z))
		obj.write(ln3)


