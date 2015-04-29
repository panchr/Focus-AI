## Unit Tests

I use unit tests to make sure each individual component of the core AI is working. This functionality also allows me to detect any errors early on.
For example, if I add a feature which breaks something else, the unit tests would catch this error and help me figure out the cause.
As long as I catch the errors early on, I will be able to fix them more easily.

As part of the unit tests, I had to create a way to generate a random database collection name. This makes setting up the test cases (as well as cleaning up afterwards) trivial, because they are executed in isolation.

Writing unit tests as I developed definitely elongated the process.
However, it forced me to review my code and algorithm more carefully, which helped from the very beginning. In addition, they have prevented me from committing numerous careless mistakes.

I used git's `pre-commit` hook to run all unit tests before committing to the repository --- this ensures that every commit is a stable release as well.
