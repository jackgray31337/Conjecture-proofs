"""Exact Presburger coverage certificate. Run with Python 3 and libisl.

All sets are integer sets. A projection existentially quantifies the witness
coordinates; subtraction is exact set difference, including congruences.
"""
import ctypes
import ctypes.util
import json
from pathlib import Path

pointer = ctypes.c_void_p
integer = ctypes.c_int
natural = ctypes.c_uint
string = ctypes.c_char_p
library_name = ctypes.util.find_library("isl")
if not library_name:
    raise RuntimeError("The shared library libisl is required.")
lib = ctypes.CDLL(library_name)


def bind(name, result_type, *argument_types):
    function = getattr(lib, "isl_" + name)
    function.argtypes = argument_types
    function.restype = result_type
    return function


def checked(value):
    if not value:
        raise RuntimeError("libisl returned a null pointer.")
    return value


context = checked(bind("ctx_alloc", pointer)())
read_set = bind("set_read_from_str", pointer, pointer, string)
subtract = bind("set_subtract", pointer, pointer, pointer)
coalesce = bind("set_coalesce", pointer, pointer)
project = bind("set_project_out", pointer, pointer, integer, natural, natural)
is_empty = bind("set_is_empty", integer, pointer)
free_set = bind("set_free", pointer, pointer)
sample = bind("set_sample_point", pointer, pointer)
coordinate = bind("point_get_coordinate_val", pointer, pointer, integer, integer)
free_point = bind("point_free", pointer, pointer)
free_val = bind("val_free", pointer, pointer)
show_value = bind("val_to_str", pointer, pointer)
free_string = ctypes.CDLL(None).free
free_string.argtypes = [pointer]
SET_DIMENSION = 3  # isl_dim_set in isl/space_type.h


def parse(formula, variables=()):
    names = ", ".join(("r", "a", "b", *variables))
    return checked(read_set(context, ("{ [" + names + "] : " + formula + " }").encode()))


def admissible(n, a, b):
    n, a, b = [f"({term})" for term in (n, a, b)]
    return " and ".join([
        f"0 <= {a} < {n}", f"0 <= {b} < {n}", f"{a} != {b}",
        f"({a} - {b} - floor({n}/2)) mod 2 = 0",
        f"-{n} <= 2*{a} - 2*{b} <= {n}",
        f"{n}-1 <= 2*{a} + 2*{b} <= 3*{n}-3",
    ])


def regions():
    pairs = [("a", "b"), ("r-1-b", "r-1-a"), ("b", "a"), ("r-1-a", "r-1-b")]
    for orientation, (u, v) in enumerate(pairs):
        yield ("A", orientation), ("c",), f"c > ({u}) and " + admissible("r-2c", u, v+"-c")
    yield ("B", 0), ("j",), "7j >= r and 5j < r and " + admissible("r-4j", "a-2j", "b-2j")
    for orientation, (u, v) in enumerate(pairs):
        yield ("C", orientation), ("c",), f"c >= ({u}) and c != 2*({u}) and " + admissible("r-2c-1", u, "r-1-c-("+v+")")

    # L, H, indicators of the two high endpoints, and the base endpoint condition.
    carriers = [
        ("(2h+1)", "(h)", 0, 0, "U+V=h and V<=h"),
        ("(2h)", "(h-1)", 0, 1, "V=U+h and U<h"),
        ("(2h+1)", "(h-1)", 1, 1, "U+V=3h and U>=h"),
    ]
    for move in ("D", "E"):
        for orientation, (u, v) in enumerate(pairs[:2]):
            for kind, (L, H, first_high, last_high, ends) in enumerate(carriers):
                offset = int(move == "D")
                variables = ("h", "m", "z", "U", "V", "x", "y")
                base = " and ".join([
                    "h >= 1", f"0 <= U < V < {L}", ends, "z >= 1",
                    f"({u})=U+z-{offset}+{first_high}m",
                    f"({v})=V+z-{offset}+{last_high}m",
                    f"r={L}+m+2z-{offset}", "2 <= m < r", admissible("m", "x", "y"),
                ])
                if move == "D":
                    yield (move, orientation, kind), variables, base + f" and x={L}-{H}-2 and z={H}+1+y"
                    continue
                base += (f" and x=j-{H}-1 and z=m+j-2i+{H}+1+y"
                         f" and (0<={H}+1+y<z or 0<={H}+1+y+j-i-{L}<z)")
                edges = [
                    ("max", f"i=0 and j={L}-1"),
                    ("unit", f"i={H} and j={H}+1"),
                    ("W", f"(U=0 and i+j={L} or V={L}-1 and i+j={L}-2)"),
                    ("diagonal", f"i+j={L}-1 and (U<i or {L}-1-V<i)"),
                ]
                for edge, condition in edges:
                    yield (move, orientation, kind, edge), variables+("i", "j"), base + f" and 0<=i<={H}<j<{L} and " + condition
    yield ("ray", 0), ("k",), "k>=2 and r=28k+22 and a=9k+7 and b=13k+10"


def read_seeds():
    paths = json.loads(Path(__file__).with_name("seeds.json").read_text())
    seeds = {}
    for path in paths:
        r = len(path)
        if sorted(path) != list(range(r)) or sorted(abs(i-j) for i,j in zip(path,path[1:])) != list(range(1,r)):
            raise ValueError(f"Invalid seed {path}")
        seeds[r,path[0],path[-1]] = tuple(path)
    return seeds


def witness(formula, variables, r, a, b):
    domain = parse(formula + f" and r={r} and a={a} and b={b}", variables)
    status = is_empty(domain)
    if status != 0:
        free_set(domain)
        if status != 1:
            raise RuntimeError("libisl emptiness check failed")
        return None
    point = checked(sample(domain))
    answer = {}
    for index, name in enumerate(variables, 3):
        val = checked(coordinate(point, SET_DIMENSION, index))
        text = checked(show_value(val))
        answer[name] = int(ctypes.string_at(text))
        free_string(text)
        free_val(val)
    free_point(point)
    return answer


def check():
    remaining = parse("r>=2 and a<b and a+b<r and "+admissible("r","a","b"))
    for _, variables, formula in regions():
        domain = parse(formula, variables)
        image = checked(project(domain, SET_DIMENSION, 3, len(variables)))
        remaining = checked(coalesce(checked(subtract(remaining, image))))
    seeds = read_seeds()
    seed_set = parse(" or ".join(f"(r={r} and a={a} and b={b})" for r,a,b in seeds))
    copy = bind("set_copy", pointer, pointer)
    excess = checked(subtract(checked(copy(seed_set)), checked(copy(remaining))))
    missing = checked(subtract(remaining, seed_set))
    if is_empty(missing) != 1 or is_empty(excess) != 1:
        raise RuntimeError("The residual set and seed keys differ.")
    print(f"Unbounded exact coverage verified. Residual equals the {len(seeds)} verified seed triples.")
    free_set(missing)
    free_set(excess)


if __name__ == "__main__":
    check()
