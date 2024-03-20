from stable_baselines3 import PPO
from sc2_env.sc2env import Sc2Env


LOAD_MODEL = r"C:\ai\RL\SCII-agent-main\sc2_env\models\2880000.zip"
# Environment:
env = Sc2Env()

# load the model:
model = PPO.load(LOAD_MODEL)


# Play the game:
obs = env.reset()
done = False
while not done:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)

