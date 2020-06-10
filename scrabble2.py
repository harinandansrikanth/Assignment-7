# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 23:43:29 2020

@author: harin
"""

"""
Created on Mon Jun  8 22:48:32 2020

@author: harin
"""

from itertools import permutations, product
import string
import sys

sys.setrecursionlimit(10**6)

file = open("sowpods.txt","r")
txt = file.readlines()
sowpods = []
for i in range(len(txt)):
    sowpods.append((txt[i].replace("\n","")).lower())

if len(sys.argv) > 1:
    input_scr = sys.argv[1]
else:
    input_scr = input("Enter scr_word,let1,pos1,let2,pos2...: ")


split_lst = input_scr.split(",")
input_list = split_lst[1:]
input_string = split_lst[0]


class Scrabble:
    """The objects in this class simulate the game Scrabble."""
    
    scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2, "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3, "l": 1, 
              "o": 1, "n": 1, "q": 10, "p": 3, "s": 1, "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4, "x": 8, "z": 10, 
              "*": 0}
    
    def __init__(self, word, input_list = [],points = 0):
        """Initializer"""
        
        
        if len(word) != 7:
            raise Exception("You must pick a string of length 7.")
        for char in word.lower():
            if char not in Scrabble.scores:
                raise Exception("You must use valid Scrabble characters.")
        if word.count("*") > 2:
            raise Exception("There are only two wildcards in the game.")
        self.points = points
        self.word = word
        self.input_list = input_list
    
    def final_list(self):
        """Returns a list of all possible strings that can be created from the selected Scrabble pieces."""
        
        w = self.word.lower()
        perm_list = []
        for i in range(2,len(w)+1):
            perm_list.append(list(permutations(w,r=i)))
        pre_scr_list = []
        for perm in perm_list:
            for word in perm:
                pre_scr_list.append("".join(word))
        scr_list = []
        for word in pre_scr_list:
            if word not in scr_list:
                scr_list.append(word)
        fin_list = []
        for word in scr_list:
            if "*" not in word:
                if word in sowpods:
                    fin_list.append(word)
            else:
                fin_list.append(word)        
        return fin_list
    
    def final_list_2(self):
        """Returns a list of the strings in final_list(self) that are valid Scrabble words in SOWPODS."""
        
        fin_list = Scrabble.final_list(self)
        letters = string.ascii_lowercase
        letters_sq = list(product(string.ascii_lowercase,repeat=2))
        
        counter = 0
        for word in fin_list:
            if word.count("*") == 1:
                for letter in letters:
                    if word.replace('*',letter) in sowpods:
                        break
                    else:
                        counter += 1                
            if word.count("*") == 2:
                for letter1, letter2 in letters_sq:
                    if word.replace("*",letter1,1).replace("*",letter2) in sowpods:
                        break
                    else:
                        counter += 1
            if (counter == 26) | (counter == 26*26):
                fin_list.remove(word)
            counter = 0
        return(fin_list)           
    
    def score_list(self):
        """Returns a list of the scores corresponding to the words in final_list_2."""
        
        fl_2 = Scrabble.final_list_2(self)
        scores_list = []
        for word in fl_2:
            for char in word:
                self.points += Scrabble.scores[char]
            scores_list.append(self.points)
            self.points = 0
        return scores_list
    
    def display(self):
        """Prints a table of the sorted scores from score_list(self) and Scrabble words from final_list_2."""
        """This function also handles user provided characters assigned to a their position in the"""
        """scarbble word.  Thus the function down selects the list for a given user provided character"""
        """and position list"""
        
        fin_list = Scrabble.final_list_2(self)
        scores_list = Scrabble.score_list(self)
        
        if len(self.input_list) > 0:
            select_word_list = []
            select_score_list = []
            for i in range(int(len(self.input_list)/2)):
                select_letter = self.input_list[2*i]
                select_pos = int(self.input_list[(2*i)+1])-1
                if len(scores_list) > 0:
                    for j in range(len(scores_list)):
                        if len(fin_list[j]) > select_pos:
                            if (fin_list[j][select_pos] == select_letter.lower()):
                                select_word_list.append(fin_list[j])
                                select_score_list.append(scores_list[j])
                            
                    scores_list = select_score_list
                    fin_list = select_word_list
                    select_word_list = []
                    select_score_list = []
          
        fin_score_tuple = [] 
        for i in range(len(scores_list)):
            fin_score_tuple.append((scores_list[i],fin_list[i]))   
        fin_score_tuple.sort(key=lambda x: x[0],reverse=True)
        for i in range(len(scores_list)):
            print(str(fin_score_tuple[i][0]) + " " + str(fin_score_tuple[i][1]))

print(input_list)
print(input_string)      
scr = Scrabble(input_string,input_list)
scr.display()