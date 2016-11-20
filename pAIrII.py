#!/usr/bin/env python
"""
A Markov model 
"""

import random
import os
import re

class Markov:
  """ The Markov model to pAIr uses to generate new programs
  """
  def __init__(self, size):
    self.model_struct = {}
    self.model_words = {}
    self.list_ids = []
    self.size = size # [size of the structure chain, 
                     #  size of the expression chain]
    self.program = ('program','begin','end')
    self.cond1 = ('while','endwhile')
    self.cond2 = ('if','else','endif')
    self.declr = ('int',)
    self.oper = ['input','output','or']
    self.varlist = []
    self.text = [[], []]

  def is_program(self,string) :
    r = string.split()
    if len(r) == 0 : return False
    if r[0] == self.program[0] :
      return True
    else :
      return False

  def is_while(self, string) :
    r = string.split()
    if len(r) == 0 : return False
    if r[0] == self.cond1[0] :
      return True
    else :
      return False

  def is_if(self, string) :
    r = string.split()
    if len(r) == 0 : return False
    if r[0] == self.cond2[0] :
      return True
    else :
      return False

  def is_declr(self, string) :
    r = string.strip().split()
    if len(r) == 0 : return False
    if r[0] == self.declr[0] :
      return True
    else :
      return False

  def remo(self, str1, oper) : # remove the operators
    r = str1.strip().split()
    for i in range(len(oper)) :
      if oper[i] in r :
        str1 = str1.replace(oper[i], '#'+str(i)+'#')
    return str1

  def resy(self,str1) : # remove the non-alphanumeric characters
    s = ''.join(c for c in str1 if c.isalnum() or c.isspace()).split()
    s = '#*#'.join(c for c in str1 if not c.isalnum() or c.isspace())
    return s

  def generate_model(self, data):
    """
    Generates a Markov model.
    ```data``` is a list of individual programs to generate the model from
    ```size``` is the number of words to look back at
    """
    for program in data:
      """ Parse the structures
      """
      byline = program.split('\n')
      flow = []
      for line in byline :
        if self.is_program(line) or self.is_declr(line) :
          continue
        if self.is_while(line) :
          flow.append(1)
        if self.is_if(line) :
          flow.append(2)

      if (self.size[0] <= len(flow)) :
        for i in range(len(flow) - self.size[0]):
          key = ()
          for j in range(self.size[0]):
            key += (flow[i+j],)
            if key in self.model_struct:
              self.model_struct[key].append(flow[i+self.size[0]])
            else:
              self.model_struct[key] = [flow[i+self.size[0]]]

      """ Parse the expressions
      """
      flow = []
      for line in byline :
        if not ( self.is_program(line) or self.is_while(line) or self.is_if(line) or self.is_declr(line) ) :
          strpd = self.resy(self.remo(line, self.oper))
          flow.append(strpd)
        if self.is_declr(line) :
          strpd = re.split(r'[;\s,]\s*',line)
          strpd.remove('int')
          self.list_ids.extend( [var for var in strpd if var] )

      if (self.size[1] <= len(flow)) :
        for i in range(len(flow) - self.size[1]):
          key = ()
          for j in range(self.size[1]):
            key += (flow[i+j],)
            if key in self.model_words: 
              self.model_words[key].append(flow[i+self.size[1]])
            else:
              self.model_words[key] = [flow[i+self.size[1]]]

    if len( self.model_struct.keys() ) == 0:
      print('size = '+size+' too large for structures')
    if len( self.model_words.keys() ) == 0:
      print('size = '+size+' too large for words')

  def generate_struct(self, key):
    if key in self.model_struct:
      return random.choice(self.model_struct[key])
    else:
      # Reached a terminal in the Markov model
      return ""

  def generate_word(self, key, varlist):
    if key in self.model_words:
      aword = random.choice(self.model_words[key])
      aword.split('#')
      for i in range(len(aword)) :
        if aword[i] == '0' :
          aword[i] = 'input'
        elif aword[i] == '1' :
          aword[i] = 'output'
        elif aword[i] == '2' :
          aword[i] = 'or'
        elif aword[i] == '*' :
          aword[i] = random.choice(varlist)
      return aword
    else:
      # Reached a terminal in the Markov model
      return ""

  def generate_header(self, count):
    """
    ```count``` is the number of variables to declare
    """
    self.varlist = random.sample(self.list_ids, count)

  def generate_text(self, count, seed=None):
    """
    Uses the Markov model to generate text
    ```count``` is the number of lines to generate between 'begin''end'
    """
    if seed is not None:
      key = seed
      key2 = random.choice(list(self.model_words.keys()))
    else:
      key = random.choice(self.model_struct.keys())
      key2 = random.choice(self.model_words.keys())
    """
    Generate the structures and expressions inside
    """
    i = 0
    nstrct = 0
    while (i < count):
      astruct = self.generate_struct(key)
      if astruct == "" :
        break; 
      if (i + astruct + 1 < count) :
        self.text[0].append(astruct)
        nstrct += 1
        i += astruct + 1
        self.text[1].append([])
        arbitrary = random.randint(i, count)

        for j in range(arbitrary-i) :
          nextword = self.generate_word(key2, self.varlist)
          self.text[1][nstrct-1].append(nextword)
          i += 1
          key2 = nextword
          print(key2)
      else :
        break
      key = astruct

      #if (self.text[0][-1] == 1 or self.text[0][-1] == 2) :
      #  self.text[1].append(self.generate_cond(key, varlist))
      #else :

  def write_program(self, filename):
    """
    Parse the text and write to a program
    """
    try :
      f = open(filename, 'w')
    except :
      print('File '+filename+' cannot be opened')
      exit()
    f.write('program\n')
    for i in self.varlist :
      f.write('    int '+i+';\n')
    f.write('begin\n')
    for i in range(len(self.text[0])) :
      if (self.text[0][i] == 1) :
        f.write(self.cond1[0])
      elif (self.text[0][i] == 2) :
        f.write(self.cond2[0])

      for j in range(len(self.text[1][i])) :
        f.write(self.text[1][i][j] + '\n')

      # ??? 'if then 'while begin'
      if (self.text[0][i] == 1) :
        for j in self.cond1[1:] :
          f.write(j + '\n')
      elif (self.text[0][i] == 2) :
        for j in self.cond2[1:] :
          f.write(j + '\n')

    f.write('end\n')

class Experience:
  """ The super legit h4xx0r experience pAIr has accumulated over the years.
  Gets a few valid core programs and formats them for the Markov model
  """

  def __init__(self, directory):
    """ ```directory``` is the directory the core programs reside in
    """
    self.directory = directory

  def get_experience(self):
    data = []
    for filename in os.listdir(self.directory):
      with open(self.directory + filename) as f:
        data.append(f.read())
    return data

def main():
  exp = Experience('./data/')
  data = exp.get_experience()
  human_program = input('Enter name of the program you want to generate: ')
  pAIr = Markov([1,1])
  pAIr.generate_model(data) 
  pAIr.generate_header(10)
  pAIr.generate_text(50, seed=(1,))
  pAIr.write_program(human_program)

if __name__ == '__main__':
  main()

