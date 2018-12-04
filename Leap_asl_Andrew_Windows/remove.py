import numpy as np
import os
import csv



DATA_DIR1 = './Train_Data/'
DATA_DIR2 = './Train_Data2/'
for filename in os.listdir(DATA_DIR1):
    with open(DATA_DIR1 + filename, 'rb') as f:
        rdr = csv.reader(f)
        #data = list(rdr)
        #print data
        #print(filename)
        #print len(data[1])
        #print len(next(rdr))
        with open(DATA_DIR2 +filename, "wb") as result:
            wtr = csv.writer(result)
            for r in rdr:
                wtr.writerow((r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10],
                    r[11], r[12], r[13], r[14], r[15], r[16], r[17], r[18], r[19], r[20],
                    r[21], r[22], r[23], r[24], r[25], r[26], r[27], r[28], r[29], r[30],
                    r[31], r[32], r[33], r[34], r[35], r[36], r[37], r[38], r[39], r[40],
                    r[41]))

            
