import os
import sys
import re

aqcm_data = sys.argv[1]
output_name = sys.argv[2]


output = open(output_name , "w")

output.write('<qcm>\n')

for i in xrange(1,31):
    f = "%s/%d.qcm" %(aqcm_data,i)
    print "opening %s" %f

    chap = open(f, "r")

    qid = None
    qbody = None
    qans = []

    state = -1

    for line in chap.readlines():
        m = None
        line = line.strip()
        if line == "":
            continue
        
        m = re.match("\[(\d+)\]", line)
        if m != None:
            print "[%s] is a qid" %line
            if state == -1:
                pass
            elif state == 1 :
                output.write('<question id="%d" chapter="%d">\n' %(qid, i))
                output.write('\t<body>\n')
                output.write(qbody)
                output.write('\n\t</body>\n')
                for ans,score in qans:
                    output.write('\t<answer score="%d">\n' %score)
                    output.write(ans)
                    output.write('\n\t</answer>\n')
                output.write('</question>\n')

                qid = None
                qans = []
                qbody = None
                
            qid = int(m.group(1))
            state = 0
            print "qid is %d" %qid
            continue

        m = re.match("Question=(.*)", line)
        if m != None:
            qbody = m.group(1)
            continue

        m = re.match("(.*)=(.*)", line)
        if m != None:
            qans += [(m.group(1), int(m.group(2)))]
            state = 1
            continue

        print "error with line [%s]" %line
    
output.write('\n</qcm>\n')
