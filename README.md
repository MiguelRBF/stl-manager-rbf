# stl-manager-rbf
Born to manage stl files

## Execution

```bash
python3 -m slicer.slicer
```

## Running pydeps

This allow you to see a graph with the imports of the provided script

```bash
pydeps slicer/slicer.py
```

### Common errors when launched

#### **graphviz**
```bash
ERROR:
cannot find 'dot'
pydeps calls dot (from graphviz) to create svg diagrams, please make sure that the dot executable is available on your path.
```

Install:
```bash
sudo apt install graphviz
```

#### **wslview**

```bash
[Errno 2] No such file or directory: '/usr/bin/wslview'
(can be caused by not finding the program to open this file)
```

Install:
```bash
sudo apt install wslu
```