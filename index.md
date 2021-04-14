# OFDClean

Pythpn implementation of Contextual Data Cleaning with Ontological Functional Dependencies.

## Datasets

Dataset, ofds, senses of clinical data of [Python code](https://github.com/ltzheng/OFDClean/tree/master/Python/datasets) and [Java code](https://github.com/ltzheng/OFDClean/tree/master/Java/data). 

## Source code

The source code is available [here](https://github.com/ltzheng/OFDClean). 

### Python code 

- Initial sense assignment
- Local sense refinement
- Provided by Longtao Zheng

#### Data path and format

Input data should align with the format in directory `datasets`

#### Run

Configure the path of data, OFDs, and senses in `main.py`, then run `python main.py`.

### Java code 

- Repair data by beam search
- Provided by Zheng Zheng

### Plot script

Figure 7 and 8 in the paper.

- Figure 8 (c)

  ```
  # Scale font and line width (dpi) by changing the size! It will always display stretched.
  set terminal svg size 400,300 enhanced fname 'arial'  fsize 10 butt solid
  set output 'out.svg'

  # Key means label...
  set ylabel 'Running Time (s)'
  set xtics font ", 16"
  set ytics font ", 16"
  set style line 1 lw 2 lc rgb '#000000' ps 2 pt 8 pi 1
  set xtics 2
  set ytics 0.2
  set yrange [0:1]
  set key inside bottom right
  set ylabel 'Accuracy'
  set style line 1 lw 2 lc rgb '#000000' ps 2 pt 8 pi 1
  set style line 2 lw 2 lc rgb '#0000FF' ps 2 pt 2 pi 1
  plot  "data.txt" using 1:2 title 'Precision' with linespoints ls 1, "data.txt" using 1:3 title 'Recall' with linespoints ls 2
  ```

- Figure 8 (d)

  ```
  # Scale font and line width (dpi) by changing the size! It will always display stretched.
  set terminal svg size 400,300 enhanced fname 'arial'  fsize 10 butt solid
  set output 'out.svg'

  # Key means label...
  set ylabel 'Running Time (s)'
  set xtics font ", 16"
  set ytics font ", 16"
  set style line 1 lw 2 lc rgb '#000000' ps 2 pt 8 pi 1
  set xtics 2
  set ytics 1
  plot  "data.txt" u 1:2 with linespoints ls 1 notitle
  ```
  
- Figure 8 (e)

  ```
  # Scale font and line width (dpi) by changing the size! It will always display stretched.
  set terminal svg size 400,300 enhanced fname 'arial'  fsize 10 butt solid
  set output 'out.svg'

  # Key means label...
  set ylabel 'Running Time (s)'
  set xtics font ", 16"
  set ytics font ", 16"
  set style line 1 lw 2 lc rgb '#000000' ps 2 pt 8 pi 1
  set xtics 3
  set ytics 0.2
  set yrange [0:1]
  set key inside bottom right
  set ylabel 'Accuracy'
  set style line 1 lw 2 lc rgb '#000000' ps 2 pt 8 pi 1
  set style line 2 lw 2 lc rgb '#0000FF' ps 2 pt 2 pi 1
  plot  "data.txt" using 1:2 title 'Precision' with linespoints ls 1, "data.txt" using 1:3 title 'Recall' with linespoints ls 2
  ```

- Figure 8 (f)
 
  ```
  # Scale font and line width (dpi) by changing the size! It will always display stretched.
  set terminal svg size 400,300 enhanced fname 'arial'  fsize 10 butt solid
  set output 'out.svg'

  # Key means label...
  set ylabel 'Running Time (s)'
  set xtics font ", 16"
  set ytics font ", 16"
  set style line 1 lw 2 lc rgb '#000000' ps 2 pt 8 pi 1
  set xtics 3
  set ytics 0.5
  plot  "data.txt" u 1:2 with linespoints ls 1 notitle
  ```

- Figure 8 (g)
  
  ```
  # Scale font and line width (dpi) by changing the size! It will always display stretched.
  set terminal svg size 400,300 enhanced fname 'arial'  fsize 10 butt solid
  set output 'out.svg'

  # Key means label...
  set ylabel 'Running Time (s)'
  set xtics font ", 16"
  set ytics font ", 16"
  set style line 1 lw 2 lc rgb '#000000' ps 2 pt 8 pi 1
  set xtics 0.2
  set ytics 0.2
  set yrange [0:1]
  set key inside bottom right
  set ylabel 'Accuracy'
  set style line 1 lw 2 lc rgb '#000000' ps 2 pt 8 pi 1
  set style line 2 lw 2 lc rgb '#0000FF' ps 2 pt 2 pi 1
  plot  "data.txt" using 1:2 title 'Precision' with linespoints ls 1, "data.txt" using 1:3 title 'Recall' with linespoints ls 2
  ```

- Figure 8 (h)
  
  ```
  # Scale font and line width (dpi) by changing the size! It will always display stretched.
  set terminal svg size 400,300 enhanced fname 'arial'  fsize 10 butt solid
  set output 'out.svg'

  # Key means label...
  set ylabel 'Running Time (s)'
  set xtics font ", 16"
  set ytics font ", 16"
  set style line 1 lw 2 lc rgb '#000000' ps 2 pt 8 pi 1
  set xtics 0.2
  set ytics 4
  plot  "data.txt" u 1:2 with linespoints ls 1 notitle
  ```
