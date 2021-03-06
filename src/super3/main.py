import ast
import os

import astor
import attr


@attr.s
class Violation:
    col_offset = attr.ib()
    end_col_offset = attr.ib()
    lineno = attr.ib()
    end_lineno = attr.ib()


@attr.s
class SourceFile:
    path = attr.ib()
    source = attr.ib()
    tree = attr.ib()


def find_parent(node, type):
    parent = getattr(node, "parent", None)
    while parent:
        node = parent
        if isinstance(node, type):
            return node
        parent = getattr(node, "parent", None)


def _iter_violations(root):

    for node in ast.walk(root):

        # Patch in parents for reference later.
        for child in ast.iter_child_nodes(node):
            child.parent = node

        # We only care about function calls
        if not isinstance(node, ast.Call):
            continue

        # We only care about calls to functions of type "Name". Otherwise they
        # are probably Attributes, super isn't a attribute
        if not isinstance(node.func, ast.Name) or node.func.id != "super":
            continue

        # We only care about function calls that have args. Since we want to
        # remove them!
        if not node.args:
            continue

        fn_def = find_parent(node, ast.FunctionDef)
        class_def = find_parent(node, ast.ClassDef)
        # Method isn't in a class. this is likely due to some metaprogramming
        # or something too advanced for us to detect.
        if not fn_def or not class_def:
            continue

        if len(node.args) != 2:
            continue

        if not isinstance(node.args[0], ast.Name):
            # Super is likely being passed something like object.Class. This is
            # generally a more complex case than we want to handle
            continue

        if node.args[0].id != class_def.name:
            # using super with a explicit name that isn't the current class, it
            # can't be removed.
            continue

        if node.args[1].id not in ("self", "cls"):
            # Only handle super calls with the conventional variable names
            continue

        # yo dawg, I heard you like args...
        if not fn_def.args.args or fn_def.args.args[0].arg not in ("self", "cls"):
            # we might be in a staticmethod or another method without the self
            # or cls. We might miss some cases here, but lets be safe and
            # ignore these for now.
            continue

        yield node


def _parse(source):
    # TODO: Handle syntax errors here. We will get that with Python 2 or other
    # invalid code.
    return ast.parse(source)


def _is_python(path):
    # TODO: We might want to support other files here? i.e. shebang?
    return path.endswith(".py")


def walk_files(path):

    if os.path.isfile(path):
        yield path
    elif not os.path.isdir(path):
        raise StopIteration

    for root, dirs, filenames in os.walk(path):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))

        for filename in sorted(filenames):
            if _is_python(filename):
                yield os.path.join(root, filename)


def load_file(file):
    with open(file) as f:
        source = f.read()
        tree = _parse(source)
        return SourceFile(path=file, source=source, tree=tree)


def read_files(path):
    for file in walk_files(path):
        try:
            yield load_file(file)
        except SyntaxError:
            print(f"Failed to parse {file}")


def upgrade_string(lines: list, violation: Violation):
    lineno = violation.lineno - 1

    # This is nasty. Need to find a better way to do this.
    lines[lineno] = (
        lines[lineno][: violation.col_offset]
        + "super()"
        + lines[lineno][violation.end_col_offset :]
    )


def upgrade_file(source_file: SourceFile):
    lines = source_file.source.splitlines()

    violation = None
    for violation in list_violations(source_file):
        upgrade_string(lines, violation)

    if not violation:
        return

    with open(source_file.path, "w") as f:
        # TODO; We need to handle different newline characters
        f.write("\n".join(lines))


def list_violations(source_file: SourceFile):
    for node in _iter_violations(source_file.tree):
        yield Violation(
            lineno=node.lineno,
            end_lineno=node.end_lineno,
            col_offset=node.col_offset,
            end_col_offset=node.end_col_offset,
        )


def has_violation(source_file):
    for node in _iter_violations(source_file.tree):
        return True
    return False
