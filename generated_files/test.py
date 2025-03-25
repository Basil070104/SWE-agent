def count_vowels(sentence): 
    
    vowels = "aeiouAEIOU"
    return sum(1 for char in sentence if char in vowels)

if __name__ == "__main__":
    import sys
    sentence = " ".join(sys.argv[1:])
    print(count_vowels(sentence))
