from visitors import ClassVisitor, FuncVisitor, DocStringVisitor
import astunparse,ast


def check_for_hard_coded_warning(api_str,node,file_name):
	val = ""
	id1 = ""			
	for node1 in ast.walk(node):
		if isinstance(node1,ast.Name):
			id1 += node1.id+","
		if isinstance(node1,ast.Constant) and node1.value:
			try:
				val += node1.value+","
			except:
				pass
	if id1.find("FutureWarning")!=-1 or id1.find("Deprecat")!=-1:
		file_name.write(api_str+node.name+"() : "+val+id1+"\n")

def check_for_doc_string_comments(api_str,node,file_name):
	dv = DocStringVisitor()
	dv.visit(node)
	doc_str = dv.return_str()
	# print(doc_str)
	try:
		if doc_str.find("deprecat")!=-1:
			doc_str_1 = doc_str.split("\n")
			str1 = ""
			for doc in doc_str_1:
				if doc.find("deprecat")!=-1:
					str1+=doc+" "
			file_name(api_str+node.name+"() : "+str1+"\n")
	except:
		pass

def check_for_deprecation_in_function(api_str,func_name,node_list,file_name):
	for node in node_list:
		# print(astunparse.dump(node))
		check_for_doc_string_comments(api_str,node,file_name)
		if node.name.find("warn")!=-1:
			check_for_hard_coded_warning(api_str,node,file_name)
		fv = FuncVisitor()
		fv.visit(node)
		f = fv.return_decorator_list([node])
		for i in range(len(f)):
			# print(f[1])
			for j in f[i][1]:
				if len(j)>0 and j.find('deprecate')!=-1:
					file_name.write(api_str+f[i][0]+"() : "+j+"\n")

def check_for_deprecation_in_class(api_str,class_name,node_list,file_name):
	for node in node_list:
		check_for_doc_string_comments(api_str,node,file_name)

	