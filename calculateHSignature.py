#!/usr/bin/python
# coding: UTF-8

import numpy as np


def calculateHSignature(path, obsts):
    m = max(len(obsts)-1, 5)
    a = np.ceil( float(m)/2 )
    b = m - a
    
    end = complex(path[0][0], path[0][1])
    start = complex(path[-2][0], path[-2][1])
    delta = end-start
    normal = complex(-delta.imag, delta.real)
    
    if np.abs(delta) < 3.0:
        map_bottom_left = start + complex(0, -3)
        map_top_right = start + complex(3, 3)
    else:
        map_bottom_left = start - normal
        map_top_right = start + delta + normal

    hsignature = 0

    for i in range(0, len(path)-1):
        z1 = complex(path[i][0], path[i][1])
        z2 = complex(path[i+1][0], path[i+1][1])

        for o1 in obsts:
            obst_l = complex(o1[0], o1[1])
            """
            f0 = h_signature_prescaler * a * (obst_l-map_bottom_left) * b * (obst_l-map_top_right)
            
            Al = f0
            for o2 in obsts:
                if o1 == o2:
                    continue
                obst_j = complex(o2[0], o2[1])
                diff = obst_l - obst_j
                Al = Al / diff
            """
            Al = 1000
            diff2 = np.abs(z2-obst_l)
            diff1 = np.abs(z1-obst_l)

            if (diff2 == 0 or diff1 == 0):
                continue
            log_real = np.log(diff2)-np.log(diff1)
            arg_diff = np.angle(z2-obst_l)-np.angle(z1-obst_l)

            imag_proposals = []

            imag_proposals.append(arg_diff) 
            imag_proposals.append(arg_diff+2*np.pi)
            imag_proposals.append(arg_diff-2*np.pi)
            imag_proposals.append(arg_diff+4*np.pi)
            imag_proposals.append(arg_diff-4*np.pi)

            log_imag = min(imag_proposals,key=abs)
            log_value = complex(log_real,log_imag)
            hsignature += Al*log_value
    return hsignature

h_signature_prescaler = 1.0

if __name__ == '__main__':
    path = [(8, 8), (7, 7), (6, 6), (5, 6), (4, 5), (3, 4), (2, 3), (1, 2), (0, 1), (0, 0)]
    obsts = []
    obsts.append((1,1))
    obsts.append((5,5))
    obsts.append((3,3))
    obsts.append((2,6))
    obsts.append((6,2))
    print calculateHSignature(path, obsts)

      
