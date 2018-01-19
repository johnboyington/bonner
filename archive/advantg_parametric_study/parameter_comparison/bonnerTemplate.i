Bonner Sphere Template
c
c Updated  7/12/17 by John Boyington 
c 
c ****************************************************************************** 
c                               CELL CARDS 
c ******************************************************************************
c
c                        -----HDPE SPHERE------
11 1 -0.95    (-1 11):(-1 -11 15 24):(-1 -15 17 25):(-1 -17 26)
c 
c                     -----DETECTOR ASSEMBLY------
c                               -----LiI crystal
21 2 -3.84    -21    -13 14   
c
c
c                               -----vaccuum around crystal
22 0          (-12 13 -22):(-13 14 21 -22)
c
c
c                               -----pmma light guide
23 3 -2.50    (-22 -14 16):(-23 -16 18)
c
c
c                               -----aluminum casing
24 4 -2.699   (-24 -11 12):(-24 22 -12 15):(-25 -15 16 22):
              (-25 -16 17 23):(-26 -17 18 23):(-26 -18 19 27)
c
c
c                               -----vaccuum in pmt
25 0          -27 -18 19 
c
c
c                     -----PROBLEM SPACE------
c                               -----air around sphere (modeled as vaccuum)
90 0          (1 -99 24 -11 15):(1 -99 25 -15 17):
              (1 -99 26 -17 19):(1 -99 -19):(1 -99 11)
c
c                               -----graveyard
99 0              99 

c ****************************************************************************** 
c                               SURFACE CARDS 
c ****************************************************************************** 
01  S   0 0 0  6.35    $Bonner Sphere
c
11 PZ    0.9    $plane tip top
12 PZ    0.7    $plane tip bot
13 PZ    0.2    $plane crystal top
14 PZ   -0.2    $plane crystal bot
15 PZ   -3.6    $plane 1.5
16 PZ   -3.8    $plane 1.6
17 PZ   -9.6    $plane 1.7
18 PZ  -10.8    $plane 1.8
19 PZ  -19.1
c
21 CZ    0.20    $cylinder 1.1
22 CZ    0.50    $cylinder 1.2
23 CZ    0.60    $cylinder 1.3
24 CZ    0.70    $cylinder 1.4
25 CZ    0.90    $cylinder 1.5
26 CZ    2.54    $cylinder 1.6
27 CZ    2.14    $cylinder 1.7
c
c
99 RPP -40 20  -20 20  -40 30 

c ****************************************************************************** 
c                               DATA CARDS 
c ******************************************************************************
IMP:N 1 6r 0
NPS   1E7
c  -----------------------------------------------------------------------------
c                                                   SOURCE SPECIFICATIONS
c  -----------------------------------------------------------------------------
SDEF   POS=-15.24 0 0 AXS=1 0 0 EXT=0 VEC=1 0 0 ERG=6.3100E+00
       DIR=1 RAD=D6 PAR=1
SI6   0  6.35
SP6 -21  1
c
c  -----------------------------------------------------------------------------
c                                                          MATERIAL CARDS
c  -----------------------------------------------------------------------------
c
c  -----------------------------------------------------------------------------
c  MATERIAL 1:      HDPE    
c  ---------------------------(density 0.950 g/cm^3)----------------------------
c  -----------------------------------------------------------------------------
M1     1001     -0.143
       6000     -0.857
MT1    poly.10t 
c
c  -----------------------------------------------------------------------------
c  MATERIAL 2:      LiI(Eu)    
c  ---------------------------(density 3.84 g/cm^3)-----------------------------
c  -----------------------------------------------------------------------------
M2    3006.70c -0.0518
     53127.70c -0.9482
c
c  -----------------------------------------------------------------------------
c  MATERIAL 3:      PMMA Light Pipe   
c  ---------------------------(density 7.858 g/cm^3)----------------------------
c  -----------------------------------------------------------------------------
M3    1001     -0.08
      6000     -0.60
     16000     -0.32
c
c  -----------------------------------------------------------------------------
c  -----------------------------------------------------------------------------
c  MATERIAL 4:      Al    
c  ---------------------------(density 2.699 g/cm^3)----------------------------
c  -----------------------------------------------------------------------------
M4  13027.70c   -1 
c
c  -----------------------------------------------------------------------------
c                                                             TALLY CARDS       
c  -----------------------------------------------------------------------------
c
c  -----------------------------------------------------------------------------
c  TALLY 14:      Light Creation within Li in Lithium Crystal
c  -----------------------------------------------------------------------------
c                               -----cell tally in crystal region
F14:N 21
c
c                               -----tally multiplier
c     Constant of proportionality | material  | 105 is (n,t) reaction of Li-6
FM14: 1 2 105
c
c
c ****************************************************************************** 
c                             END OF INPUT FILE
c ******************************************************************************
