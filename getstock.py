def main():

     print("hello world1234")

class Stock(): 
     종목코드 = None
     종목명 = None
     현재가 = None
     시가총액 = None
     PER = None
     
     def evaluate(self):
        ret = f"종목코드:{self.종목코드}, 종목명:{self.종목명}, 현재가:{self.현재가}, 시가총액:{self.시가총액}, PER:{self.PER}"
        print(ret)

def getStock():
    
    f=open("stock.csv", "rt", encoding='UTF8') #UTF-8 한글 처리

    ret =[]
    
    for i, line in enumerate(f.readlines()):
        if i ==0:
           continue 
    
        r1 = line.strip()
        r2 = r1.split(',')

        s = Stock()

        s.종목코드 = r2[0]
        s.종목명 = r2[1]
        s.현재가 = r2[2]
        s.시가총액 = r2[3]
        s.PER = r2[4]
   
        s.evaluate()
        ret.append(s)


    return ret

if __name__ == "__main__":
    main()
    # ex3()
    # ex4()
    # ex5()
    # ex12()
    items = getStock()

    for item in items:
        print(item.종목코드, item.종목명, item.현재가, item.시가총액, item.PER) 