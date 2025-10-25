def main():

     print("hello world1234")
def ex3():
     s1="hello 123 world"
     num = s1[6:9]
     print(num)

     r = len(s1)
     print(r) 
def ex4():
     s4="   hello 123 world  \n"
     r1 = len(s4)
     r2 = len(s4.strip())

     print(r1) 
     print(r2) 
def ex5(): 
     rec="홍길동,100,95,88"

     item=rec.split(",")
     print("="*10)
     print("이름: ", item[0])
     print("국어: ", item[1])
     print("영어: ", item[2])
     print("수학: ", item[3])
     print("="*10)    
def ex6(): 
     name="조홍선"

     age=32
     s= f"{name}의 나이는{age}입니다"
     print(s)

class stock(): 
     종목코드 = None
     회사명 = None
     현재가 = None
     거래량 = None
     예측 = None
     
     def evaluate(self):
        ret = f"종목코드:{self.종목코드}, 회사명:{self.회사명}, 현재가: {self.현재가}, 거래량: {self.거래량}, 예측:{self.예측}"
        print(ret)

def ex7(): 
    a = 5
    b = 'hello'
    
    c = stock() 
    c.종목코드 = '005910'
    c.회사명 = '삼성전자'
    c.혐재가 = 91000
    c.거래량 = 1000000
    c.예측 = 1 

    d = stock() 
    d.종목코드 = '000660'
    d.회사명 = 'SK하이닉스'
    d.혐재가 = 130000
    d.거래량 = 5000000
    d.예측 = 0 

    c.evaluate()
    d.evaluate()


if __name__ == "__main__":
      main()
    # ex3()
    # ex4()
    # ex5()
      ex7()