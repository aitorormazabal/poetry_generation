# -*- coding: utf-8

import sys

tildes="áéíóú"
nsv="aeiouns"


def hastilde(st):
  return sum([i in tildes for i in st])>0
def hasnsv(st):
  return sum([i in nsv for i in st])>0

def setstress(word):
#  print "Palabra:"+''.join(word).encode("utf8")
  if len(word)==1 and hastilde(word[0]):
    stress=['+']
  elif len(word)==1:
    stress=['?']
  else:
    stress=["-"]*len(word)
    acentuado=[hastilde(i) for i in word]
    if sum(acentuado)>0:
      stress[acentuado.index(True)]="+"
    else:
      lastchar=word[-1][-1]
      if lastchar in nsv:
        stress[-2]="+"
      else:
        stress[-1]="+"
  #print "Acento:"+''.join(stress)
  return stress



