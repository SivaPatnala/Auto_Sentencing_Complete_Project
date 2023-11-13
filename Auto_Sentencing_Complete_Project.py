import tkinter as tk
from tkinter import scrolledtext  # graphical user interface

import nltk  # Natural language toolkit
nltk.download('punkt') 

import re   #regular expression

import random  # generating random integers or String in Python

import requests # Making HTTP requests

from bs4 import BeautifulSoup  #Pulling data out of HTML and XML files

from sklearn.feature_extraction.text import TfidfVectorizer #Convert a collection of raw documents to a matrix of TF-IDF features

from sklearn.metrics.pairwise import cosine_similarity  #To finding the similar words



# creating the class for  Auto sentence complete
# Here we use the tkinter package
class AutoSentenceComplete:
    #__init__(self) This self represents the object of the class itself
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Sentence App") # Mention the tittle

        self.title_label = tk.Label(root, text="Enter the title:")  #creating the label for interface
        self.title_label.pack()

        self.title_entry = tk.Entry(root)  #Adding to the main root
        self.title_entry.pack()

        self.text_label = tk.Label(root, text="Enter the starting word or phrase:") # creating the label for interface
        self.text_label.pack()

        self.text_entry = tk.Entry(root) #Adding to the main root
        self.text_entry.pack()

        self.output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=150, height=35,font=("Arial",10)) # Scroll box for the output sentence
        self.output_text.pack()

        # Configure the tag for left alignment
        self.output_text.tag_configure("left", justify='left')
        
        # Creating the generate button
        self.generate_button = tk.Button(root, text="Generate", command=self.generate_text)
        self.generate_button.pack()


    #Give the access to the interface
    def generate_text(self):
        
        topic = self.title_entry.get()  # From the interface collecting the title input
        
        given_word = self.text_entry.get()  # From the interface collecting the given sentence input


        # Function for getting information for our need
        # Using the request and BeautifulSoup
        
        def web_scrap (x):
            
            x=re.sub("\s","_",x)
            
            url="https://en.wikipedia.org/wiki/"+str(x) # Using the wikipedia
            
            response= requests.get(url)
            
            soup = BeautifulSoup(response.text,'html.parser')
            
            #You're probably treating a list of elements like a single element
            dataset=[]
            
            for i in soup.find_all("p"):  # ("p")paragraph in the  html text
                
                data=i.get_text()
                
                dataset.append(data)
                
            return str(dataset)
        
        # For join the many dictionary in one dictionary
        def merge(dict1,dict2,dict3,dict4,dict5,dict6):
                max=dict1,dict2,dict3,dict4,dict5,dict6
                for i in max:
                    dict1.update(i)
                return dict1

            
        #Creating dictionary for n-grams from using the scrapped information from the web
        def n_grams(token):
                
                # 1 gram words
                monogram={}
                for i in range(len(token)-1):
                    token1,token2=token[i],token[i+1]
                    gram_key=(token1)
                    if gram_key not in monogram:
                        monogram[gram_key]=[token2]
                    elif token2 not in monogram[gram_key]:
                            monogram[gram_key] += [token2]
                # 2 gram words
                digram={}
                for i in range(len(token)-2):
                    token1,token2,token3=token[i],token[i+1],token[i+2]
                    gram_words=(token1,token2)
                    if gram_words not in digram:
                        digram[gram_words]=[token3]
                    elif token3 not in digram[gram_words]:
                        digram[gram_words] += [token3]

                #3 gram words
                trigram={}
                for i in range(len(token)-3):
                    token1,token2,token3,token4=token[i],token[i+1],token[i+2],token[i+3]
                    gram_words=(token1,token2,token3)
                    if gram_words not in trigram:
                        trigram[gram_words]=[token4]

                    elif token4 not in trigram[gram_words]:
                        trigram[gram_words]+=[token4]

                # 4 gram words
                fourgram={}
                for i in range(len(token)-4):
                    token1,token2,token3,token4,token5=token[i],token[i+1],token[i+2],token[i+3],token[i+4]
                    gram_words=(token1,token2,token3,token4)
                    if gram_words not in fourgram:
                        fourgram[gram_words]=[token5]
                    elif token5 not in fourgram[gram_words]:
                            fourgram[gram_words] += [token5]
                # 5 gram word
                fivegram={}
                for i in range(len(token)-5):
                    token1,token2,token3,token4,token5,token6=token[i],token[i+1],token[i+2],token[i+3],token[i+4],token[i+5]
                    gram_words=(token1,token2,token3,token4,token5)
                    if gram_words not in fivegram:
                        fivegram[gram_words]=[token6]
                    elif token5 not in fivegram[gram_words]:
                        fivegram[gram_words]+=[token6]

                #Creating the empty dictionary for join every grams dictionary Using merge function
                grams={}
                merge(grams,monogram,digram,trigram,fourgram,fivegram)
                return grams
            

        # For getting the most popular information using the string similarity
        # Here we using the TfidfVectorizer and cosine_similarity package
        
        def string_similar(corpus,input_phrase):
            
                dataset=nltk.sent_tokenize(corpus)
                
                # Tokenize and preprocess the data
                tfidf_vectorizer = TfidfVectorizer()
                tfidf_matrix = tfidf_vectorizer.fit_transform(dataset)

                # Transform the input phrase into a TF-IDF vector
                input_vector = tfidf_vectorizer.transform([input_phrase])
                
                # Calculate cosine similarity
                cosine_similarities = cosine_similarity(input_vector, tfidf_matrix)
                
                # Create a list of (sentence, similarity) pairs
                similarity_scores = list(enumerate(cosine_similarities[0]))
                
                # Sort the list by similarity scores in descending order
                sorted_similarities = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
                
                # Filter suggestions based on a threshold (e.g., 0.3)
                threshold = 0.3
                filtered_suggestions = [dataset[i] for i, score in sorted_similarities if score >= threshold]
                
                return filtered_suggestions


        # Function for prediciting the next word using n-grams
        def next_word(word,grams):
                word=tuple(word)
                if len(word)==1:
                    word=word[0]
                    if word in grams:
                        next_word=grams[word]
                        return next_word
                    else:
                        return []

        # Function for final output sentence
        # Here we are using the random package
        def sentence_complete(input_sent,grams,dataset_sent,final_sent=[]):
            while final_sent==[]:
                    words=input_sent.split()
                    
                    #Reverse the loop number for want input sentence reversly to check the n-grams
                    for i in range(len(words)-1,-1,-1):
                        last_word=words[i:len(words)]   # It will take the given sentence from the last to first
                        
                        next_words=next_word(last_word,grams) # It will check the word whether it is present in the n-grams dictionary
                        
                        if next_words==[]: # if it is empty than skip current ilteration
                            continue
                        
                        else:
                            if len(next_words) > 0: #If have any values then it will work
                                
                                suggestion = random.choice(next_words) # If it have more than one words than it will choose the one word
                                
                                update_sentence= input_sent + " " + suggestion
                                
                                final_sent=string_similar(dataset_sent,update_sentence) # Here it will check the similarity
                                
                                if len(final_sent) >0:
                                    return update_sentence +" "+" ".join(final_sent) # if have any sentence than it will return
                                
                                input_sent=update_sentence # otherwise it will take the updated sentence for next ilteration

       

        
        # Data preprocessing for model
        # Here re package
        dataset = web_scrap(topic) # Here we using the function for web scrap
        
        dataset = dataset.lower()
        dataset_sent = dataset
        dataset = re.sub("\s+", " ", dataset) 
        dataset = re.sub("\d+", " ", dataset)
        dataset = re.sub("\W+", " ", dataset)
        dataset = re.sub(" n ", " ", dataset)
        dataset = re.sub("\s+", " ", dataset)

        token = nltk.word_tokenize(dataset) # Tokenizing the dataset 

        # It will use for seperate data cleaning for string similarity
        dataset_sent=re.sub('\s+'," ",dataset_sent) 
        dataset_sent=re.sub('[.]',"SPACE ",dataset_sent)
        dataset_sent=re.sub('\d+'," ",dataset_sent)
        dataset_sent=re.sub('\W+'," ",dataset_sent)
        dataset_sent=re.sub(' n ',"",dataset_sent)
        dataset_sent=re.sub('SPACE',".",dataset_sent)
        dataset_sent=re.sub('\s+'," ",dataset_sent)

        # Here we use the function n-gram
        grams= n_grams(token)

        # Here we use the function sentence complete
        generated_sentence=sentence_complete(given_word,grams,dataset_sent)
        
        # Update the output text widget with the generated sentence
        Generated_sentence = "Generated sentence: "+ given_word + ". "+" ".join(generated_sentence)
        
        # Add the generated sentence with the 'left' tag for left alignment
        self.output_text.insert(tk.END, Generated_sentence + "\n\n", "left")

if __name__ == "__main__":  # If we close the interface the loop will stop
    root = tk.Tk()
    app = AutoSentenceComplete(root)
    root.mainloop()
