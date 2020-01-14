import numpy as np


#phone encoder



class PhoneCode:

    def __init__(self):
        self.phone_list = [
              "b",  #as in bug
              "d",  #as in dad
              "f",  #as in fat
              "g",  #as in gas
              "h",  #as in jop
              "dz"  #somewhere between dj and dz, as in jam,, wage
              "k",  #as in kill, kit
              "l",  #as in live
              "m",  #as in man
              "n",  #as in net
              "p",  #as in pit, puppy
              "r",  #as in run
              "s",  #as in sit
              "t",  #as in tip
              "v",  #as in vine, five
              "w",  #as in wit, qUIck
              "z",  #as in zed, buzz
              "zh", #as in teaSure, diviSion
              "ch"  #as in CHip, watCH
              "sh", #as in SHam, Sure
              "th", #as in the
              "dh", #as in teaTHer, THee
              "ng", #as in riNG
              "j",  #as in You, halleluJah
              "ae", #as in cat, laugh
              "ei", #as in bey
              "e",  #as in end
              "ii", #as in bee, meat
              "i",  #as in it, england
              "ai", #as in EYe, spIder
              "o",  #as in HOnest
              "ou", #as in open
              "uu", #as in boo, look
              "u",  #as in wolf
              "a",  #as in lug, blood
              "uu", #as in whO, lOOm
              "oi", #as in boy
              "au", #as in now
              "uh", #as in About, honOUR
              "ea", #as in AIr
              "aa", #as in arm
              "rd", #as in bird
              "oo", #as in awe, paw
              "ia", #as in ear
              "ur", #as in cure
              ]

        self.phone_codes = []
        for i in range(len(self.phone_list)):
            self.phone_codes.append("")


    def number_to_binary(self, num):
        string = ""
        string += str(num%2)
        num//=2

        while num > 0:
            string += str(num%2)
            num//=2

        ret = string[::-1]

        #check if the number contains 6 digits
        while len(ret) < 6:
            ret = "0" + ret
        return ret

    def return_phone_list(self):
            return self.phone_list

    def make_default_codes(self):
        for i in range(len(self.phone_list)):
            self.phone_codes[i] = number_to_binary(i)

    def add_code_to_phone(self, phone, code):
        pos = 0
        for i in range(len(self.phone_list)):
            if self.phone_list[i] == phone:
                pos = i
                break

        self.phone_codes[pos] = code



if __name__ == '__main__':
   code = PhoneCode()
   print(code.number_to_binary(3))
   print(code.number_to_binary(4))
   print(code.return_phone_list())
   
   print("The number of phones is", len(code.phone_codes))
