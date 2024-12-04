# Hidden-Markov-Model
This project creates a Hidden Markov Model of the recorded PM2.5 Index based
on data from the Changping data set. The evidence for this HMM is the day. The evidence is
true if the day is within the first two weeks of the data set (days 1-14) and the evidence
is false if the day is within the last two weeks of the data set (days 15-28). Prior uses the default
because there is a 50/50 split between true and false for the evidence. The PM2.5 readings are broken
into four ranges: low(0-50), moderate(51-100), high(101-150), and very high(151+). Then
the true and false probabilities were caclulated for each of the four ranges of the PM2.5 attribute
