import matplotlib.pyplot as plt




y_axis_range = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
bar_color = ["#ff0000", "#ff0000", "#ff0000", "#ff0000", "#ff0000", "#ff0000", "#ff0000", "#ff0000", "#ff0000", "#ff0000", "#ff0000", "#ff0000", "#ff0000", "#ff0000", "#ff0000", "#ff0000", "#ff0000", "#ffa500", "#ffa500", "#3cb371"]


def draw(population):

    fitness_scores = {
        "overall_score" : [],
        "note_rest_ratio": [],
        "note_length_ratio" : [],
        "contiguous_melody_ratio" : [],
        "interval_size_ratio" : [],
        "allowable_interval_size" : []
}
    for score in population:
        score = score[1]
        fitness_scores["overall_score"].append(score["overall_score"])
        fitness_scores["note_rest_ratio"].append(score['note_rest_ratio'])
        fitness_scores["note_length_ratio"].append(score['note_length_ratio'])
        fitness_scores["contiguous_melody_ratio"].append(score['contiguous_melody_ratio'])
        fitness_scores["interval_size_ratio"].append(score['interval_size_ratio'])
        fitness_scores["allowable_interval_size"].append(score['allowable_interval_size'])

    fig, axes = plt.subplots(2, 3, figure=(12,4))
    plt.subplots_adjust(hspace = 0.4)
    fig.suptitle("Scores of Generated Music Pieces!!")

    #subplot 1
    _, _, patches1 = axes[0][0].hist(fitness_scores["overall_score"], bins=y_axis_range, edgecolor='black', color='orange')
    axes[0][0].set_title('Scores of Generated Music Pieces (Overall)')
    axes[0][0].set_xlabel('Overall Score Value')

    #subplot 2
    _, _, patches2 = axes[0][1].hist(fitness_scores["note_rest_ratio"], bins=y_axis_range, edgecolor='black')
    axes[0][1].set_title('Scores of Generated Music Pieces (Note/Rest Ratio)')
    axes[0][1].set_xlabel('Data1 Score Value')

    #subplot 3
    _, _, patches3 = axes[0][2].hist(fitness_scores["note_length_ratio"], bins=y_axis_range, edgecolor='black')
    axes[0][2].set_title('Scores of Generated Music Pieces (Note Length Ratio)')
    axes[0][2].set_xlabel('Data2 Score Value')

    #subplot 4
    _, _, patches4 = axes[1][0].hist(fitness_scores["contiguous_melody_ratio"], bins=y_axis_range, edgecolor='black')
    axes[1][0].set_title('Scores of Generated Music Pieces (Contiguous Melody Shape)')
    axes[1][0].set_xlabel('Data2 Score Value')

    #subplot 5
    _, _, patches5 = axes[1][1].hist(fitness_scores["interval_size_ratio"], bins=y_axis_range, edgecolor='black')
    axes[1][1].set_title('Scores of Generated Music Pieces (Interval Jump Ratio)')
    axes[1][1].set_xlabel('Data2 Score Value')

    #subplot 6
    _, _, patches6 = axes[1][2].hist(fitness_scores["allowable_interval_size"], bins=y_axis_range, edgecolor='black')
    axes[1][2].set_title('Scores of Generated Music Pieces (Allowed Interval Jumps)')
    axes[1][2].set_xlabel('Data2 Score Value')
    
    #get max ylimit
    ylims = []
    for ax1 in axes:
        for ax in ax1:
            ylims.append(ax.get_ylim()[1])
    max_y_lim = max(ylims)

    for ax1 in axes:
        for ax in ax1:
            ax.set_ylim([0, max_y_lim])
            ax.set_ylabel('Pieces of Music')

    for i in range(len(bar_color)):
        patches1[i].set_facecolor(bar_color[i])
        patches2[i].set_facecolor(bar_color[i])
        patches3[i].set_facecolor(bar_color[i])
        patches4[i].set_facecolor(bar_color[i])
        patches5[i].set_facecolor(bar_color[i])
        patches6[i].set_facecolor(bar_color[i])


    plt.show()

    #color for all subplots