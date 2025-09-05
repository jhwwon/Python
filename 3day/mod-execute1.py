#import mymod.mod2
#from mymod import mod2       #mymod는 파일 혹은 디렉토리, mod2는 파일 혹은 클래스 혹은 함수 
from mymod import mod2 as m2  #별칭(alias) 지정

#result = mymod.mod2.add(3, 4)
#result = mod2.add(3, 4)
result = m2.add(3,4)
print('결과값:',result)
