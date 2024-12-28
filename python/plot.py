import click
import seaborn as sns
import pandas as pd
import json
import numpy as np

@click.command()
@click.option("--results-file", type=click.File(), help="File to load results from")
def main(results_file):
    results = json.load(results_file)
    
    results_df = pd.DataFrame({
        "tasks": [],
        "time": [],
        "type": []
    })
    for experiment in results:
        results_df = pd.concat([results_df, pd.DataFrame(
            {
                "tasks":  [1, 2, 4, 8, 16, 32],
                "time": experiment["times"],
                "type": [experiment["name"]] * 6
            }
        )])

    results_df["time"] = np.clip(results_df["time"], 0, 60)

    # print(results_raw)
    # results_df = pd.DataFrame.from_records(results_raw)
        
    import matplotlib.pyplot as plt

    # plt.ylim(0, 60)

    # Plot the results into results-file named "results-file.png"
    sns.set_theme(style="whitegrid")
    plot = sns.lineplot(x="tasks", y="time", hue="type", data=results_df)
    
    # Save the plot
    fig = plot.get_figure()
    fig.savefig(results_file.name + ".png")
    
if __name__ == '__main__':
    main()