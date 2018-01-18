#一行Python代码


#------------------------------------------冒泡排序
array = [1,2,5,3,6,8,4]
for i in range(len(array)-1,0,-1):
	print i
	for j in range(0,i):
		print j
		if array[j] > array[j+1]:
			array[j],array[j+1] = array[j+1],array[j]
print array

#斐波那契数列
print [x[0] for x in [  (a[i][0], a.append((a[i][1], a[i][0]+a[i][1]))) for a in ([[1,1]], ) for i in xrange(100) ]]


#素数
print(*(i for i in range(2, 1000) if all(tuple(i%j for j in range(2, int(i**.5))))))

#阶乘
reduce ( lambda x,y:x*y,  range(1,input()+1))

#摄氏度与华氏度之间转换
print((lambda i:i not in [1,2] and "Invalid input!" or i==1 and (lambda f:f<-459.67 and "Invalid input!" or f)(float(input("Please input a Celsius temperature:"))*1.8+32) or i==2 and (lambda c:c<-273.15 and "Invalid input!" or c)((float(input("Please input a Fahrenheit temperature:"))-32)/1.8))(int(input("1,Celsius to Fahrenheit\n2,Fahrenheit to Celsius\nPlease input 1 or 2\n"))))

#9*9口诀
print '\n'.join([' '.join(['%s*%s=%-2s' % (y,x,x*y) for y in range(1,x+1)]) for x in range(1,10)])

#获取外网ip
python -c "import socket; sock=socket.create_connection(('ns1.dnspod.net',6666)); print sock.recv(16); sock.close()"

python -c "import this"

python -m pyftpdlib

import antigravity

#心形状图片
print'\n'.join([''.join([('AndyLove'[(x-y)%8]if((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3<=0 else' ')for x in range(-30,30)])for y in range(15,-15,-1)])


"".join((lambda x:(x.sort(),x)[1])(list(‘string’)))
qsort = lambda arr: len(arr) > 1 and  qsort(filter(lambda x: x<=arr[0], arr[1:] )) + arr[0:1] + qsort(filter(lambda x: x>arr[0], arr[1:] )) or arr
