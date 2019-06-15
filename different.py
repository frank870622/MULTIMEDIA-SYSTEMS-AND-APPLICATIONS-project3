hit = 0;
miss= 0;

f = open("F74056166.csv", encoding='utf-8')
g = open("q500ans.txt", encoding='utf-8')

for i in range(1,501):
    line1 = f.readline()
    line2 = g.readline()
    if(line1 == line2):
       hit += 1
    else:
        miss+=1

print("hit: " + str(hit))
print("miss: " + str(miss))
print(str(hit/(miss+hit)))