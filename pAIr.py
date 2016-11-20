#!/usr/bin/env python
"""
A Markov model 
"""

import random
import os

class Markov:
  """
  The Markov model to pAIr uses to generate new programs
  """
  def __init__(self, size):
    self.model = {}
    self.size = size

  def generate_model(self, data):
    """
    Generates a Markov model.
    ```data``` is a list of programs to generate the model from
    ```size``` is the number of words to look back at
    """
    for program in data:
      vocab = program.split()
      #Run through each original word in vocab and tokenize, making new words
      newVocab = []
      for pos in range(len(vocab)):
        newWords = []  #list of new words to replace the original word
        chars = list(vocab[pos])  #list of chars in the original word

        newWord = ""
        #Iterates through chars of the original word and separates into new words
        for char in chars:
          #new word goes until a nonalphanumeric char
          if char.isalpha() or char.isdigit():
            newWord += char
          else:
            #Keep track of new words to add
            newWords.append(newWord)
            newWords += char
            newWord = ""
        #Add all new words to new vocab
        if len(newWords) != 0:
          newVocab += newWords

      vocab = newVocab
      
      #Case: Program has less words than the number of words to check
      if (self.size > len(vocab)):
        continue
      #Iterate through each size-tuple of words in the program and make it into a key, then make next word into the value
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
    #Case: start word(s) is given
    if seed is not None:
      key = tuple([seed]) 
    else:
      key = random.choice(self.model.keys())
    i = 0
    text = ""
    #Puts initial words from start word(s) into text
    for word in list(key):
      text += word
    while (True):
      word = self.generate_word(key)
      #Case: Found ending word, returns text
      if word == "" or word == end:
        return text + " " + word
      text += " " + word

      #Makes new key from [1:] of current key and the new word
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

  #Makes list with a program as each element
  def get_experience(self):
    data = []
    for filename in os.listdir(self.directory):
      with open(self.directory + filename) as f:
        data.append(f.read())
    return data

def main():
  exp = Experience('./data/')
  data = exp.get_experience()
  """
  human_program = input('Enter the program you want to run: ')
  data.append(human_program)
  """
  pAIr = Markov(1)
  pAIr.generate_model(data)
  print(pAIr.generate_text(50, 'end', seed='program'))

if __name__ == '__main__':
  main()
