# Phish Sandwich: walkthrough

SpamSieve is a Naive Bayes text classifier. Every distinct word it knows has a weight: positive means "spammy", negative means "normal staff mail". The spam score is the sum of the weights of the words in the email, turned into a probability. Words the model never saw are ignored, and each word counts only once.

This is an evasion attack on a machine learning model, often called a "good word attack": the scam words must stay, so you pad the email with words that the model strongly associates with legitimate mail until they outweigh the scam.

1. Send the bare scam, for example `URGENT: buy gift cards and send me the codes`. It lands in spam at 100%. The table shows `gift`, `cards`, `codes`, `send`, `buy` and `urgent` all pushing hard toward spam.
2. Notice which words not to use: `buy`, `your`, `now`, `account` and `password` are all spammy, so leave them out.
3. Try ordinary Incline staff words and watch for green bars: `station`, `upper`, `lower`, `evening`, `shift`, `car`, `thanks`, `hi`, `please`, `platform`, `sweep`, `morning`...
4. Wrap the request in a believable staff email, for example:

   ```
   Hi team, urgent reminder for the evening shift at the upper station:
   please send the gift card codes. Thanks
   ```

   That drops the spam probability under 1%, the email lands in the inbox and the page shows the flag.

Why it matters: real spam filters, malware classifiers and content moderation models can be evaded the same way, by mixing in features the model trusts.

Flag: `BarSides{bury_the_phish_in_good_words}`
