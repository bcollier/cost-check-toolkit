# Iteration

> ✍️ **WRITE THIS YOURSELF.** 

## What went wrong

The first attempt was suggesting showing prices to the user rather than checking whether the calls to the API were logged.

## Why

An earlier version of the skill suggested checking whether prices were shown to end users and I didn't catch it to say no that is not helpful. 

## What I changed

I told it to stop checking for showing prices to users and start checking if all API calls are logged both send and received.

## Rerun result

Now it returns the correct results, making sure all API calls are logged.

https://github.com/bcollier/cost-check-toolkit/tree/main/notes/excerpts