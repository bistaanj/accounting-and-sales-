#input file
fin = open("file.txt", "r")
#output file to write the result to
fout = open("out.txt", "w")
#for each line in the input file
width = 'width'
height = 'height'
font = 'font'
count = 0
count2 = 0
while True:
    line  = fin.readline()
    if not line:
        break
    # w=0
    # h=0
    # f=0
    if width in line:
        w=1
        p1 = line.find(width)
        p2 = line.find(',',p1)
        temp = line[p1:p2]
        temp =temp.replace(')',' ')
        num = ''
        for c in temp:
            if c.isdigit():
                num = num + c
        #print(temp)
        #print(int(num))
        temp3 = 'width = int(WR*'+num+')'
        #print(temp3)
        fout.write(line.replace(temp, temp3))
    
    # if height in line:
    #     h=1
    #     p1 = line.find(height)
    #     p2 = line.find(',',p1)
    #     temp = line[p1:p2]
    #     temp =temp.replace(')',' ')
    #     num = ''
    #     for c in temp:
    #         if c.isdigit():
    #             num = num + c
    #     #print(temp)
    #     #print(int(num))
    #     temp3 = 'height = int(HR*'+num+')'
    #     #print(temp3)
    #     fout.write(line.replace(temp, temp3))

    # if font in line:
    #     f=1
    #     p1 = line.find(font)
    #     p2 = line.find(')',p1)
    #     temp = line[p1:p2]
    #     #temp =temp.replace(')',' ')
    #     num = ''
    #     #print(temp)
    #     for c in temp:
    #         if c.isdigit():
    #             num = num + c

    #     temp4=temp.replace(num, 'int(FR*'+num+')')
    #     #print(num)
    #     #print(temp4)
    #     #print(temp)
    #     #print(int(num))
    #     #temp3 = 'width = int(WR*'+num+')'
    #     #print(temp3)
    #     fout.write(line.replace(temp, temp4))
    else:
        fout.write(line)

#print(count2+count)
#read replace the string and write to output file
#close input and output files
fin.close()
fout.close()
