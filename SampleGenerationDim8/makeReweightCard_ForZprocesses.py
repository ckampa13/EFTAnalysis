import decimal
import math

file1 = open("WWZ_reweight_card.dat","w+")

L = [
"change mode NLO       # Define type of Reweighting. For LO sample this command\n", 
"                      # has no effect since only LO mode is allowed. \n",
"change helicity False # has also been done in the example I got from Kenneth \n"
"change rwgt_dir rwgt\n"]

file1.writelines(L)

L = [
"set anoinputs 1 0.0e-12 # FS0\n",
"set anoinputs 2 0.0e-12 # FS1\n",
"set anoinputs 3 0.0e-12 # FS2\n",
"set anoinputs 4 0.0e-12 # FM0\n",
"set anoinputs 5 0.0e-12 # FM1\n",
"set anoinputs 6 0.0e-12 # FM2\n",
"set anoinputs 7 0.0e-12 # FM3\n",
"set anoinputs 8 0.0e-12 # FM4\n",
"set anoinputs 9 0.0e-12 # FM5\n",
"set anoinputs 10 0.0e-12 # FM6\n",
"set anoinputs 11 0.0e-12 # FM7\n",
"set anoinputs 12 0.0e-12 # FT0\n",
"set anoinputs 13 0.0e-12 # FT1\n",
"set anoinputs 14 0.0e-12 # FT2\n",
"set anoinputs 15 0.0e-12 # FT3\n",
"set anoinputs 16 0.0e-12 # FT4\n",
"set anoinputs 17 0.0e-12 # FT5\n",
"set anoinputs 18 0.0e-12 # FT6\n",
"set anoinputs 19 0.0e-12 # FT7\n",
"set anoinputs 20 0.0e-12 # FT8\n",
"set anoinputs 21 0.0e-12 # FT9\n"
]

FS0 = [-3.0e-8, -1.5e-8, -1e-8, -0.8e-8, -0.4e-8, -0.2e-8, 0.2e-8, 0.4e-8, 0.8e-8, 1e-8, 1.5e-8, 3.0e-8]
FS1 = [-3.0e-8, -1.5e-8, -1e-8, -0.8e-8, -0.4e-8, -0.2e-8, 0.2e-8, 0.4e-8, 0.8e-8, 1e-8, 1.5e-8, 3.0e-8]
FS2 = [-3.0e-8, -1.5e-8, -1e-8, -0.8e-8, -0.4e-8, -0.2e-8, 0.2e-8, 0.4e-8, 0.8e-8, 1e-8, 1.5e-8, 3.0e-8]

FM0 = [-3.0e-11, -1.5e-11, -1e-11, -0.8e-11, -0.4e-11, -0.2e-11, 0.2e-11, 0.4e-11, 0.8e-11, 1e-11, 1.5e-11, 3.0e-11]
FM1 = [-3.0e-11, -1.5e-11, -1e-11, -0.8e-11, -0.4e-11, -0.2e-11, 0.2e-11, 0.4e-11, 0.8e-11, 1e-11, 1.5e-11, 3.0e-11]
FM2 = [-3.0e-11, -1.5e-11, -1e-11, -0.8e-11, -0.4e-11, -0.2e-11, 0.2e-11, 0.4e-11, 0.8e-11, 1e-11, 1.5e-11, 3.0e-11]
FM3 = [-3.0e-11, -1.5e-11, -1e-11, -0.8e-11, -0.4e-11, -0.2e-11, 0.2e-11, 0.4e-11, 0.8e-11, 1e-11, 1.5e-11, 3.0e-11]
FM4 = [-3.0e-11, -1.5e-11, -1e-11, -0.8e-11, -0.4e-11, -0.2e-11, 0.2e-11, 0.4e-11, 0.8e-11, 1e-11, 1.5e-11, 3.0e-11]
FM5 = [-3.0e-11, -1.5e-11, -1e-11, -0.8e-11, -0.4e-11, -0.2e-11, 0.2e-11, 0.4e-11, 0.8e-11, 1e-11, 1.5e-11, 3.0e-11]
FM6 = [-3.0e-11, -1.5e-11, -1e-11, -0.8e-11, -0.4e-11, -0.2e-11, 0.2e-11, 0.4e-11, 0.8e-11, 1e-11, 1.5e-11, 3.0e-11]
FM7 = [-3.0e-11, -1.5e-11, -1e-11, -0.8e-11, -0.4e-11, -0.2e-11, 0.2e-11, 0.4e-11, 0.8e-11, 1e-11, 1.5e-11, 3.0e-11]

FT0 = [-3.0e-12, -1.5e-12, -1e-12, -0.8e-12, -0.4e-12, -0.2e-12, 0.2e-12, 0.4e-12, 0.8e-12, 1e-12, 1.5e-12, 3.0e-12]
FT1 = [-3.0e-12, -1.5e-12, -1e-12, -0.8e-12, -0.4e-12, -0.2e-12, 0.2e-12, 0.4e-12, 0.8e-12, 1e-12, 1.5e-12, 3.0e-12]
FT2 = [-3.0e-12, -1.5e-12, -1e-12, -0.8e-12, -0.4e-12, -0.2e-12, 0.2e-12, 0.4e-12, 0.8e-12, 1e-12, 1.5e-12, 3.0e-12]

FT5 = [-3.0e-11, -1.5e-11, -1e-11, -0.8e-11, -0.4e-11, -0.2e-11, 0.2e-11, 0.4e-11, 0.8e-11, 1e-11, 1.5e-11, 3.0e-11]
FT6 = [-3.0e-11, -1.5e-11, -1e-11, -0.8e-11, -0.4e-11, -0.2e-11, 0.2e-11, 0.4e-11, 0.8e-11, 1e-11, 1.5e-11, 3.0e-11]
FT7 = [-3.0e-11, -1.5e-11, -1e-11, -0.8e-11, -0.4e-11, -0.2e-11, 0.2e-11, 0.4e-11, 0.8e-11, 1e-11, 1.5e-11, 3.0e-11]

total = len(FS0) + len(FS1) + len(FS2) + len(FM0) + len(FM1) + len(FM2) + len(FM3) + len(FM4) + len(FM5) + len(FM6) + len(FM7) + len(FT0) + len(FT1) + len(FT2) + len(FT5) + len(FT6) + len(FT7) 

for i in range(0, len(FS0)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(i+1) + "/" + str(total) + "] FS0:" + str(FS0[i])+"\n")
  if(FS0[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__FS0_m"+"{:1.2g}".format(math.fabs(FS0[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__FS0_p"+"{:1.2g}".format(math.fabs(FS0[i]))+"\n")
  file1.write("set anoinputs 1 " + str(FS0[i]) + " # FS0\n")
  file1.write(L[1])
  file1.write(L[2])
  file1.write(L[3])
  file1.write(L[4])
  file1.write(L[5])
  file1.write(L[6])
  file1.write(L[7])
  file1.write(L[8])
  file1.write(L[9])
  file1.write(L[10])
  file1.write(L[11])
  file1.write(L[12])
  file1.write(L[13])
  file1.write(L[14])
  file1.write(L[15])
  file1.write(L[16])
  file1.write(L[17])
  file1.write(L[18])
  file1.write(L[19])
  file1.write(L[20])

for i in range(0, len(FS1)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(i+1+len(FS0)) + "/" + str(total) + "] FS1:" + str(FS1[i])+"\n")
  if(FS1[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__FS1_m"+"{:1.2g}".format(math.fabs(FS1[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__FS1_p"+"{:1.2g}".format(math.fabs(FS1[i]))+"\n")
  file1.write(L[0])
  file1.write("set anoinputs 2 " + str(FS1[i]) + " # FS1\n")
  file1.write(L[2])
  file1.write(L[3])
  file1.write(L[4])
  file1.write(L[5])
  file1.write(L[6])
  file1.write(L[7])
  file1.write(L[8])
  file1.write(L[9])
  file1.write(L[10])
  file1.write(L[11])
  file1.write(L[12])
  file1.write(L[13])
  file1.write(L[14])
  file1.write(L[15])
  file1.write(L[16])
  file1.write(L[17])
  file1.write(L[18])
  file1.write(L[19])
  file1.write(L[20])

for i in range(0, len(FS2)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(i+1+len(FS0)+len(FS1)) + "/" + str(total) + "] FS2:" + str(FS2[i])+"\n")
  if(FS2[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__FS2_m"+"{:1.2g}".format(math.fabs(FS2[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__FS2_p"+"{:1.2g}".format(math.fabs(FS2[i]))+"\n")
  file1.write(L[0])
  file1.write(L[1])
  file1.write("set anoinputs 3 " + str(FS2[i]) + " # FS2\n")
  file1.write(L[3])
  file1.write(L[4])
  file1.write(L[5])
  file1.write(L[6])
  file1.write(L[7])
  file1.write(L[8])
  file1.write(L[9])
  file1.write(L[10])
  file1.write(L[11])
  file1.write(L[12])
  file1.write(L[13])
  file1.write(L[14])
  file1.write(L[15])
  file1.write(L[16])
  file1.write(L[17])
  file1.write(L[18])
  file1.write(L[19])
  file1.write(L[20])


for i in range(0, len(FM0)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(i+1+len(FS0)+len(FS1)+len(FS2)) + "/" + str(total) + "] FM0:" + str(FM0[i])+"\n")
  if(FM0[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__FM0_m"+"{:1.2g}".format(math.fabs(FM0[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__FM0_p"+"{:1.2g}".format(math.fabs(FM0[i]))+"\n")
  file1.write(L[0])
  file1.write(L[1])
  file1.write(L[2])
  file1.write("set anoinputs 4 " + str(FM0[i]) + " # FM0\n")
  file1.write(L[4])
  file1.write(L[5])
  file1.write(L[6])
  file1.write(L[7])
  file1.write(L[8])
  file1.write(L[9])
  file1.write(L[10])
  file1.write(L[11])
  file1.write(L[12])
  file1.write(L[13])
  file1.write(L[14])
  file1.write(L[15])
  file1.write(L[16])
  file1.write(L[17])
  file1.write(L[18])
  file1.write(L[19])
  file1.write(L[20])

for i in range(0, len(FM1)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(i+1+len(FS0)+len(FS1)+len(FS2)+len(FM0)) + "/" + str(total) + "] FM1:" + str(FM1[i])+"\n")
  if(FM1[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__FM1_m"+"{:1.2g}".format(math.fabs(FM1[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__FM1_p"+"{:1.2g}".format(math.fabs(FM1[i]))+"\n")
  file1.write(L[0])
  file1.write(L[1])
  file1.write(L[2])
  file1.write(L[3])
  file1.write("set anoinputs 5 " + str(FM1[i]) + " # FM1\n")
  file1.write(L[5])
  file1.write(L[6])
  file1.write(L[7])
  file1.write(L[8])
  file1.write(L[9])
  file1.write(L[10])
  file1.write(L[11])
  file1.write(L[12])
  file1.write(L[13])
  file1.write(L[14])
  file1.write(L[15])
  file1.write(L[16])
  file1.write(L[17])
  file1.write(L[18])
  file1.write(L[19])
  file1.write(L[20])

for i in range(0, len(FM2)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(i+1+len(FS0)+len(FS1)+len(FS2)+len(FM0)+len(FM1)) + "/" + str(total) + "] FM2:" + str(FM2[i])+"\n")
  if(FM2[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__FM2_m"+"{:1.2g}".format(math.fabs(FM2[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__FM2_p"+"{:1.2g}".format(math.fabs(FM2[i]))+"\n")
  file1.write(L[0])
  file1.write(L[1])
  file1.write(L[2])
  file1.write(L[3])
  file1.write(L[4])
  file1.write("set anoinputs 6 " + str(FM2[i]) + " # FM2\n")
  file1.write(L[6])
  file1.write(L[7])
  file1.write(L[8])
  file1.write(L[9])
  file1.write(L[10])
  file1.write(L[11])
  file1.write(L[12])
  file1.write(L[13])
  file1.write(L[14])
  file1.write(L[15])
  file1.write(L[16])
  file1.write(L[17])
  file1.write(L[18])
  file1.write(L[19])
  file1.write(L[20])

for i in range(0, len(FM6)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(i+1+len(FS0)+len(FS1)+len(FS2)+len(FM0)+len(FM1)) + "/" + str(total) + "] FM6:" + str(FM6[i])+"\n")
  if(FM6[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__FM6_m"+"{:1.2g}".format(math.fabs(FM6[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__FM6_p"+"{:1.2g}".format(math.fabs(FM6[i]))+"\n")
  file1.write(L[0])
  file1.write(L[1])
  file1.write(L[2])
  file1.write(L[3])
  file1.write(L[4])
  file1.write(L[5])
  file1.write(L[6])
  file1.write(L[7])
  file1.write(L[8])
  file1.write("set anoinputs 10 " + str(FM6[i]) + " # FM6\n")
  file1.write(L[10])
  file1.write(L[11])
  file1.write(L[12])
  file1.write(L[13])
  file1.write(L[14])
  file1.write(L[15])
  file1.write(L[16])
  file1.write(L[17])
  file1.write(L[18])
  file1.write(L[19])
  file1.write(L[20])

for i in range(0, len(FM7)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(i+1+len(FS0)+len(FS1)+len(FS2)+len(FM0)+len(FM1)+len(FM6)) + "/" + str(total) + "] FM7:" + str(FM7[i])+"\n")
  if(FM7[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__FM7_m"+"{:1.2g}".format(math.fabs(FM7[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__FM7_p"+"{:1.2g}".format(math.fabs(FM7[i]))+"\n") 
  file1.write(L[0])
  file1.write(L[1])
  file1.write(L[2])
  file1.write(L[3])
  file1.write(L[4])
  file1.write(L[5])
  file1.write(L[6])
  file1.write(L[7])
  file1.write(L[8])
  file1.write(L[9])
  file1.write("set anoinputs 11 " + str(FM7[i]) + " # FM7\n")
  file1.write(L[11])
  file1.write(L[12])
  file1.write(L[13])
  file1.write(L[14])
  file1.write(L[15])
  file1.write(L[16])
  file1.write(L[17])
  file1.write(L[18])
  file1.write(L[19])
  file1.write(L[20])

for i in range(0, len(FT0)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(i+1+len(FS0)+len(FS1)+len(FS2)+len(FM0)+len(FM1)+len(FM6)+len(FM7)) + "/" + str(total) + "] FT0:" + str(FT0[i]) + "\n")
  if(FT0[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__FT0_m"+"{:1.2g}".format(math.fabs(FT0[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__FT0_p"+"{:1.2g}".format(math.fabs(FT0[i]))+"\n")
  file1.write(L[0])
  file1.write(L[1])
  file1.write(L[2])
  file1.write(L[3])
  file1.write(L[4])
  file1.write(L[5])
  file1.write(L[6])
  file1.write(L[7])
  file1.write(L[8])
  file1.write(L[9])
  file1.write(L[10])
  file1.write("set anoinputs 12 " + str(FT0[i]) + " # FT0\n")
  #file1.write("set anoinputs 12 " + "%1.3g" % FT0[i] + " # FT0\n")
  #file1.write("set anoinputs 12 " + "{:1.3g}".format(FT0[i]) + " # FT0\n")
  file1.write(L[12])
  file1.write(L[13])
  file1.write(L[14])
  file1.write(L[15])
  file1.write(L[16])
  file1.write(L[17])
  file1.write(L[18])
  file1.write(L[19])
  file1.write(L[20])

for j in range(0, len(FT1)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(j+1+len(FS0)+len(FS1)+len(FS2)+len(FM0)+len(FM1)+len(FM6)+len(FM7)+len(FT0)) + "/" + str(total) + "] FT1:" + str(FT1[j])+"\n")
  if(FT1[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__FT1_m"+"{:1.2g}".format(math.fabs(FT1[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__FT1_p"+"{:1.2g}".format(math.fabs(FT1[i]))+"\n")
  file1.write(L[0])
  file1.write(L[1])
  file1.write(L[2])
  file1.write(L[3])
  file1.write(L[4])
  file1.write(L[5])
  file1.write(L[6])
  file1.write(L[7])
  file1.write(L[8])
  file1.write(L[9])
  file1.write(L[10])
  file1.write(L[11])
  file1.write(L[12])
  file1.write("set anoinputs 13 " + str(FT1[j]) + " # FT1\n")
  file1.write(L[14])
  file1.write(L[15])
  file1.write(L[16])
  file1.write(L[17])
  file1.write(L[18])
  file1.write(L[19])
  file1.write(L[20])

for j in range(0, len(FT2)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(j+1 + len(FS0)+len(FS1)+len(FS2)+len(FM0)+len(FM1)+len(FM6)+len(FM7)+len(FT0)+len(FT1)) + "/" + str(total) + "] FT2:" + str(FT2[j])+"\n")
  if(FT2[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__FT2_m"+"{:1.2g}".format(math.fabs(FT2[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__FT2_p"+"{:1.2g}".format(math.fabs(FT2[i]))+"\n")
  file1.write(L[0])
  file1.write(L[1])
  file1.write(L[2])
  file1.write(L[3])
  file1.write(L[4])
  file1.write(L[5])
  file1.write(L[6])
  file1.write(L[7])
  file1.write(L[8])
  file1.write(L[9])
  file1.write(L[10])
  file1.write(L[11])
  file1.write(L[12])
  file1.write(L[13])
  file1.write("set anoinputs 14 " + str(FT2[j]) + " # FT2\n")
  file1.write(L[15])
  file1.write(L[16])
  file1.write(L[17])
  file1.write(L[18])
  file1.write(L[19])
  file1.write(L[20])

file1.write("\n")
file1.write("#Standard Model\n")
file1.write("launch --rwgt_name=EFT__SM\n")
for k in range(0, len(L)):
  file1.write(L[k])
