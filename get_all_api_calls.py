import os
import ast, astunparse
import re
from visitors import ClassVisitor, FuncVisitor
from check_for_deprecation import check_for_deprecation_in_function, check_for_deprecation_in_class

def automatic_api_deprecation_detection(file1,file2,path1):
    def generate_ast_tree(path):
        code_text = open(path).read()
        tree = ast.parse(code_text, type_comments = True)
        return tree

    def print_py_files(path,files_list):
        for file in os.listdir(path):
            if(file == 'tests'):
                continue
            if(os.path.isfile(path+str(file)) and re.search(".*\.py$",file)):
                files_list.append(path+str(file))
            elif(os.path.isdir(path+str(file))):
                print_py_files(path+str(file)+"/",files_list)
        return files_list

    py_files = print_py_files(path1,[])

    print(len(py_files))
    for file in py_files:
        l1 = file.split('/')
        API_string = ""
        for i in range(2,len(l1)-1):
            API_string+=l1[i]
            API_string+="."    
        try:
            tree = generate_ast_tree(file)
            cv = ClassVisitor()
            cv.visit(tree)
            classes_list = cv.return_class_names()
            check_for_deprecation_in_class(API_string,classes_list,cv._class_nodes,file2)
            functions_in_class_list = cv.get_func_names()
            # check_for_deprecation_in_class(cv._class_nodes)
            fv = FuncVisitor()
            fv.visit(tree)
            functions_list = list(set(fv.return_func_names()))
            # check_for_deprecation_in_class(API_string,classes_list,cv._class_nodes,file2)
            try:
                functions_list = [f for f in functions_list if f not in functions_in_class_list]
            except:
                pass
            check_for_deprecation_in_function(API_string,functions_list,fv._func_nodes,file2)
            # print(classes_list,functions_list,functions_in_class_list)
            for f in functions_list:
                file1.write(API_string+f+"()\n")
            if(len(classes_list)!=0):
                for c in classes_list:
                    if(c[0]=="_"):
                        continue
                    check_for_deprecation_in_function(API_string+c+".",functions_in_class_list,cv._func_nodes,file2)
                    file1.write(API_string+c+"\n")
                    for fc in functions_in_class_list:
                        file1.write(API_string+c+"."+fc+"()\n")
        except:
            pass

