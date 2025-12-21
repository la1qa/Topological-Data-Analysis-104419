from typing import Protocol, runtime_checkable

from drawsvg import Circle, Context, Drawing, Line, Lines, Text


@runtime_checkable
class SimplexProtocol(Protocol):
    points: list[tuple[float, ...]]
    dim: int
    name: str


@runtime_checkable
class SimplicialComplexProtocol(Protocol):
    simplexs: list[SimplexProtocol]
    dim: int


def get_centroid(points: list[tuple[float, ...]]) -> tuple[float, ...]:
    points_T = zip(*points)
    return tuple(sum(ax) / len(points) for ax in points_T)


def create_canvas(points: list[tuple[float, float]], margin=100) -> Drawing:
    xs, ys = zip(*points)
    return Drawing(
        2 * max(abs(x) for x in xs) + margin,
        2 * max(abs(y) for y in ys) + margin,
        origin="center",
        context=Context(invert_y=True),
    )


def draw_simplex(simplex, vsize=10, vopacity=1):
    if simplex.dim == 0:
        ((x1, y1),) = simplex.points
        d = Circle(x1, y1, vsize, fill="gray", fill_opacity=vopacity)
    elif simplex.dim == 1:
        (x1, y1), (x2, y2) = simplex.points
        d = Line(x1, y1, x2, y2, stroke="black")
    elif simplex.dim == 2:
        (x1, y1), (x2, y2), (x3, y3) = simplex.points
        d = Lines(x1, y1, x2, y2, x3, y3, fill="gray", fill_opacity=0.4)
    else:
        raise RuntimeError("Cannot draw this, buddy.")
    xc, yc = get_centroid(simplex.points)
    label = Text(simplex.name, 12, xc, yc, center=True)
    return d, label


def draw(*objs, margin=100, axis=False, vsize=10, vopacity=1):
    _points = []
    _svg_objs = []
    for obj in objs:
        if isinstance(obj, SimplexProtocol):
            _points.extend(obj.points)
            d, label = draw_simplex(obj, vsize=vsize, vopacity=vopacity)
            _svg_objs.extend([d, label])
        elif isinstance(obj, SimplicialComplexProtocol):
            for s in sorted(obj.simplexs, key=lambda x: -x.dim):
                _points.extend(s.points)
                d, label = draw_simplex(s, vsize=vsize, vopacity=vopacity)
                _svg_objs.extend([d, label])
        else:
            raise NotImplementedError()
    canvas = create_canvas(_points, margin=margin)
    if axis:
        x0, y0, x1, y1 = canvas.view_box
        x_axis = Line(x0, 0, x1, 0, stroke="gray", stroke_dasharray="5,5")
        y_axis = Line(0, y0, 0, y1, stroke="gray", stroke_dasharray="5,5")
        _svg_objs = [x_axis, y_axis] + _svg_objs
    for el in _svg_objs:
        canvas.append(el)
    return canvas
