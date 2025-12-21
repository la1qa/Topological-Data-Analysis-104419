import numpy as np
from drawing_utils import draw


class Simplex:
    def __init__(self, points, name=""):
        self.points = tuple(sorted(points))
        self.dim = len(points) - 1
        self.name = name

    def faces(self):
        if self.dim == 0:
            return
        for i in range(self.dim + 1):
            yield Simplex(self.points[:i] + self.points[i + 1 :])

    def __eq__(self, other):
        return self.points == other.points

    def __hash__(self):
        return hash(self.points)

    def __repr__(self):
        return self.name or str(list(self.points))


class SimplicialComplex:
    def __init__(self, *simplexs, dim=None):
        self.simplexs = simplexs
        self.dim = dim or max(s.dim for s in simplexs)
        self.basis = {
            dim: [s for s in simplexs if s.dim == dim] for dim in range(self.dim + 1)
        }

    @classmethod
    def instantiate_maximally(cls, *simplexs, dim=None):
        all_simplexes = set()
        for simplex in simplexs:
            all_simplexes.add(simplex)
            if simplex.dim > 0:
                all_simplexes |= set(
                    cls.instantiate_maximally(*simplex.faces()).simplexs
                )
        return cls(*all_simplexes, dim=dim)

    def diff_matrix(self, dim, field=None):
        _matrix = np.zeros(
            (len(self.basis[dim - 1]) if dim > 0 else 1, len(self.basis[dim])),
            dtype=int,
        )
        for i, simplex in enumerate(self.basis[dim]):
            for j, face in enumerate(simplex.faces()):
                _matrix[self.basis[dim - 1].index(face), i] = (-1) ** j
        if field:
            return field(_matrix % field.characteristic)
        return _matrix

    def betti_numbers(self, field=None):
        _diff_image_dims = []
        _diff_kernel_dims = []
        for i in range(self.dim + 1):
            diff_matrix = self.diff_matrix(i, field)
            rank = np.linalg.matrix_rank(diff_matrix) if diff_matrix.size else 0
            domain_dim = len(self.basis[i])
            _diff_image_dims.append(int(rank))
            _diff_kernel_dims.append(int(domain_dim - rank))
        return [_diff_kernel_dims[i] - _diff_image_dims[i + 1] for i in range(self.dim)]

    def draw(self, **kwargs):
        return draw(self, **kwargs)

    def euler_characteristic(self):
        x = 0
        for s in self.simplexs:
            x += (-1) ** s.dim
        return x

    def _repr_html_(self):
        try:
            return self.draw().as_svg()
        except RuntimeError:
            return self.__repr__()
