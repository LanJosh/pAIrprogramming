#!/usr/bin/env python
"""
A Markov model 
"""

import random

class Markov:
  """ The Markov model to pAIr uses to generate new programs
  """
  def __init__(self, size):
    self.model = {}
    self.size = size

  def generate_model(self, data):
    """
    Generates a Markov model.
    ```data``` is a list of headlines to generate the model from
    ```size``` is the number of words to look back at
    """
    for program in data:
      vocab = program.split()
      if (self.size > len(vocab)):
        continue
      for i in range(len(vocab) - self.size):
        key = ()
        for j in range(self.size):
          key += (vocab[i+j],) 
        if key in self.model:
          self.model[key].append(vocab[i+self.size])
        else:
          self.model[key] = [vocab[i+self.size]] 
  
  def generate_word(self, key):
    if key in self.model:
      return random.choice(self.model[key])
    else:
      # Reached a terminal in the Markov model
      return ""

  def generate_text(self, count, end, seed=None):
    """
    Uses the Markov model to generate text
    ```count``` is the number of words to generate
    """
    if seed is not None:
      key = tuple([seed]) 
    else:
      key = random.choice(self.model.keys())
    i = 0
    text = ""
    for word in list(key):
      text += " " + word
    while (True):
      word = self.generate_word(key)
      if word == "" or word == end:
        return text + " " + word
      text += word + " "
      key = ((list(key))[1:]) 
      key.append(word)
      key = tuple(key)
      i += 1 
    return text 

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
  human_program = input('Enter the program you want to run: ')
  data.append(human_program)
  pAIr = Markov(1)
  pAIr.generate_model(data) 
  print(y.generate_text(50, 'end', seed='program'))

if __name__ == '__main__':
  main()

