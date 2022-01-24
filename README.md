# Chart Plot

## Install

```bash
pip install matplotlib getch numpy
```

## Run

### Create Data
```bash
python CreateData.py
```

### Edit Data
```bash
python EditData.py
```

### Plot Data
```bash
python PlotData.py
```

### Save Finished Data
```bash
all you need to save is just your finished json file
```

## Control

### Mode Select
```bash
q : NORMAL Mode
i : EDIT Mode
a : ADD Mode
s : SCALE Mode
```

### Common func
```bash
x : quit scripts
u : regenerate confidence interval
d : delete current point
```

### NORMAL Mode
```bash
h : select left point
l : select right point
j : select last line
k : select next line
```

### EDIT Mode
```bash
h : move point left
l : move point right
j : move point down
k : move point up
J : lower confidence interval
K : upper confidence interval
o : lower confidence max
p : upper confidence max
n : lower confidence min
m : upper confidence min
```

### ADD Mode
```bash
h : move point left
l : move point right
j : move point down
k : move point up
H : 10h
L : 10l
J : 10j
K : 10k
a : add point to line
n : create new line start from current position
```

### SCALE Mode
```bash
h : move left all data
l : move right all data
j : move down all data
k : move up all data
H : scale x lower
L : scale x upper
J : scale y lower
K : scale y upper
```

## Enjoy it~

