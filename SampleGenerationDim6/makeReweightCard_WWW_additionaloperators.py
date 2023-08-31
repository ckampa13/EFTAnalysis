import decimal
import math

file1 = open("WWW_Dim6_cW_cHd_cHWB_cHW_reweight_card.dat","w+")

L = [
"change mode NLO       # Define type of Reweighting. For LO sample this command\n", 
"                      # has no effect since only LO mode is allowed. \n",
"change helicity False # has also been done in the example I got from Kenneth \n"
"change rwgt_dir rwgt\n"]

file1.writelines(L)

L = [
"set SMEFT 2 0 # cW\n",
"set SMEFT 4 0 # cHbox\n",
"set SMEFT 5 0 # cHDD\n", 
"set SMEFT 7 0 # cHW\n",
"set SMEFT 8 0 # cHB\n",
"set SMEFT 9 0 # cHWB\n",
"set SMEFT 22 0 # cHl3\n",
"set SMEFT 24 0 # cHq1\n",
"set SMEFT 25 0 # cHq3\n",
"set SMEFT 26 0 # cHu\n",
"set SMEFT 27 0 # cHd\n",
"set SMEFT 30 0 # cll1\n"
]

cW = [-10.0, -5.0, -1.0, -0.7, -0.5, -0.3, -0.1, -0.05, -0.01, 0.01, 0.05, 0.1, 0.3, 0.5, 0.7, 1.0, 5.0, 10.0]
cHDD = [-100.0, -50.0, -10.0, -7.0, -5.0, -3.0, -1.0, -0.5, -0.1, 0.1, 0.5, 1.0, 3.0, 5.0, 7.0, 10.0, 50.0, 100.0]
cHW = [-10.0, -5.0, -1.0, -0.7, -0.5, -0.3, -0.1, -0.05, -0.01, 0.01, 0.05, 0.1, 0.3, 0.5, 0.7, 1.0, 5.0, 10.0]
cHB = [-100.0, -50.0, -10.0, -7.0, -5.0, -3.0, -1.0, -0.5, -0.1, 0.1, 0.5, 1.0, 3.0, 5.0, 7.0, 10.0, 50.0, 100.0]
cHWB = [-100.0, -50.0, -10.0, -7.0, -5.0, -3.0, -1.0, -0.5, -0.1, 0.1, 0.5, 1.0, 3.0, 5.0, 7.0, 10.0, 50.0, 100.0]
cHbox= [-100.0, -50.0, -10.0, -7.0, -5.0, -3.0, -1.0, -0.5, -0.1, 0.1, 0.5, 1.0, 3.0, 5.0, 7.0, 10.0, 50.0, 100.0]
cHu  = [-100.0, -50.0, -10.0, -7.0, -5.0, -3.0, -1.0, -0.5, -0.1, 0.1, 0.5, 1.0, 3.0, 5.0, 7.0, 10.0, 50.0, 100.0]
cHd  = [-100.0, -50.0, -10.0, -7.0, -5.0, -3.0, -1.0, -0.5, -0.1, 0.1, 0.5, 1.0, 3.0, 5.0, 7.0, 10.0, 50.0, 100.0]
cHq1 = [-100.0, -50.0, -10.0, -7.0, -5.0, -3.0, -1.0, -0.5, -0.1, 0.1, 0.5, 1.0, 3.0, 5.0, 7.0, 10.0, 50.0, 100.0]
cHq3 = [-100.0, -50.0, -10.0, -7.0, -5.0, -3.0, -1.0, -0.5, -0.1, 0.1, 0.5, 1.0, 3.0, 5.0, 7.0, 10.0, 50.0, 100.0]
cll1 = [-100.0, -50.0, -10.0, -7.0, -5.0, -3.0, -1.0, -0.5, -0.1, 0.1, 0.5, 1.0, 3.0, 5.0, 7.0, 10.0, 50.0, 100.0] 
cHl3 = [-100.0, -50.0, -10.0, -7.0, -5.0, -3.0, -1.0, -0.5, -0.1, 0.1, 0.5, 1.0, 3.0, 5.0, 7.0, 10.0, 50.0, 100.0]

Fname_cW = [-10.0, -5.0, -1.0, -0.7, -0.5, -0.3, -0.1, -0.05, -0.01, 0.01, 0.05, 0.1, 0.3, 0.5, 0.7, 1.0, 5.0, 10.0]
Fname_cHDD_cHB_cHWB = [-100.0, -50.0, -10.0, -7.0, -5.0, -3.0, -1.0, -0.5, -0.1, 0.1, 0.5, 1.0, 3.0, 5.0, 7.0, 10.0, 50.0, 100.0] 

total = len(cW) + len(cHDD) + len(cHW) + len(cHB) + len(cHWB) + len(cHbox) + len(cHu) + len(cHd) + len(cHq1) + len(cHq3) + len(cll1) + len(cHl3)

file1.write("\n")
file1.write("#Standard Model\n")
file1.write("launch --rwgt_name=EFT__SM\n")
for k in range(0, len(L)):
  file1.write(L[k])

for i in range(0, len(cW)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(i+1) + "/" + str(total) + "] cW:" + str(cW[i])+"\n")
  if(cW[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__cW_m"+"{:1.2f}".format(math.fabs(Fname_cW[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__cW_p"+"{:1.2f}".format(math.fabs(Fname_cW[i]))+"\n")
  file1.write("set SMEFT 2 " + str(cW[i]) + " # cW\n")
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

for i in range(0, len(cHbox)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(i+1+len(cW)) + "/" + str(total) + "] cHbox:" + str(cHbox[i])+"\n")
  if(cHbox[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__cHbox_m"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__cHbox_p"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
  file1.write(L[0])
  file1.write("set SMEFT 4 " + str(cHbox[i]) + " # cHbox\n")
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

for i in range(0, len(cHDD)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(i+1+len(cW)+len(cHbox)) + "/" + str(total) + "] cHDD:" + str(cHDD[i])+"\n")
  if(cHDD[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__cHDD_m"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__cHDD_p"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
  file1.write(L[0])
  file1.write(L[1])
  file1.write("set SMEFT 5 " + str(cHDD[i]) + " # cHDD\n")
  file1.write(L[3])
  file1.write(L[4])
  file1.write(L[5])
  file1.write(L[6])
  file1.write(L[7])
  file1.write(L[8])
  file1.write(L[9])
  file1.write(L[10])
  file1.write(L[11])

for i in range(0, len(cHW)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(i+1+len(cW)+len(cHbox)+len(cHDD)) + "/" + str(total) + "] cHW:" + str(cHW[i])+"\n")
  if(cHW[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__cHW_m"+"{:1.2f}".format(math.fabs(Fname_cW[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__cHW_p"+"{:1.2f}".format(math.fabs(Fname_cW[i]))+"\n")
  file1.write(L[0])
  file1.write(L[1])
  file1.write(L[2])
  file1.write("set SMEFT 7 " + str(cHW[i]) + " # cHW\n")
  file1.write(L[4])
  file1.write(L[5])
  file1.write(L[6])
  file1.write(L[7])
  file1.write(L[8])
  file1.write(L[9])
  file1.write(L[10])
  file1.write(L[11])

for i in range(0, len(cHB)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(i+1+len(cW)+len(cHbox)+len(cHDD)+len(cHW)) + "/" + str(total) + "] cHB:" + str(cHB[i])+"\n")
  if(cHB[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__cHB_m"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__cHB_p"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
  file1.write(L[0])
  file1.write(L[1])
  file1.write(L[2])
  file1.write(L[3])
  file1.write("set SMEFT 8 " + str(cHB[i]) + " # cHB\n")
  file1.write(L[5])
  file1.write(L[6])
  file1.write(L[7])
  file1.write(L[8])
  file1.write(L[9])
  file1.write(L[10])
  file1.write(L[11])

for i in range(0, len(cHWB)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(i+1+len(cW)+len(cHbox)+len(cHDD)+len(cHW)+len(cHWB)) + "/" + str(total) + "] cHWB:" + str(cHWB[i])+"\n")
  if(cHWB[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__cHWB_m"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__cHWB_p"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
  file1.write(L[0])
  file1.write(L[1])
  file1.write(L[2])
  file1.write(L[3])
  file1.write(L[4])
  file1.write("set SMEFT 9 " + str(cHWB[i]) + " # cHWB\n")
  file1.write(L[6])
  file1.write(L[7])
  file1.write(L[8])
  file1.write(L[9])
  file1.write(L[10])
  file1.write(L[11])

for i in range(0, len(cHl3)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(i+1+len(cW)+len(cHbox)+len(cHDD)+len(cHW)+len(cHWB)+len(cHl3)) + "/" + str(total) + "] cHl3:" + str(cHl3[i])+"\n")
  if(cHl3[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__cHl3_m"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__cHl3_p"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
  file1.write(L[0])
  file1.write(L[1])
  file1.write(L[2])
  file1.write(L[3])
  file1.write(L[4])
  file1.write(L[5])
  file1.write("set SMEFT 22 " + str(cHl3[i]) + " # cHl3\n")
  file1.write(L[7])
  file1.write(L[8])
  file1.write(L[9])
  file1.write(L[10])
  file1.write(L[11])

for i in range(0, len(cHq1)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(i+1+len(cW)+len(cHbox)+len(cHDD)+len(cHW)+len(cHWB)+len(cHl3)+len(cHq1)) + "/" + str(total) + "] cHq1:" + str(cHq1[i])+"\n")
  if(cHq1[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__cHq1_m"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__cHq1_p"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
  file1.write(L[0])
  file1.write(L[1])
  file1.write(L[2])
  file1.write(L[3])
  file1.write(L[4])
  file1.write(L[5])
  file1.write(L[6])
  file1.write("set SMEFT 24 " + str(cHq1[i]) + " # cHq1\n")
  file1.write(L[8])
  file1.write(L[9])
  file1.write(L[10])
  file1.write(L[11])

for i in range(0, len(cHq3)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(i+1+len(cW)+len(cHbox)+len(cHDD)+len(cHW)+len(cHWB)+len(cHl3)+len(cHq1)+len(cHq3)) + "/" + str(total) + "] cHq3:" + str(cHq3[i])+"\n")
  if(cHq3[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__cHq3_m"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__cHq3_p"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
  file1.write(L[0])
  file1.write(L[1])
  file1.write(L[2])
  file1.write(L[3])
  file1.write(L[4])
  file1.write(L[5])
  file1.write(L[6])
  file1.write(L[7])
  file1.write("set SMEFT 25 " + str(cHq3[i]) + " # cHq3\n")
  file1.write(L[9])
  file1.write(L[10])
  file1.write(L[11])

for i in range(0, len(cHu)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(i+1+len(cW)+len(cHbox)+len(cHDD)+len(cHW)+len(cHWB)+len(cHl3)+len(cHq1)+len(cHq3)+len(cHu)) + "/" + str(total) + "] cHu:" + str(cHu[i])+"\n")
  if(cHu[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__cHu_m"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__cHu_p"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
  file1.write(L[0])
  file1.write(L[1])
  file1.write(L[2])
  file1.write(L[3])
  file1.write(L[4])
  file1.write(L[5])
  file1.write(L[6])
  file1.write(L[7])
  file1.write(L[8])
  file1.write("set SMEFT 27 " + str(cHu[i]) + " # cHu\n")
  file1.write(L[10])
  file1.write(L[11])

for i in range(0, len(cHd)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(i+1+len(cW)+len(cHbox)+len(cHDD)+len(cHW)+len(cHWB)+len(cHl3)+len(cHq1)+len(cHq3)+len(cHu)+len(cHd)) + "/" + str(total) + "] cHd:" + str(cHd[i])+"\n")
  if(cHd[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__cHd_m"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__cHd_p"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
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
  file1.write("set SMEFT 28 " + str(cHd[i]) + " # cHd\n")
  file1.write(L[11])

for i in range(0, len(cll1)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(i+1+len(cW)+len(cHbox)+len(cHDD)+len(cHW)+len(cHWB)+len(cHl3)+len(cHq1)+len(cHq3)+len(cHu)+len(cHd)+len(cll1)) + "/" + str(total) + "] cll1:" + str(cll1[i])+"\n")
  if(cll1[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__cll1_m"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__cll1_p"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
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
  file1.write("set SMEFT 30 " + str(cll1[i]) + " # cll1\n")
