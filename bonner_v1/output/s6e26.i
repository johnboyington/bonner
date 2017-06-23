Bonner Sphere Template
c  *********************************************************
c                           BLOCK 1
c  *********************************************************
c
21 4 -3.840000   -21    -13 14           $LiI(Eu) crystal
22 0             -22    -12 14 #21       $crystal space
c
23 3 -2.500000   -22    -14 16           $pglass top
24 3 -2.500000   -23    -16 18           $pglass bot
c
25 2 -2.699   -24    -11 12               $Al tip
26 2 -2.699   -24 22 -12 15               $Al top
27 2 -2.699   -25    -15 16 22            $Al top
28 2 -2.699   -25    -16 17 23            $Al top
29 2 -2.699   -26    -17 18 23            $Al top
30 0             -27    -18 19            $Al top
31 2 -2.699   -26    -18 19 27            $Al top
c
11 5 -1.200000   -01  #21 #22 #23 #24 #25 #26 #27 #28 #29 #30 #31
90 1 -0.001293   -99 24 -11 15 #11    $space
91 1 -0.001293   -99 25 -15 17 #11    $space
92 1 -0.001293   -99 26 -17 19 #11    $space
93 1 -0.001293   -99       -19        $space
94 1 -0.001293   -99        11 #11    $space
99 0              99                  $graveyard (RIP in peace)

c  *********************************************************
c                           BLOCK 2
c  *********************************************************
01  S   0 0 -0.9  15.24    $Bonner Sphere
c
11 PZ    0.00    $plane tip top
12 PZ   -0.20    $plane tip bot
13 PZ   -0.70    $plane crystal top
14 PZ   -1.10    $plane crystal bot
15 PZ   -4.50    $plane 1.5
16 PZ   -4.70    $plane 1.6
17 PZ  -10.50    $plane 1.7
18 PZ  -11.70    $plane 1.8
19 PZ  -20.00
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

c  *********************************************************
c                           BLOCK 3
c  *********************************************************
NPS   2E9
IMP:N 1 16r 0
c  ---------------------------------------------------------
c                    SOURCE SPECIFICATIONS
c  ---------------------------------------------------------
SDEF   POS=-15.24 0 0 AXS=1 0 0 EXT=0 VEC=1 0 0 ERG=D1
       DIR=D5 RAD=D6 PAR=1
SI1   4.8052e-05 0.000148729
SP1   0  1
SI6   0  1.27
SP6 -21  1
SI5 H    -1.00000e+00 6.12323e-17 1.73648e-01 3.42020e-01
          5.00000e-01 6.42788e-01 7.66044e-01 8.66025e-01
          9.39693e-01 9.84808e-01 9.97564e-01 9.98630e-01
          9.99391e-01 9.99848e-01 1.00000e+00
SP5 D     0.00000e+00 8.63429e-10 2.62736e-10 9.32365e-10
          1.73756e-09 2.56126e-09 3.26996e-09 3.75745e-09
          3.97569e-09 4.12532e-09 4.70193e-09 5.77100e-09
          1.07535e-08 1.14822e-08 5.54211e-09
c  ---------------------------------------------------------
c  ----------------------MATERIAL CARDS---------------------
c  ---------------------------------------------------------
c
c  ---------------------------------------------------------
c  MATERIAL 1:      AIR      
c  ------------------------(density 0.001293 g/cm^3)--------
c  ---------------------------------------------------------
M1    7014 -0.7558
      8016 -0.2314
     18000 -0.0128
c
c  ---------------------------------------------------------
c  MATERIAL 2:      Al    
c  ---------------------------(density 2.699 g/cm^3)--------
c  ---------------------------------------------------------
M2  13027.70c   -1 
c
c  ---------------------------------------------------------
c  MATERIAL 3:      SILICON    
c  ---------------------------(density 7.858 g/cm^3)--------
c  ---------------------------------------------------------
M3   14000 0.33
      8016 0.67
c
c  ---------------------------------------------------------
c  MATERIAL 4:      LiI(Eu)    
c  ---------------------------(density 3.84 g/cm^3)--------
c  ---------------------------------------------------------
M4    3006.70c -0.0518
     53127.70c -0.9482
c  ---------------------------------------------------------
c  MATERIAL 5:      HDPE    
c  ---------------------------(density 1.000 g/cm^3)--------
c  ---------------------------------------------------------
M5     1001     -0.125355
       5010.70c -0.100000
       6000     -0.774645 
c
c TALLY
F14:N 21
FM14: 1 4 105
