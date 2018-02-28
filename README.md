# POS-Tagging
<ul>
  <li>
Developed a Hidden Markov Model Part-of-Speech Tagger for English, Chinese and Hindi languages.
  </li>
  <li>
Performed a comparison between various transition and emission smoothing techniques which include Laplace Smoothing, Absolute Discounting and Good-Turing Smoothing.
    </li>
  <li>
Attained accuracy of 88% for English, 86% for Chinese and 92% for Hindi.
    </li>
  <li>
Trained the tagger on the corpus adapted from the English (Original) and Chinese (GSD) sections of the Universal Dependencies corpus.
</li>
  <li>
The script hmmlearn3.py estimates transition and emission probabilities and stores them to hmmmodel.txt.</li>
  <li>
The tagging program will be invoked in the following way:  </li>
<li>
  python hmmdecode.py /path/to/input</li>
  <li>
The argument is a single file containing the test data; the program will read the parameters of a hidden Markov model from the file hmmmodel.txt, tag each word in the test data, and write the results to a text file called hmmoutput.txt in the same format as the training data. 
  </li>
