from subprocess import call
call('dasgoclient --query="dataset dataset=/*/*Summer20UL*/NANOAODSIM" > ULSamples.txt', shell=True)
call('cut -f1-2 -d"/" ULSamples.txt > ProcessedULSamples.txt', shell=True)
call('cut -c-20 ProcessedULSamples.txt > FurtherProcessedULSamples.txt', shell=True)
call('cut -c-20 Samples2018.txt > ProcessedSamples2018.txt', shell=True)

with open('FurtherProcessedULSamples.txt', 'r') as file1:
    with open('ProcessedSamples2018.txt', 'r') as file2:
        same = set(file1).intersection(file2)

same.discard('\n')

with open('samplesdone.txt', 'w') as file_out:
    for line in same:
        file_out.write(line)

call('grep -f "samplesdone.txt" ULSamples.txt > textFileForDASQuery.txt', shell=True)
appendText1='dasgoclient -query=\"summary dataset='
appendText2='\"'
lines = open("textFileForDASQuery.txt", 'r')
finalFile = open('FinalFile.sh', 'w')
for line in lines:
  finalFile.write(appendText1 + line.rstrip() + appendText2 + '\n')
finalFile.close()

inputlines = open('FinalFile.sh', 'r')
call('bash FinalFile.sh > OutputOfDAS.txt', shell=True)
"""
outputlines = open('OutputOfDAS.txt', 'r')
outputInfo = open('TableForTalk.txt', 'w')
for inputline in inputlines:
  print inputline 
  for outputline in outputlines:
    print outputline
    outputInfo.write(inputline + ' SUMMARY : ' + outputline + '\n')
outputInfo.close()
"""
call('paste FinalFile.sh OutputOfDAS.txt > TableForTalk.txt', shell=True) 
