import clang.cindex
import json

def extract_(file):
    """ Extract AST from a c++ file using Clang """
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file)
    return parse_node(translation_unit.cursor)

def parse_node(node):
    """ Recursively parse a node in the AST """
    ast_data = {
        "kind" : str(node.kind),
        "spelling" : node.spelling,
        "location" : f"{node.location.file} : {node.location.line}"\
        if node.location.file else None,
        "children" : [parse_node(child) \
                      for child in node.get_children()]
    }

    return ast_data


cpp_file = "sample.cc"
ast = extract_(cpp_file)
with open("ast.json","w") as f:
    json.dump(ast,f,indent=4)

print("AST extracted and saved to ast.json")
