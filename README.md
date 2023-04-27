# USE AI AGENTs, like AUTOGPT or BABYAGI, without paids API 😤 . **TOTALLY FOR FREE🤑**

Tired of paying for OPENAI, PINECONE, GOOGLESEARCH APIs to try out the latest developments in the AI field?
Perfect, **this is the repository for you! 🎁**

For any problem open an ISSUE 🚬, the project is very simple so any help is welcome💸.

![GH](https://user-images.githubusercontent.com/108482353/234973544-427cbd59-93a0-4bfc-b9c9-eeddf7134a11.gif)



## WHY THIS REPOSITORY ? 🤔

Hello everyone :smiling_face_with_three_hearts: ,

I wanted to start by **talking about how important it is to democratize AI**. Unfortunately, most new applications or discoveries in this field end up enriching some big companies, leaving behind small businesses or simple projects. One striking example of this is Autogpt, an autonomous AI agent capable of performing tasks.

Autogpt and similar projects like BabyAGI **only work with paid APIs, which is not fair**. That's why I tried to recreate a simpler but very interesting and, above all, open-source version of Autogpt that **does not require any API and does not need any particular hardware.**

I believe that by providing free and open-source AI tools, we can give small businesses and individuals the opportunity to create new and innovative projects without the need for significant financial investment. **This will allow for more equitable and diverse access to AI technology, which is essential for advancing society as a whole.**



-----

## HOW TO GET CHATGPT & HUGGINGFACE TOKEN FREE 🔑🔐

- **HUGGINGFACE🤗** : Visit this simple [official guide](https://huggingface.co/docs/hub/security-tokens)
- **CHATGPT🖥** : visit this [site](https://chat.openai.com/api/auth/session) and copy the "accessToken"

![CHATGPT_TOKEN](https://user-images.githubusercontent.com/108482353/234968090-b724e277-566c-4e42-9936-7592043f70fa.png)



-----

## HOW TO RUN CAMEL 🐫
- dowload the repository [FREE AUTOGPT REPOSITORY](https://github.com/IntelligenzaArtificiale/Free-AUTOGPT-with-NO-API) and extract
- pip3 install -r requirements.txt
- streamlit run Camel.py
- get your free token on [this link](https://chat.openai.com/api/auth/session)
<video  width="100%" height="240" controls autoplay>
<source src="https://video.wixstatic.com/video/3c029f_363d7f30738147e5a43f5943757a0246/1080p/mp4/file.mp4"  type="video/webm" >
</video> 

![image|690x441](img/ok.png)


-----



## HOW TO RUN BABY AGI 👶
- dowload the repository [FREE AUTOGPT REPOSITORY](https://github.com/IntelligenzaArtificiale/Free-AUTOGPT-with-NO-API)
- pip3 install -r requirements.txt
- Usage: **python BABYAGI.py --hf_token YoUrHFtOkEn --chatgpt_token YoUrChATgPTtOkENisSOlOnG**




https://user-images.githubusercontent.com/108482353/234963635-004adace-36ab-46de-9022-61858cd3dca4.mp4






-----

## HOW TO RUN AUTOGPT 🤖
- dowload the repository [FREE AUTOGPT REPOSITORY](https://github.com/IntelligenzaArtificiale/Free-AUTOGPT-with-NO-API)
- pip3 install -r requirements.txt
- Usage: **python AUTOGPT.py --hf_token YoUrHFtOkEn --chatgpt_token YoUrChATgPTtOkENisSOlOnG**


https://user-images.githubusercontent.com/108482353/234947600-1df35b1f-6505-40f9-be1d-3257a46eacf3.mp4




-----


## HOW IT WORK ? 🔨🔩

To create an open-source version of Autogpt that does not require paid APIs or specific hardware, **we performed a reverse engineering process on ChatGPT**, a language model developed by OpenAI. By doing so, we were able to use the agents and new technologies of langchain for free.

We then created a custom LLM wrapper with langchain, **which can be used as a plug-and-play solution with any langchain function or tool 💡**.

```python
from ChatGPTAPI import ChatGPT

# Instantiate a ChatGPT object with your token
llm = ChatGPT(token="YOURTOKEN")

# Generate a response based on the given prompt
response = llm("Hello, how are you?")

# Print the response
print(response)

```

The code snippet provided above shows how to use our custom ChatGPT LLM class to interact with the language model. It requires a token from the ChatGPT API, which can be obtained from [https://chat.openai.com/api/auth/session](https://chat.openai.com/api/auth/session). 

Please note that there is a limit of 50 requests per hour for each account on the ChatGPT API 💣. Therefore, we implemented a call counter in our ChatGPT class to prevent exceeding this limit.

We believe that our open-source version of Autogpt will promote equitable and diverse access to AI technology and empower individuals and small businesses to create innovative AI projects without significant financial investment.



### With this "CUSTOM LLM WRAPPER" now u can build or test your LLM APP's WITHOUT PAYing

-----

#### LINK : 
- [VIDEO DEMO](https://watch.screencastify.com/v/vSDUBdhfvh9yEwclHUyw)
- [FREE AUTOGPT REPOSITORY](https://github.com/IntelligenzaArtificiale/Free-AUTOGPT-with-NO-API)
- [Camel project](https://www.camel-ai.org/)
- [BABY AGI](https://python.langchain.com/en/latest/use_cases/agents/baby_agi_with_agent.html)
- [AutoGPT](https://python.langchain.com/en/latest/use_cases/autonomous_agents/autogpt.html?highlight=autogpt#setup-model-and-autogpt)
- [langchain for custom llm wrapper](https://python.langchain.com/en/latest/modules/models/llms/examples/custom_llm.html)


# **🤗 Democratize AI 🤗**

-----

## TODO , I NEED YOUR HELP 
- [x] Create free LLM langchain wrapper based on [Reverse Engineered ChatGPT API by OpenAI](https://github.com/acheong08/ChatGPT) 
- [x] Create a simple versione of AUTOGPT based on [Camel theory](https://arxiv.org/pdf/2303.17760.pdf)
- [x] Find a way to replace OpenAIEmbeddings()
- [x] Create a simple version of AUTOGPT based on [Baby AGI](https://alumni.media.mit.edu/~kris/ftp/SafeBabyAGI-J.BiegerEtAl2015.pdf)
- [x] Add web search agent
- [x] Add file writer agent
- [x] Finally AUTOGPT without paids API

- [ ] Add other free Custom LLM wrapper [Add this](https://github.com/xtekky/gpt4free)
- [ ] Add long term memory
- [ ] Find a way to replace PINECONE api
- [ ] Find a way to replace official Google API


-----

