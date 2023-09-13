def summ(f):
    carry=0
    ss=[]
    for i in range(0,16,1):
        s=int(f[0][i])+int(f[1][i])+carry
        if s==0:
            ss.append('0')
        elif s==1:
            ss.append('1')
            if carry==1:
                carry=0
        elif s==2:
            ss.append('0')
            carry=1
        elif s==3:
            ss.append('1')
            carry=1
    while(carry!=0):
        for i in range(0,16,1):
            s=int(ss[i])+carry
            if s==int(ss[i]):
                break
            if s==1:
                ss[i]='1'
                if carry==1:
                    carry=0
            if s==2:
                ss[i]='0'
                carry=1
    return ss

def checksum(text):
    ascii_values = []
    flag=0
    for character in text:
        ascii_values.append(ord(character))
    for i in ascii_values:
            f=[]
            while i!=0:
                i=int(i)
                f.append(str(i%2))
                i/=2
                i=int(i)
            f.append('0')
            if flag==0:
                binary_vals=list(f)
                flag=1
            else:
                binary_vals+=f
    return binary_vals

def calculate_checksum(f):
    sum=[['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0']]
    count=0
    for  i in f:
        if len(i)==2:
            sum.append(checksum(i))
            count+=1
    if count==2:
        s=list(sum[1:3])
        s=summ(s)
        s=''.join(s)
        return(s)
    elif count==1:
        return(''.join(sum[1]))
    else:
        return(''.join(sum[0]))