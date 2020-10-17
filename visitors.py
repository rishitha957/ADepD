import ast, astunparse

class DocStringVisitor(ast.NodeVisitor):
    """Visits all the Constant Nodes in AST to get the doc string"""
    def __init__(self):
        self.visited = 0;
        self.doc_str = ""
    def return_str(self):
        return self.doc_str
    def generic_visit(self,node):
        if isinstance(node, ast.Constant) and self.visited == 0:
            self.visited = 1
            self.doc_str = node.value
        ast.NodeVisitor.generic_visit(self,node)

class FuncVisitor(ast.NodeVisitor):
    """Visits all the FunctionDef Nodes in AST"""
    def __init__(self):
        super(FuncVisitor, self).__init__()
        self.func_names = []
        self._func_nodes = []
        self.func_dec_map = []

    def flatten_attr(self,node):
        """For Nested Decorators"""
        if isinstance(node, ast.Attribute):
            return str(self.flatten_attr(node.value)) + '.' + node.attr
        elif isinstance(node, ast.Name):
            return str(node.id)
        else:
            pass
    def return_func_names(self):
        return self.func_names

    def return_list(self):
        return self.func_dec_map

    def return_decorator_list(self, _func_nodes = None):
        if _func_nodes is None:
            _func_nodes = self._func_nodes
        for node in _func_nodes:
            found_decorators = []
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Name):
                    found_decorators.append(decorator.id)
                elif isinstance(decorator, ast.Attribute):
                    found_decorators.append(self.flatten_attr(decorator))
                elif isinstance(decorator, ast.Call):
                    comment = ""
                    id1 = ""
                    for val_node in ast.walk(decorator):
                        if isinstance(val_node,ast.Name):
                            id1 = val_node.id
                        if isinstance(val_node,ast.Constant):
                            comment = val_node.value
                    try:
                        found_decorators.append(id1+" # "+comment)
                    except:
                        pass
            self.func_dec_map.append((node.name,found_decorators))
        return self.func_dec_map

    def generic_visit(self,node):
        if isinstance(node,ast.FunctionDef):
            if node.name.find("warn")!=-1 or node.name[0]!="_":
                self.func_names.append(node.name)
                self._func_nodes.append(node)
        ast.NodeVisitor.generic_visit(self,node)

        
class ClassVisitor(ast.NodeVisitor):
    def __init__(self):
        self.class_names = []
        self._class_nodes = []
        self._func_nodes = []
    def return_class_names(self):
        return self.class_names
    def get_doc_string_class(self):
        dv = DocStringVisitor()
        doc_str_list = []
        for i in range(len(self.class_names)):
            dv.visit(self._class_nodes[i])
            doc_str_list.append((self.class_names[i],dv.return_str()))
    def get_func_names(self):
        fv = FuncVisitor()
        for node in self._class_nodes:
            fv.visit(node)
            self._func_nodes = fv._func_nodes
            return fv.return_func_names()
    def generic_visit(self,node):
        if isinstance(node, ast.ClassDef):
            self.class_names.append(node.name)
            self._class_nodes.append(node)
        ast.NodeVisitor.generic_visit(self,node)