# Tactics framework: Synergizing Reinforcement Learning and Large Language Models to Play StarCraft II

![SCII-Structure](https://github.com/Shuaikx/SC2_Agent/blob/main/Images/image1.png)

Given the highly intricate state space, incomplete information gameplay, and the necessity for long-term strategic planning, StarCraft II has emerged as a crucial platform for research and development in reinforcement learning (RL). Models such as AlphaStar and ROA-Star have attracted attention for their achievements in simulating strategic planning in the game world. however, their training processes consume substantial resources and lack interpretability in long-term strategic planning and actions. Emerging large language model (LLMs) agents, such as TextStarCraft II, address some RL agents' shortcomings, yet extensive API calls consumes significant time, yielding experimental results below expected excellence. Therefore, we propose the Tactics framework, which synergizes RL and LLM, leveraging the decision-making and game tactics capabilities of LLMs along with the real-time feedback strengths of RL. This framework has been successfully deployed in the complex RTS game StarCraft II. The structure includes enhanced components such as self-reflection and memory, as well as using LLM's reasoning and decision-making capabilities for the first time to choose game tactics. Experimental results demonstrate significant reductions in both the frequency and total duration of API calls during gameplay when compared to the LLM agent. Simultaneously, the best result of agent surpassed the Level 7 build-in AI. achieving a 90% win rate against the Level 4 built-in AI, and securing a 60% victory rate over the Level 5 built-in AI.

## Project Setup
### You need to complete the following tasks before running the code:
1. download the StarCraft II,the download link: https://www.bilibili.com/video/BV1M841127zT/?spm_id_from=333.337.search-card.all.click  
2. You can upload the maps in Map file
3. This project involves calling the OpenAI model and needs to register an api_key, which needs to be filled in to the.env file. As follows:
```bash
# Once you add your API key below, make sure to not share it with anyone! The API key should remain private.

OPENAI_API_KEY=abc123
```

### Before installing the environment, you can use conda to create an environment

```bash
conda create -n sc2_agent python=3.10
conda activate sc2_agent
```

### Install the environment and run the code
```bash
pip install -r requirements.txt
python train_PPO.py
```


## Performance evaluation of the Tactics framework
![SCII-Structure](https://github.com/Shuaikx/SC2_Agent/blob/main/Images/image3.png)


![SCII-Structure](https://github.com/Shuaikx/SC2_Agent/blob/main/Images/image4.png)

