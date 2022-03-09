import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter


def main():

    # Create figure and axis
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))

    # Plot bar charts
    axs[0][0].bar([1.4, 2], [5.24, 5.29], width=0.6, yerr=0.04, ecolor='black',
                  error_kw=dict(lw=2, capsize=15, capthick=2),
                  color=['#3f5796', '#aebde4'], edgecolor='k')
    bars = axs[0][1].bar([1.4, 2], [5.26, 5.125], width=0.6, yerr=0.04,
                         error_kw=dict(lw=2, capsize=15, capthick=2),
                         color=['#3f5796', '#aebde4'], ecolor='black',
                         edgecolor='k')
    axs[1][0].bar([1.4, 2], [1.755, 1.69], width=0.6, yerr=0.02,
                  error_kw=dict(lw=2, capsize=15, capthick=2),  ecolor='black',
                  color=['#3f5796', '#aebde4'], edgecolor='k')
    axs[1][0].invert_yaxis()
    axs[1][1].bar([1.4, 2], [1.735, 1.765], width=0.6, yerr=0.02,
                  error_kw=dict(lw=2, capsize=15, capthick=2), ecolor='black',
                  color=['#3f5796', '#aebde4'], edgecolor='k')
    axs[1][1].invert_yaxis()

    # Remove axes, ticks etc that are not needed
    for ax in axs.flatten():
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.tick_params(right=False, top=False, bottom=False)
        ax.set(xticklabels=[])

    # Ensure same scales on top and bottom plots
    axs[0][1].set_ylim(axs[0][0].get_ylim())
    axs[1][1].set_ylim(axs[1][0].get_ylim())

    # Remove y-axes from right plots
    for ax in [axs[0][1], axs[1][1]]:
        ax.spines['left'].set_visible(False)
        ax.tick_params(left=False)
        ax.set(yticklabels=[])

    # Set axes labels
    axs[0][0].set_xlabel('Negativity Reduced', fontsize=18)
    axs[0][1].set_xlabel('Positivity Reduced', fontsize=18)
    axs[0][0].set_ylabel('Positive Words (per cent)', fontsize=18)
    axs[1][0].set_ylabel('Negative Words (per cent)', fontsize=18)

    # Format y-axis on first plot
    axs[0][0].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    # Create legend for top right plot
    axs[0][1].legend(bars, ['Control', 'Experimental'], loc='upper right',
                     bbox_to_anchor=(1, 1.05))

    # Save figure
    plt.tight_layout()
    fig.savefig('emotions_bar.png')
    plt.close()


if __name__ == "__main__":
    main()
