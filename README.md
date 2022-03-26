<h1 align="center"> OpenAI's GPT-3 Messenger </h1>


<img align="left" width="600" height="600" src="img/GPT-3.gif"/>

  
This is a Messenger app of Open AI's [GPT-3 API](https://openai.com/blog/openai-api/)

* Here is the relevant [Facebook application](https://www.facebook.com/The-All-Knowing-One-103780238591514)

* Web hosting is on a [Heroku server](https://www.heroku.com). The server has a CI/CD integration with this Github repository, such that any pushes to the 'main' branch result in a rebuilding of the web application.

## Usage:
* Requires a Facebook account
* Requires administrator access to the Facebook Developer Application (request Flynn for this access - info@flynnowen.com)
*  It is coded to be a simple conversation implementation. It will respond to messages one at a time, and can not yet respond to images, links, gifs, or any other type of attachment. This implementation has a 'working memory' of 5 minutes - meaning that if it hasn't received a message within 5 minutes of your previous message, it's memory is wiped. This wiping could be considered as a 'conversation'. 

## Notes:
I've stumbled across the adaptor design pattern (https://en.wikipedia.org/wiki/Adapter_pattern) - which this repository could be considered as (a conversational messenger adaptor for GPT-3)

