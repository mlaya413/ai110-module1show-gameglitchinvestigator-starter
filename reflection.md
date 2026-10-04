# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| pressed new game button | new game starts  |    nothing happens  |  no output or error - app.py
|  no input, exceeded attempts | score is 0 |        score is negative|    "Score: -35" - logic_utils.py
| entered guess higher than secret num| to output "go lower" | outputs "go higher" | "Go HIGHER!"| - logic_utils.py

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

1. I used Copilot on this project.
2. One example of an AI suggestion that was correct was the AI suggesting reversing the outputs of the higher/lower branches. Intitially, when the user's guess was higher than secret number, it was telling the user to still guess higher. The AI found the correct lines and flipped the outputs, so that they correlated to their surrounding logic. I verified the results using pytest cases for this specific bug.
3. One example of an AI suggest I didn't accept but that the AI wanted to create and run test cases before it had fully finished fixing the bugs. While all of its suggestion leading up to that were in scope and easy to read, the test cases were also too large and did not directly test the specific bug we were looking at.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

To decide if a bug was really fixed, I had the AI make any test cases for any edge case I could think of. I also went back to my list of issues at the beginning and looked through manually to see if there was anything that stuck out to me. I ran the entire app by itself and noticed how certain buttons like the new game button were not working. The AI helped me understand the test by explaining exactly what it was testing and why it would catch bugs of a certain type. 
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
