#Kyle Mellott

#This program is used to evaluate the results of the Naive Bayes classifier. It receives
#input via the command prompt, with the first argument being the results from testing data
#with the classifier, and the second argument being the gold standard results for the
#test data.

#The program outputs each review ID, followed by the gold standard answer and the answer
#from the Naive Bayes classifier. After each review has been printed, it prints out the accuracy,
#precision, recall, and the number of true and false positives and negatives.

#An example of program operation is as follows:
#   In the command prompt:
#   >> Python eval.py naive-bayes-answers.txt sentiment-gold.txt > naive-bayes-answers-scored.txt

#The steps of the program are as follows:
#   The user starts the program via the command prompt, passing in the 2 arguments mentioned previously.
#   These arguments are then passed to the main() function.

#   The main function first calls gatherID, passing in the list of results. gatherID uses readlines()
#   to separate each review and uses a regular expression to find the review ID. It then appends each
#   review ID to a list, and returns this list.

#   Next, the gatherResults function is called, passing in the list of results. gatherResults works
#   in much the same way as gatherID, but it uses a regular expression to search for the 0 or 1 at
#   the end of each line. It then appends this 0 or 1 to a resultList, and returns the list.

#   correctAnswer is then called, passing in the gold standard answers. This function works in the
#   exact same way as the gatherResults function and returns the list of gold standard answers.

#   The lists of IDs, results, and gold standard answers are then passed to the evaluate function.
#   The evaluate function enters a while loop that continues until the entirety of the lists
#   has been iterated through. For each iteration, it prints the review ID followed by the
#   gold standard answer and the result of the classifier. It then keeps a count of each true
#   or false positive or negative answer.
#   It then calculates precision, accuracy, and recall. Following this, it prints out each of these
#   values along with the number of true or false positive and negative answers.




import sys, re, string




def gatherID(results):
    idList = []
    file = open(results, "r", encoding = "utf-8")
    lines = file.readlines()
    file.close()
    for line in lines:
        #This regular expression extracts the review ID from each review
        x = re.search("(.*).txt .*", line)
        idList.append(x.group(1))
    return idList


def gatherResults(results):
    resultList = []
    file = open(results, "r", encoding = "utf-8")
    lines = file.readlines()
    file.close()
    for line in lines:
        #This regular expression extracts the 0 or 1 from each result
        x = re.search("([01])\n", line)
        resultList.append(x.group(1))
    return resultList

def correctAnswer(goldStandard):
    resultList = []
    file = open(goldStandard, "r", encoding = "utf-8")
    lines = file.readlines()
    file.close()
    for line in lines:
        #This regular expression extracts the 0 or 1 from the gold standard answers
        x = re.search("([01])\n", line)
        resultList.append(x.group(1))
    return resultList

def evaluate(idList, resultList, correctAnswers):
    truePositive = 0
    trueNegative = 0
    falsePositive = 0
    falseNegative = 0
    i = 0
    while i < len(correctAnswers):
        print(idList[i] + " " + correctAnswers[i] + " " + resultList[i])

        #The following if/elif statements keep a running count of each true/false
        #positive/negative value
        
        if resultList[i] == '1' and correctAnswers[i] == '1':
            truePositive += 1
            i += 1
        elif resultList[i] == '0' and correctAnswers[i] == '0':
            trueNegative += 1
            i += 1
        elif resultList[i] == '1' and correctAnswers[i] == '0':
            falsePositive += 1
            i += 1
        elif resultList[i] == '0' and correctAnswers[i] == '1':
            falseNegative += 1
            i += 1

    #Calculations for precision/accuracy/recall, sourced from the textbook
    precision = (truePositive / (truePositive + falsePositive))
    accuracy = (truePositive + trueNegative) / (truePositive + trueNegative + falsePositive + falseNegative)
    recall = truePositive / (truePositive + falseNegative)
    
    print("Accuracy is: " + str(accuracy))
    print("Precision is: " + str(precision))
    print("Recall is: " + str(recall))
    print("truePositive = " + str(truePositive))
    print("trueNegative = " + str(trueNegative))
    print("falsePositive = " + str(falsePositive))
    print("falseNegative = " + str(falseNegative))



def main(results, goldStandard):
    idList = gatherID(results)
    resultList = gatherResults(results)
    correctAnswers = correctAnswer(goldStandard)
    evaluate(idList, resultList, correctAnswers)



if __name__ == '__main__':
    results = sys.argv[1]
    goldStandard = sys.argv[2]
    main(results, goldStandard)
