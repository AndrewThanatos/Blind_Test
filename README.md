# Test_Solver

## The code contains detailed comments and explanations

This particular algorithm searches for the right answers for 25 questions with 4 options (the algorithm itself is universal so it can process more question with more options). Each request returns the number of correct answers.

The request is the most time consuming processes in the program. So **my goal was to minimize the number of requests**, and thus significantly reduce the time required to run the program. This algorithm employs the use of multiprocessing. For added efficiency multiple answers are checked simultaneously. 

To understand how the algrithm works, lets say that we have only 10 questions with 4 options.

The list of correct answers = *[1, 3, 2, 0, 0, 1, 3, 1, 1, 1]*


So first we want to determine the number of times each options apears as the correct answer, in our example it will be:

- option 0 appears 2 times.
- option 1 appears 5 times.
- option 2 appears 1 times.
- option 3 appears 2 times.

We can generate a sequence that  contains the correct answers, but are put in a random order. According to the Probability Theory, if the number of questions is large enough, many of the answers will happen to be in the correct positions. So this algorithm will function even better, when there are more questions.

Another thing that we can do to speed up our algorithm, is to sort the pool of options by how often they appear. So we will get a list containing options sorted from the most frequent ones to the least frequent. And later when we need to substitute an option, we will use the most frequent one first.

So the preparation was made. Now we can iterate over all options, and in each iteration iterate over all questions (first loop, second loop). In the second loop, we substitute options to check which ones are correct. In simpler words, we just brute force, but we don't go through all the options. There are 3 possible states:

- 1 Privious option was correct
- 2 Changed option is correct
- 3 Both options are incorrect

Every outcome provides valuable information. With the first and second we get the correct answer, Perfect. With the third we know, we no longer need to try this options.

So, that's it. We iterate over all options getting feedback (determining which options were correct and which were not) and on every iteration we get  significantly fewer requests. After the last iteration, we have all the correct answers. In the worst case scenario we get O(n\*m) but it is very rare, on average it will be **O(n\*log(m)**, where n = questions, m = options.
