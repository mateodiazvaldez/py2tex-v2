import ast
import contextlib


class CodeGen:
    def __init__(self):
        self._indentation = 0
        self._lines = []

    def line(self, line):
        self._lines.append((line, self._indentation))

    def _indented_lines(self):
        for line, indentation in self._lines:
            yield "  " * indentation + line + "\n"

    def to_string(self):
        return "".join(self._indented_lines())

    @contextlib.contextmanager
    def indent(self):
        self._indentation += 1
        yield
        self._indentation -= 1


class Py2Tex(ast.NodeVisitor, CodeGen):
    def __init__(self):
        super().__init__()
        self._emit_tex = True

    def visit(self, node):
        if node is None:
            return ""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        result = visitor(node)
        if result is None:
            return ""
        return result

    def visit_all(self, nodes):
        for node in nodes:
            self.visit(node)

    def visit_Module(self, node):
        for stmt in node.body:
            self.visit(stmt)

    def body(self, body):
        with self.indent():
            self.visit_all(body)

    def arg(self, a):
        if a.annotation is None:
            return r"\PyArg{" + a.arg + "}"
        else:
            if isinstance(a.annotation, ast.Str):
                annotation_tex = a.annotation.s
            else:
                annotation_tex = self.visit(a.annotation)
            return r"\PyArgAnnotation{" + a.arg + "}{" + annotation_tex + "}"

    def expr(self, e):
        return r"\PyExpr{" + self.visit(e) + "}"

    def visit_FunctionDef(self, node):
        if not self._emit_tex:
            return
        
        safe_name = node.name.replace('_', r'\_')
        args = r"\PyArgSep".join(self.arg(a) for a in node.args.args)
        
        if node.returns:
            if isinstance(node.returns, ast.Str):
                returns_tex = node.returns.s
            else:
                returns_tex = self.visit(node.returns)
            self.line(r"\Function{" + safe_name + "}{" + args +
                      r"}{ $\rightarrow$ \texttt{" + returns_tex + "}}")
            self.body(node.body)
            self.line(r"\EndFunction%")
        else:
            self.line(r"\Procedure{" + safe_name + "}{" + args + "}")
            self.body(node.body)
            self.line(r"\EndProcedure%")

    def visit_Assign(self, node):
        if not self._emit_tex:
            return
        targets = r" \PyAssignSep ".join(
            self.visit(target) for target in node.targets)
        assign = r"\PyAssign{" + targets + "}{" + self.expr(node.value) + "}"
        self.line(r"\State{" + assign + "}")

    def visit_AnnAssign(self, node):
        if not self._emit_tex:
            return
        target = self.visit(node.target)
        if isinstance(node.annotation, ast.Str):
            annotation_tex = node.annotation.s
        else:
            annotation_tex = self.visit(node.annotation)
        
        if node.value:
            assign = r"\PyAssign{" + target + "}{" + self.expr(node.value) + "}"
            self.line(r"\State{" + assign + "}")
        else:
            assign = r"\PyAnnotation{" + target + "}{" + annotation_tex + "}"
            self.line(r"\State{" + assign + "}")

    def visit_Expr(self, node):
        # Maneja docstrings y !tex, !hide, !show
        if isinstance(node.value, ast.Str):
            self.handle_magic_string(node.value.s)
            return
        # Maneja llamadas a funciones que no se asignan (ej. print())
        if not self._emit_tex:
            return
        self.line(r"\State{" + self.expr(node.value) + "}")

    def handle_magic_string(self, s: str):
        # ¡IMPORTANTE! Se modificó para ignorar comentarios/docstrings
        if s.startswith("!tex\n"):
            for l in s.splitlines()[1:]:
                self.line(l)
        elif s == "!show":
            self._emit_tex = True
        elif s == "!hide":
            self._emit_tex = False
        else:
            # Antes aquí se imprimía \Comment{}, ahora no hace nada.
            pass

    # --- Nodos de Constantes (Python 3.8+) ---
    def visit_Constant(self, node):
        if isinstance(node.value, str):
            return r"\PyStr{" + node.value + "}"
        if node.value is True:
            return r"\PyTrue"
        if node.value is False:
            return r"\PyFalse"
        if node.value is None:
            return r"\PyNone"
        return r"\PyNum{" + str(node.value) + "}"

    # --- Nodos antiguos (Pre-Python 3.8) ---
    def visit_Str(self, node):
        return r"\PyStr{" + node.s + "}"

    def visit_Name(self, node):
        safe_id = node.id.replace('_', r'\_')
        return r"\PyName{" + safe_id + "}"

    def visit_Num(self, node):
        return r"\PyNum{" + str(node.n) + "}"

    def visit_NameConstant(self, node):
        return r"\Py" + str(node.value)

    def visit_BoolOp(self, node):
        return (r" \Py" + type(node.op).__name__ + " ").join(self.visit(v) for v in node.values)

    # --- visit_Call (Actualizado para métodos, lambda, *args) ---
    def visit_Call(self, node):
        # 1. Obtener la función (puede ser un nombre o un atributo)
        if isinstance(node.func, ast.Name):
            func_tex = self.visit(node.func)
            func_for_macro = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_tex = self.visit(node.func) # Llama a visit_Attribute
            func_for_macro = func_tex # No es 'print', así que no importa
        else:
            func_tex = self.visit(node.func)
            func_for_macro = func_tex

        # 2. Obtener argumentos (posicionales, *starred, keywords)
        all_args = []
        for a in node.args:
            all_args.append(self.visit(a)) # visit_Starred se encargará de *args
        
        for k in node.keywords:
            key = k.arg.replace('_', r'\_')
            val = self.visit(k.value)
            all_args.append(key + r" = " + val)
        
        all_args_tex = r" \PyCallSep ".join(all_args)

        # 3. Casos especiales
        if isinstance(node.func, ast.Name) and node.func.id == '_':
            return r"\PyPar{" + all_args_tex + "}"
        
        # 4. Usar macro \PyCall para 'print'
        if isinstance(node.func, ast.Name):
            return r"\PyCall{" + func_for_macro + "}{" + all_args_tex + "}"

        # Es una llamada a método, ej: puntos.sort(...)
        return func_tex + "(" + all_args_tex + ")"

    def visit_For(self, node):
        if not self._emit_tex:
            return

        if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and node.iter.func.id == 'range':
            # Manejo de 'range'
            nargs = len(node.iter.args)
            args = map(self.visit, node.iter.args)
            if nargs == 1:
                start = 0; [stop] = args; step = 1
            if nargs == 2:
                [start, stop] = args; step = 1
            if nargs == 3:
                [start, stop, step] = args
            
            variable = self.visit(node.target)
            self.line(
                r"\PyFor" + "".join("{" + str(x) + "}" for x in [variable, start, stop, step]))
            self.body(node.body)
            self.line(r"\EndPyFor")
        else:
            # Manejo genérico de 'for x in y'
            var_tex = self.visit(node.target)
            iter_tex = self.visit(node.iter)
            self.line(r"\ForEach{" + var_tex + r" \in " + iter_tex + "}")
            self.body(node.body)
            self.line(r"\EndForEach")

    def visit_BinOp(self, node):
        op_name = type(node.op).__name__
        if op_name == "FloorDiv":
             op_tex = r" \PyFloorDiv "
        else:
             op_tex = r" \Py" + op_name + " "
        return self.visit(node.left) + op_tex + self.visit(node.right)

    def visit_UnaryOp(self, node):
        return r"\Py" + type(node.op).__name__ + "{" + self.visit(node.operand) + "}"

    # --- visit_Subscript (Actualizado para Slicing) ---
    def visit_Subscript(self, node):
        val_tex = self.visit(node.value)
        slice_tex = self.visit(node.slice)
        return r"\PySubscript{" + val_tex + "}{" + slice_tex + "}"

    def visit_Index(self, node):
        return self.visit(node.value)

    def visit_Slice(self, node):
        lower = self.visit(node.lower) if node.lower else ""
        upper = self.visit(node.upper) if node.upper else ""
        step = self.visit(node.step) if node.step else ""
        
        if step:
            return lower + ":" + upper + ":" + step
        if upper or lower:
            return lower + ":" + upper
        return ":" # Para [:]

    # --- Nuevos Nodos ---
    def visit_Attribute(self, node):
        val_tex = self.visit(node.value)
        attr_tex = node.attr.replace('_', r'\_')
        return val_tex + "." + attr_tex

    def visit_Lambda(self, node):
        args = [a.arg for a in node.args.args]
        args_tex = ", ".join(args)
        body_tex = self.visit(node.body)
        return r"\PyLambda{" + args_tex + r"}{" + body_tex + "}"

    def visit_Starred(self, node):
        return r"*" + self.visit(node.value)

    def visit_Tuple(self, node):
        elts = r" \PyCallSep ".join(self.visit(el) for el in node.elts)
        return r"(" + elts + r")"
    
    # --- Match/Case (No Soportado) ---
    def visit_Match(self, node):
        self.line(r"\State \ERROR{La sintaxis 'match/case' no es soportada.}")
        self.line(r"\State \ERROR{Por favor, reemplace con 'if/elif/else'.}")
    
    # --- Fin Nuevos Nodos ---

    def visit_Compare(self, node):
        result = self.visit(node.left)
        for op, right in zip(node.ops, node.comparators):
            result += r" \Py" + type(op).__name__ + " " + self.visit(right)
        return result

    def visit_If(self, node):
        if not self._emit_tex:
            return
        self.line(r"\If{" + self.expr(node.test) + "}")
        self.body(node.body)
        if node.orelse:
            self.line(r"\Else%")
            self.body(node.orelse)
        self.line(r"\EndIf%")

    def visit_While(self, node):
        if not self._emit_tex:
            return
        self.line(r"\While{" + self.expr(node.test) + "}")
        self.body(node.body)
        self.line(r"\EndWhile%")

    def visit_Return(self, node):
        if not self._emit_tex:
            return
        if node.value:
            self.line(r"\Return{" + self.expr(node.value) + "}")
        else:
            self.line(r"\Return{}")

    def visit_List(self, node):
        elts = r" \PyListSep ".join(self.visit(el) for el in node.elts)
        return r"\PyList{" + elts + "}"

    def generic_visit(self, node):
        # Fallback para que no se colapse
        print(f"WARN: Nodo AST no manejado: {type(node).__name__}")
        return r"\PyName{---NODO-NO-SOPORTADO---}"


def ast_to_pseudocode(source_ast, **kwargs):
    return "\n".join(Py2Tex(**kwargs).visit(source_ast)) + "\n"

def source_to_pseudocode(source, **kwargs):
    return ast_to_pseudocode(ast.parse(source), **kwargs)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Python file to convert")
    args = parser.parse_args()

    with open(args.file) as f:
        source = f.read()
    
    try:
        parsed_ast = ast.parse(source)
        py2tex = Py2Tex()
        py2tex.visit(parsed_ast)
        print(py2tex.to_string(), end="")
    except Exception as e:
        # Imprime el error en el .tex para depuración
        print(r"\State \ERROR{Error al procesar el archivo Python:}")
        print(r"\State \ERROR{" + str(e) + r"}")

if __name__ == "__main__":
    main()