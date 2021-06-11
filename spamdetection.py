# -*- coding: utf-8 -*-
"""SpamDetection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZV2_eDVDQL7DbiYESZhIytoC6ruV7H0L

## **Spam Mail Detection**


Spam detection is one of the applications of Machine Learning today. Pretty much all of the major email service providers have spam detection systems built in and automatically classify such mail as 'Junk Mail' or 'Spam'.

Here I have used the **Naive Bayes algorithm** to create a model that can classify dataset SMS messages as spam or not spam, based on the training we give to the model. I have further experimented with using **SVM algorthim**.

It is important to have some level of intuition as to what a spammy text message might look like. Usually they have words like 'free', 'win', 'winner', 'cash', 'prize' and the like in them as these texts are designed to catch your eye and in some sense tempt you to open them. Also, spam messages tend to have words written in all capitals and also tend to use a lot of exclamation marks. To the recipient, it is usually pretty straightforward to identify a spam text and our objective here is to train a model to do that for us!

This is a **binary classification** problem as messages are classified as either 'Spam' or 'Not Spam'. Also, this is a **supervised learning problem**, as we will be feeding a labelled dataset into the model.
"""

import pandas as pd
url = 'https://raw.githubusercontent.com/AmbujaBudakoti27/SpamClassifier/main/SMSSpamCollection'
messages = pd.read_csv(url, sep='\t', names=["labels", "message"])

import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
corpus = []

from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

for i in range(0, len(messages)):
  m = re.sub('[^a-zA-Z]', ' ', messages["message"][i])
  m = m.lower()
  m = m.split()
  m = [ps.stem(word) for word in m if not word in stopwords.words('english')]
  m =' '.join(m)
  corpus.append(m)

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 2500)
X = cv.fit_transform(corpus).toarray()

y = pd.get_dummies(messages['labels'])
y = y.iloc[:,1].values

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

"""## **Naive Bayes**
Naive Bayes is a probabilistic classifier inspired by the Bayes theorem under a simple assumption which is the attributes are conditionally independent.

Naive Bayes is a very simple algorithm to implement and good results have obtained in most cases. It can be easily scalable to larger datasets since it takes linear time, rather than by expensive iterative approximation as used for many other types of classifiers.

### Why Multinomial Naive Bayes? What about other models like Gaussian Naive Bayes or Bernoulli Naive Bayes?

Well, Multinomial NB considers the frequency count (occurrences) of the features (words in our case) while Bernoulli NB cares only about the presence or absence of a particular feature (word) in the document. The latter is adequate for features that are binary-valued (Bernoulli, boolean). Whereas, with Gaussian NB, features are real-valued or continuous and their distribution is Gaussian, the Iris Flower dataset is an example with continuous features.
"""

from sklearn.naive_bayes import MultinomialNB
spam_detect_model_v1 = MultinomialNB().fit(X_train, y_train)
y_pred = spam_detect_model_v1.predict(X_test)

from sklearn.metrics import accuracy_score
accuracy_v1 = accuracy_score(y_test, y_pred)

from sklearn.metrics import confusion_matrix
conf_v1 = confusion_matrix(y_test, y_pred)

spam_detect_model_v1.score(X_test,y_test)

print("BOW and NaiveBayes\n")
print("accuracy: ", accuracy_v1, "\n")
print(conf_v1)

from sklearn.metrics import classification_report
classificationr=classification_report(y_test, y_pred)
print(classificationr)

"""## **Support Vector Machine**
SVM is a supervised machine learning algorithm which can be used for both classification or regression challenges. However, it is mostly used in classification problems.

SVM builds a classifier by searching for a separating hyperplane (optimal hyperplane) which is optimal and maximises the margin that separates the categories (in our case spam and ham). Thus, SVM has the advantage of robustness in general and effectiveness when the number of dimensions is greater than the number of samples.
Unlike Naive Bayes, SVM is a non-probabilistic algorithm.

**gamma**: Kernel coefficient for ‘rbf’, ‘poly’ and ‘sigmoid’. Higher the value of gamma, will try to exact fit the as per training data set i.e. generalization error and cause over-fitting problem.

**C:** (Regularization parameter) C is 1 by default and it’s a reasonable default choice. If you have a lot of noisy observations you should decrease it: decreasing C corresponds to more regularization.

**Low values of gamma indicates a large similarity radius** which results in more points being grouped togther. For high vlaues of gamma, the points need to be very close to each other to be considered in the same group.

If **C is small, the penalty for misclassification is low** so a decision boundary with large margin is chosen.

If **C is large, SVM tries to minimize the numberr of misclassified examples due to high penalty** which results in a decision boundary with a smaller margin.
"""

from sklearn.svm import SVC
model_C = SVC(C=10)
model_C.fit(X_train, y_train)
model_C.score(X_test, y_test)

from sklearn.svm import SVC
model_C2 = SVC(C=100)
model_C2.fit(X_train, y_train)
model_C2.score(X_test, y_test)

from sklearn.svm import SVC
model_C3 = SVC(C=0.01)
model_C3.fit(X_train, y_train)
model_C3.score(X_test, y_test)

from sklearn.svm import SVC
model_g = SVC(gamma=10)
model_g.fit(X_train, y_train)
model_g.score(X_test, y_test)

from sklearn.svm import SVC
model_g2 = SVC(gamma=0.01)
model_g2.fit(X_train, y_train)
model_g2.score(X_test, y_test)

model_linear_kernal = SVC(kernel='linear')
model_linear_kernal.fit(X_train, y_train)
model_linear_kernal.score(X_test, y_test)

model_kernal = SVC(kernel='rbf')
model_kernal.fit(X_train, y_train)
model_kernal.score(X_test, y_test)

model_sigmoid_kernal = SVC(kernel='sigmoid')
model_sigmoid_kernal.fit(X_train, y_train)
model_sigmoid_kernal.score(X_test, y_test)

model_poly_kernal = SVC(kernel='poly')
model_poly_kernal.fit(X_train, y_train)
model_poly_kernal.score(X_test, y_test)

"""### Highest accuracy achieved above:

from Linear SVM Algorithm :    0.9874439461883409 

from Naive Bayes Algorithm:   0.9856502242152466 
"""