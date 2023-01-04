Optimisation Report
-------------------
The first thing I did in an attempt to optimise this code
was to use a generator for the random.choice() calls. This
did not appear to alter my time at all and hence I removed it
afterwards. You can check my previous commits to find this.

Following this, I tried using different methods from the
random module. First I tried using random.randint(), as I
found online that generating and indexing using a random 
number is meant to be faster than the choice method, but I
found that when I implemented this, the time increased. As a
result, I then tried to use random.shuffle() and then
selecting the first value after this. This, however, took
well over ten minutes before I gave up. I then did some more
research and found that using random.SystemRandom() was meant
to be more secure, but this increased my time by nearly
double. 

I then spent quite a lot of time trying to implement the use
of the multiprocessing module, but I failed to get it working.
I forgot to include this into a commit, so I will do that
after I commit the completion of this report. I aimed to
speed the processing time of the page rank by making multiple
cores completing a fraction of the work each at the same
time, as I expected this would make it significantly shorter.
However, no matter how many things I tried, I was stuck on
getting the pool to run the stochastic method using argparse.

Other minor alterations that were successful included
replacing some for loops with dictionary comprehensions, and
only importing required methods from the modules that we
were required to use. As a result, I managed to shorten the
duration of the stochastic method from 50 seconds to 44
seconds on my computer.

After committing and attempting to recover evidence of
multiprocessing, I realised that I had deleted most of it
without making a copy of it anywhere. As a result, I will
instead post a part of it which I did manage to recover in
an attempt to prove that this was actually attempted.

```
def calculate_stochastic_page_rank(graph, args):
    # Create a new process for each chunk of the graph
    with Pool(4) as p:
        # Remove open file TextIOWrapper Object
        del vars(args)['datafile']
        # Map the stochastic_page_rank function to each chunk of the graph
        results = p.map(stochastic_page_rank, graph, args)
        return results
```