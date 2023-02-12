#Kyle Mellott

#This program is a Naive Bayesian classifier that performs sentiment analysis on movie reviews.
#The program is trained with training data and then tested using test data, and the results are
#analyzed by a different program.

#The first input after the file name is the unigram frequency cutoff. The 2nd and 3rd inputs
#are file names with the .txt extension included, and are the training and test data, respectively.

#An example of program operation is as follows:
#   In the command prompt:
#   >> Python naive.py 93 sentiment-train.txt sentiment-test.txt
#The unigram cutoff in this example is 93, meaning that only unigrams that occur 93 or more times
#are factored into the training of the program. The output of the program is then stored in a text
#file called results.txt.

#The steps of the program are as follows:
#   The user starts the program via the command prompt, passing in the 3 arguments mentioned previously
#   These arguments are then passed to the main() function. The main function then calls getText, passing
#   in the training data. getText uses file.read() to generate a continuous string of all the data, as well
#   as using file.readlines() to separate each review from the others. It then returns both of these to main.

#   Next, the raw training data is passed to typeCount, which uses a dictionary to determine how many unique
#   types are in the data. The length of this dictionary is returned as the type count.

#   Next, the training data is passed to sentientCheck. Using a regular expression, this function counts the total
#   number of positive and negative reviews by searching for the 0 or 1 following the .txt extension. This data
#   is then returned as the variables "positive" and "negative" to be used later.

#   The Positive and Negative variables are passed to the probabilityCheck function, which calculates and returns
#   the probability that each review is positive or negative, based on the training data.

#   The next step is the reviewHandle function, which receives N, the list of separated reviews, and the type count
#   The reviewHandle function begins by separating and concatenating all of the positive reviews and all of the
#   negative reviews so that they can be analyzed separately. This is done using the same regular expression as
#   the sentientCheck.

#   Each continuous string of text (The positive reviews and negative reviews) is then passed to the textHandle
#   function, along with N. The textHandle function uses regular expressions to remove certain characters that
#   I personally chose to remove, such as commas, periods, and question marks. It also removes the 0 and 1
#   classifier from each review, although this is likely unnecessary. It then counts the number of times that
#   each word occurs and stores the data as key:value pairs in the wordCount dictionary. A separate dictionary
#   , selectedWords, is used to select the unigrams that meet the unigram frequency cutoff. This function then
#   returns the selectedWords and the tokens to reviewHandle. reviewHandle then aggregates the data from
#   the positive and negative textHandle and returns the positive words, negative words, positive tokens,
#   and negative tokens.

#   The next step is the probabilityCalc, which receives the list of words, list of tokens, and the length
#   of the list of types. The probability calculator takes the list of chosen words and calculates the
#   probability of each word by dividing the count of the specific word by the sum of the number of tokens
#   and the number of types. These probabilities are then assigned to each word using a separate dictionary
#   which is then returned. This is repeated for the negative words.

#   At this point, the training data is analyzed and the test can begin. The probability of a positive or
#   negative review, along with the probability of the positive and negative words, is then passed to the
#   conductTest function along with the test data.

#   The conductTest function uses readLines() to separate each review in the test data. It then iterates
#   through each review in the test data, gets the review ID using a regular expression, and sums up the
#   logarithm of the probabilities of each word. If a word is not in the training data, the word is skipped.
#   When the log of every word probability has been summed, it then compares the negative and positive
#   probabilities and assigns positive if the positive probability is higher, and negative if the negative
#   is higher. The results are then written to a text file named results.txt.

    
import sys, re, string, math



def getText(training):
    file = open(training, "r", encoding = "utf-8")
    data = file.read()
    file.close()
    file = open(training, "r", encoding = "utf-8")
    lines = file.readlines()
    file.close()
    return data, lines

def typeCount(training):
    types = {}
    training = training.split()
    for word in training:
        types[word] = int(0)
    return(len(types))


#The sentientCheck function determines how many positive and negative reviews are
#found in the training data. 
def sentientCheck(training):
    positive = 0;
    negative = 0;
    #This regular expression searches for the 0 or 1 after the .txt of the every review ID
    #and adds them to X, which is a list of these numbers. The list is then iterated through
    #to get the total count of positive and negative IDs.
    x = re.findall(".*\.txt ([01]) .*", training)
    for num in x:
        if (num == '1'): positive += 1
        elif (num == '0'): negative += 1
    return positive, negative

def probCheck(positive, negative):
    total = positive + negative
    positiveProb: float = positive / total
    negativeProb: float = negative / total
    return positiveProb, negativeProb
    
def textHandle(n, text):
    wordCount = {}

    #The following regular expressions are used to remove certain punctuation and other
    #things from the training data that I personally decided I didn't want in there.
    #I made this choice because I want to focus on the raw words in the data and not
    #have my training data be influenced if there are more questions in the positive reviews
    #or negative reviews.
    #I also removed the reviewID and the 0 or 1. This is fairly unnecessary but I wanted
    #to do it anyway.
    text = re.sub(",", " ", text)
    text = re.sub("\.", " ", text)
    text = re.sub("\?", " ", text)
    text = re.sub("!", " ", text)
    text = re.sub("\(", " ", text)
    text = re.sub("\)", " ", text)
    text = re.sub("\"", " ", text)
    text = re.sub("[.*].txt [01]", " ", text)
    tokens = text
    tokens = tokens.split()
    #Adds each token to a dictionary. Takes advantage of the fact that Python dictionaries
    #do not allow duplicates. The length of the dictionary will be equal to the number of
    #types
    for word in tokens:
        wordCount[word] = int(0)
    #Counts the number of times that each word occurs
    for word in tokens:
        wordCount[word] += 1
    selectedWords = {}
    #This is where the unigram cutoff comes into play. Iterates through the dictionary of
    #words and, if the word occurs more than the cutoff value, adds it to a separate dictionary
    #called selectedWords
    for word in wordCount:
        if wordCount.get(word) >= int(n):
            selectedWords[word] = wordCount.get(word)    
    return selectedWords, tokens

def reviewHandle(n, reviews, types):
    posText = " "
    negText = " "
    for review in reviews:
        #This regular expression is used to concatenate every positive review into one
        #long string, and every negative review into a different long string. This is
        #done to support processing of every positive/negative review at once.
        x = re.findall(".*\.txt ([01]) .*", review)
        if x[0] == '1':
            posText += review
        elif x[0] == '0':
            negText += review
    #posWords/negWords are the dictionaries of words with their counts that meet the
    #requirements of the unigram frequency cutoff
    posWords, posTokens = textHandle(n, posText)
    negWords, negTokens = textHandle(n, negText)
    return posWords, negWords, posTokens, negTokens


#Calculates the probability of each word by taking the number of times the word appears,
#and dividing by the sum of the number of tokens and the number of types. The probability
#is stored in the probabilities dictionary in a key:value pair
def probabilityCalc(words, tokens, types):
    probabilities = {}
    for word in words:
        probability = float(words.get(word)/(types + len(tokens)))
        probabilities[word] = float(probability)
    return probabilities


#Runs the test data. I could not use the regular method of multiplying each probability
#because every value would come out as 0.0. I think I was able to see one actual value, and it
#was to the power of -326.
#Instead, the log of each probability is summed.
def conductTest(positiveProb, negativeProb, posWordProbs, negWordProbs, test):
    result = int
    file = open(test, "r", encoding = "utf-8")
    reviews = file.readlines()
    file.close()
    file = open("results.txt", "w", encoding = "utf-8")
    for review in reviews:
        #Converts the original probability of the review being positive/negative to a logarithm
        pGivenPositive = float(math.log(positiveProb))
        pGivenNegative = float(math.log(negativeProb))
        #The following regular expression obtains the review ID of each review
        x = re.search("(.*).txt .*", review)
        reviewID = x.group(1) + ".txt"
        review = review.split()
        #This is where the probabilities are actually calculated. Sums the log of the probability
        #of each word and assigns each result either a 1 or a 0
        for word in review:
            if(posWordProbs.get(word) == None):
               continue
            else:
                pGivenPositive += float(math.log(posWordProbs.get(word)))
        for word in review:
            if(negWordProbs.get(word) == None):
                continue
            else:
                pGivenNegative += float(math.log(negWordProbs.get(word)))
        if (pGivenPositive > pGivenNegative):
            result = 1
        else:
            result = 0
        #Writes the results to the results.txt file, which can be renamed later if needed
        file.write(reviewID + " " + str(pGivenPositive) + " " + str(pGivenNegative) + " " + str(result) + "\n")
    file.close()
           
    
def main(n, training, test):
    training, reviews = getText(training)
    types = typeCount(training)
    positive, negative = sentientCheck(training)
    positiveProb, negativeProb = probCheck(positive, negative)
    posWords, negWords, posTokens, negTokens = reviewHandle(n, reviews, types)
    posWordProbs = probabilityCalc(posWords, posTokens, types)
    negWordProbs = probabilityCalc(negWords, negTokens, types)
    conductTest(positiveProb, negativeProb, posWordProbs, negWordProbs, test)


    

if __name__ == '__main__':
    n = sys.argv[1]
    training = sys.argv[2]
    test = sys.argv[3]
    main(n, training, test)


    
