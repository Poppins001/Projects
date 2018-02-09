from gym.envs.registration import register

register(
    id = 'Custom-env-1',
    entry_point = 'Custom-env.envs:Env1'
)
register(
    id = 'Custom-env-2',
    entry_point = 'Custom-env.envs:Env2'
)
