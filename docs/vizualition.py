import pandas as pd
import plotly.express as px

def rewards_by_episode():
    df = pd.read_csv('../data/rewards.csv', delimiter=",")

    fig = px.line(df).update_layout(
        xaxis_title="Episodes", yaxis_title="Rewards"
    )
    fig.show()

if __name__ == '__main__':
    rewards_by_episode()
