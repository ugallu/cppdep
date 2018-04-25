PATH = '.'
import os
from glob import glob
headers = [y for x in os.walk(PATH) for y in glob(os.path.join(x[0], '*.h'))]
cpps = [y for x in os.walk(PATH) for y in glob(os.path.join(x[0], '*.cpp'))]
cs= [y for x in os.walk(PATH) for y in glob(os.path.join(x[0], '*.c'))]

cpps = cpps + cs
graph = {}

def processFile(fn):
    predir = ""
    if fn.rfind("/") > -1:
        predir = fn[:fn.rfind("/")+1]
    with open(fn) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    
    name = fn[:fn.find('.')]
    if not name in graph:
        graph[name] = []
    for line in content:
        if "#include" in line and "\"" in line:
            includeName = line[line.find("\"")+1:line.rfind(".")]
            if predir + includeName+".h" in headers:
                includeName = predir + includeName
            if not name == includeName:
                graph[name].append(includeName)

headers =  [x[2:] for x in headers]
cpps =  [x[2:] for x in cpps]

for h in headers:
    processFile(h)
    
for c in cpps:
    processFile(c)
    
def createGraph(l):
    
    print"digraph dependencies {"
    for node in l:
        for c in l[node]:
            print "\""+node+"\" -> \""+c+"\""
    print "}"

createGraph(graph)
