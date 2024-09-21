import matplotlib.pyplot as plt

from music_file import fitness_scores


y_axis_range = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
bar_color = ["#ff0000", "#ff0000", "#ff0000", "#ff0000", "#ff0000", "#ff0000", "#ffa500", "#ffa500", "#3cb371", "#3cb371"]


def draw():
    fig, axes = plt.subplots(3, 3, figure=(12,4))
    plt.subplots_adjust(hspace = 0.4)
    fig.suptitle("Scores of Generated Music Pieces!!")

    #subplot 1
    _, _, patches1 = axes[0][0].hist(fitness_scores["overall_score"], bins=y_axis_range, edgecolor='black', color='orange')
    axes[0][0].set_title('Scores of Generated Music Pieces (Overall)')
    axes[0][0].set_xlabel('Overall Score Value')

    #subplot 2
    _, _, patches2 = axes[1][0].hist(fitness_scores["note_rest_ratio"], bins=y_axis_range, edgecolor='black')
    axes[1][0].set_title('Scores of Generated Music Pieces (note_rest_ratio)')
    axes[1][0].set_xlabel('Data1 Score Value')

    #subplot 3
    _, _, patches3 = axes[1][1].hist(fitness_scores["note_length_ratio"], bins=y_axis_range, edgecolor='black')
    axes[1][1].set_title('Scores of Generated Music Pieces (note_length_ratio)')
    axes[1][1].set_xlabel('Data2 Score Value')

    #subplot 4
    _, _, patches4 = axes[1][2].hist(fitness_scores["contiguous_melody_ratio"], bins=y_axis_range, edgecolor='black')
    axes[1][2].set_title('Scores of Generated Music Pieces (contiguous_melody_ratio)')
    axes[1][2].set_xlabel('Data2 Score Value')

    #subplot 5
    _, _, patches5 = axes[2][0].hist(fitness_scores["interval_size_ratio"], bins=y_axis_range, edgecolor='black')
    axes[2][0].set_title('Scores of Generated Music Pieces (interval_size_ratio)')
    axes[2][0].set_xlabel('Data2 Score Value')

    #subplot 6
    _, _, patches6 = axes[2][1].hist(fitness_scores["allowable_interval_size"], bins=y_axis_range, edgecolor='black')
    axes[2][1].set_title('Scores of Generated Music Pieces (allowable_interval_size)')
    axes[2][1].set_xlabel('Data2 Score Value')
    
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