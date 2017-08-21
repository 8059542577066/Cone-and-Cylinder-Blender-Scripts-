import math
import bisect


def getCartesian(radius, theta, z):
    x = radius * math.cos(theta)
    y = radius * math.sin(theta)
    return (x, y, z)

def calculate(segments, radius, height):
    faces = []
    top = height / 2
    bottom = -top
    for i in xrange(segments - 1):
        theta_current = 2 * i * math.pi / segments
        theta_next = 2 * (i + 1) * math.pi / segments
        v1 = getCartesian(radius, theta_current, bottom)
        v2 = getCartesian(radius, theta_next, bottom)
        v3 = getCartesian(radius, theta_next, top)
        v4 = getCartesian(radius, theta_current, top)
        faces.append((v1, v2, v3, v4))
    theta_last = 2 * (segments - 1) * math.pi / segments
    v1 = getCartesian(radius, theta_last, bottom)
    v2 = getCartesian(radius, 0, bottom)
    v3 = getCartesian(radius, 0, top)
    v4 = getCartesian(radius, theta_last, top)
    faces.append((v1, v2, v3, v4))
    top_face = []
    bottom_face = []
    for i in xrange(segments):
        theta = 2 * i * math.pi / segments
        top_face.append(getCartesian(radius, theta, top))
        bottom_face.append(getCartesian(radius, theta, bottom))
    faces.append(tuple(top_face))
    faces.append(tuple(reversed(bottom_face)))
    return faces

def getVertices(faces):
    vertices = []
    for face in faces:
        for vertex in face:
            vertices.append(vertex)
    return sorted(set(vertices))

def matchVerticesToFaces(vertices, faces):
    new_faces = []
    for face in faces:
        new_face = []
        for vertex in face:
            new_vertex = bisect.bisect(vertices, vertex) - 1
            new_face.append(new_vertex)
        new_faces.append(tuple(new_face))
    return new_faces

def save(vertices, faces):
    with open("Cylinder.txt", "w") as f:
        f.write("import bpy\n\n\n")
        f.write("vertices = []\n\n")
        for vertex in vertices:
            f.write("vertices.append(" + str(vertex) + ")\n")
        f.write("\n\nfaces = []\n\n")
        for face in faces:
            f.write("faces.append(" + str(face) + ")\n")
        f.write("\n\nmesh = bpy.data.meshes.new(\"cylinder\")\n")
        f.write("object = bpy.data.objects.new(\"cylinder\", mesh)\n\n")
        f.write("object.location = bpy.context.scene.cursor_location\n")
        f.write("bpy.context.scene.objects.link(object)\n\n")
        f.write("mesh.from_pydata(vertices, [], faces)\n")
        f.write("mesh.update(calc_edges = True)")


def main():
    segments = int(raw_input("Number of Segments: "))
    radius = float(raw_input("Radius of Cylinder: "))
    height = float(raw_input("Height of Cylinder: "))
    faces = calculate(segments, radius, height)
    vertices = getVertices(faces)
    print "\nNumber of Vertices: " + str(len(vertices))
    faces = matchVerticesToFaces(vertices, faces)
    print "Number of Faces: " + str(len(faces)) + "\n"
    save(vertices, faces)
    raw_input("Finished.")


if __name__ == "__main__":
    main()
