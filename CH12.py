def main():

     print("hello world1234")

class stock(): 
     종목코드 = None
     회사명 = None
     현재가 = None
     거래량 = None
     예측 = None
     
     def evaluate(self):
        ret = f"종목코드:{self.종목코드}, 회사명:{self.회사명}, 현재가: {self.현재가}, 거래량: {self.거래량}, 예측:{self.예측}"
        print(ret)

def ex12(): 
    f=open("mytext.txt", "rt", encoding='UTF8') #UTF-8 한글 처리
   while True:
    r=f.readline()
    if not r:
        break
    print(r)
# The file closing statement is assumed to follow here, but it's cut off in the image.


if __name__ == "__main__":
      main()
    # ex3()
    # ex4()
    # ex5()
      ex12()