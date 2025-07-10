import pandas as pd
import plotly.express as px

def sizes_by_episode():
    df = pd.read_csv('../data/sizes.csv', delimiter=",")

    fig = px.line(df).update_layout(
        xaxis_title="Episodes", yaxis_title="Sizes"
    )
    fig.show()

if __name__ == '__main__':
    sizes_by_episode()
