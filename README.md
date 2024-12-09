# Email Summerizer using Llama

## Problem Statement
It's really cumbersome to go through all the emails we get on a daily basis across our personal and professional lives, having a quick one line summery would result in a 14% increase in productive time per day.

## Data Generation 
- Used Llama 3.1 8B to generated high quality emails,
- This showed the capabilities of LLM's to generate their own high quality synthetic data through goof prompting
- More importantly it's impressive to see how good a relativly smaller and chepaer model was at genereting this data

## Implementation 
- Used the Ollama framework in python to leverage open-sourse AI
- Passed the sythetically generated emails back to the LLM along with well engineered prompts to get a catagory and summery of the given emails

## Results 
Using the Llama 3.1 8B model, I was able to both generate and summarize the email data. I could have used a Google API and pulled in some real Gmail emails for the model to summarize, but I found the idea of having the LLM generate its own data very profound. The data generated was quite high quality even though a relatively low-cost model was used, which was intriguing.

The summaries were pretty clear, concise, and captured all the details of the emails in a single sentence as any good summarizer should. A lot of that had to do with good prompt engineering and less about the model used, depicting the importance of good prompt engineering in this day and age of technology.

The main caveat here was that I used Meta's open-source Llama 3.1 model with 8B parameters. This model wasn't really built for high-quality direct inference, but the results show that for simple tasks, the heavier, more expensive model is NOT needed. Picking a model with the required capabilities is more important, as this smaller model would significantly reduce costs on a production level compared to its larger 70B and 405B counterparts.
