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
                "tasks": experiment["tasks"],
                "time": experiment["times"],
                "type": [experiment["name"]] * len(experiment["times"])
            }
        )])

    # results_df["time"] = np.clip(results_df["time"], 0, 60)

    # print(results_raw)
    # results_df = pd.DataFrame.from_records(results_raw)
        
    import matplotlib.pyplot as plt
    import seaborn as sns
    from scipy.signal import savgol_filter

    # Assuming 'results_df' is your DataFrame
    # Example data smoothing with savgol_filter
    # results_df['smoothed_time'] = savgol_filter(results_df['time'], window_length=7, polyorder=2)  # Adjust window length and polyorder

    import matplotlib.pyplot as plt

    # plt.ylim(0, 60)

    # Plot the results into results-file named "results-file.png"
    sns.set_theme(style="whitegrid")
    plot = sns.lineplot(x="tasks", y="time", hue="type", data=results_df, legend=True)

    # # Add labels slightly above the middle of each line, aligned to the curve
    # for type_name in results_df['type'].unique():
    #     # Get the subset of data for this "type"
    #     subset = results_df[results_df['type'] == type_name]
        
    #     # Choose a point around the middle for label placement
    #     mid_index = len(subset) // 2
    #     x_mid = subset['tasks'].iloc[mid_index]
    #     y_mid = subset['time'].iloc[mid_index]
        
    #     # Use two nearby points to calculate the slope
    #     if mid_index < len(subset) - 1:
    #         x1, y1 = subset['tasks'].iloc[mid_index - 1], subset['time'].iloc[mid_index - 1]
    #         x2, y2 = subset['tasks'].iloc[mid_index], subset['time'].iloc[mid_index]
    #     else:
    #         # If mid_index is at the end, use the last two points
    #         x1, y1 = subset['tasks'].iloc[mid_index - 1], subset['time'].iloc[mid_index - 1]
    #         x2, y2 = subset['tasks'].iloc[mid_index], subset['time'].iloc[mid_index]

    #     # Calculate the angle of the slope in degrees
    #     angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        
    #     # Add the label above the midpoint of the line
    #     plt.text(
    #         x_mid, y_mid + 1, type_name,  # Adjust y_mid + 1 for a slight vertical offset
    #         fontsize=9, va='bottom', ha='center',
    #         rotation=angle, rotation_mode='anchor'
    #     )

    # Save the plot
    fig = plot.get_figure()
    fig.savefig(results_file.name + ".png")
    
if __name__ == '__main__':
    main()