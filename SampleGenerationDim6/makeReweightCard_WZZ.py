import decimal
import math

file1 = open("WZZ_Dim6_cW_cHd_cHWB_cHW_reweight_card.dat","w+")

L = [
"change mode NLO       # Define type of Reweighting. For LO sample this command\n", 
"                      # has no effect since only LO mode is allowed. \n",
"change helicity False # has also been done in the example I got from Kenneth \n"
"change rwgt_dir rwgt\n"]

file1.writelines(L)

L = [
"set SMEFT 2 0 # cW\n",
"set SMEFT 5 0 # cHDD\n", 
"set SMEFT 7 0 # cHW\n",
"set SMEFT 8 0 # cHB\n",
"set SMEFT 9 0 # cHWB\n"
]

cW = [-10.0, -5.0, -1.0, -0.7, -0.5, -0.3, -0.1, -0.05, -0.01, 0.01, 0.05, 0.1, 0.3, 0.5, 0.7, 1.0, 5.0, 10.0]
cHDD = [-100.0, -50.0, -10.0, -7.0, -5.0, -3.0, -1.0, -0.5, -0.1, 0.1, 0.5, 1.0, 3.0, 5.0, 7.0, 10.0, 50.0, 100.0]
cHW = [-10.0, -5.0, -1.0, -0.7, -0.5, -0.3, -0.1, -0.05, -0.01, 0.01, 0.05, 0.1, 0.3, 0.5, 0.7, 1.0, 5.0, 10.0]
cHB = [-100.0, -50.0, -10.0, -7.0, -5.0, -3.0, -1.0, -0.5, -0.1, 0.1, 0.5, 1.0, 3.0, 5.0, 7.0, 10.0, 50.0, 100.0]
cHWB = [-100.0, -50.0, -10.0, -7.0, -5.0, -3.0, -1.0, -0.5, -0.1, 0.1, 0.5, 1.0, 3.0, 5.0, 7.0, 10.0, 50.0, 100.0]

Fname_cW = [-10.0, -5.0, -1.0, -0.7, -0.5, -0.3, -0.1, -0.05, -0.01, 0.01, 0.05, 0.1, 0.3, 0.5, 0.7, 1.0, 5.0, 10.0]
Fname_cHDD_cHB_cHWB = [-100.0, -50.0, -10.0, -7.0, -5.0, -3.0, -1.0, -0.5, -0.1, 0.1, 0.5, 1.0, 3.0, 5.0, 7.0, 10.0, 50.0, 100.0] 

total = len(cW) + len(cHDD) + len(cHW) + len(cHB) + len(cHWB)

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

for i in range(0, len(cHDD)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(i+1+len(cW)) + "/" + str(total) + "] cHDD:" + str(cHDD[i])+"\n")
  if(cHDD[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__cHDD_m"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__cHDD_p"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
  file1.write(L[0])
  file1.write("set SMEFT 5 " + str(cHDD[i]) + " # cHDD\n")
  file1.write(L[2])
  file1.write(L[3])
  file1.write(L[4])

for i in range(0, len(cHW)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(i+1+len(cW)+len(cHDD)) + "/" + str(total) + "] cHW:" + str(cHW[i])+"\n")
  if(cHW[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__cHW_m"+"{:1.2f}".format(math.fabs(Fname_cW[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__cHW_p"+"{:1.2f}".format(math.fabs(Fname_cW[i]))+"\n")
  file1.write(L[0])
  file1.write(L[1])
  file1.write("set SMEFT 7 " + str(cHW[i]) + " # cHW\n")
  file1.write(L[3])
  file1.write(L[4])

for i in range(0, len(cHB)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(i+1+len(cW)+len(cHDD)+len(cHW)) + "/" + str(total) + "] cHB:" + str(cHB[i])+"\n")
  if(cHB[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__cHB_m"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__cHB_p"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
  file1.write(L[0])
  file1.write(L[1])
  file1.write(L[2])
  file1.write("set SMEFT 8 " + str(cHB[i]) + " # cHB\n")
  file1.write(L[4])

for i in range(0, len(cHWB)):
  file1.write("\n")
  file1.write("\n")
  file1.write("#[" + str(i+1+len(cW)+len(cHDD)+len(cHW)+len(cHWB)) + "/" + str(total) + "] cHWB:" + str(cHWB[i])+"\n")
  if(cHWB[i] < 0.0):
    file1.write("launch --rwgt_name=EFT__cHWB_m"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
  else:
    file1.write("launch --rwgt_name=EFT__cHWB_p"+"{:1.2f}".format(math.fabs(Fname_cHDD_cHB_cHWB[i]))+"\n")
  file1.write(L[0])
  file1.write(L[1])
  file1.write(L[2])
  file1.write(L[3])
  file1.write("set SMEFT 9 " + str(cHWB[i]) + " # cHWB\n")

