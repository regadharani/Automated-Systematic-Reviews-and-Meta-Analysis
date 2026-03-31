import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def create_forest_plot(df_extracted):
    """
    Generates a Forest Plot from extracted study statistics.
    Expects a DataFrame with 'Title' or 'ID', 'Effect_Size', 'CI_Lower', and 'CI_Upper'.
    """
    if df_extracted.empty:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.text(0.5, 0.5, "No data available for Meta-Analysis", ha='center', va='center')
        ax.axis('off')
        return fig
    
    # Ensure columns exist, fallback to Title if ID missing or vice versa
    labels = df_extracted['Title'].apply(lambda x: x[:30] + '...') if 'Title' in df_extracted.columns else df_extracted.index.astype(str)
    try:
        effect_sizes = df_extracted['Effect_Size'].astype(float)
        ci_lower = df_extracted['CI_Lower'].astype(float)
        ci_upper = df_extracted['CI_Upper'].astype(float)
    except KeyError:
        # If headers are mising, plot empty
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.text(0.5, 0.5, "Invalid data format for Forest Plot", ha='center', va='center')
        ax.axis('off')
        return fig

    # Errors for errorbar plot (distance from effect_size to bounds)
    err_lower = effect_sizes - ci_lower
    err_upper = ci_upper - effect_sizes
    errors = [err_lower, err_upper]

    # Initialize plot
    fig, ax = plt.subplots(figsize=(8, len(df_extracted) * 0.8 + 2))
    
    # Plot the Data
    y_pos = np.arange(len(df_extracted))
    ax.errorbar(effect_sizes, y_pos, xerr=errors, fmt='o', color='darkblue', 
                ecolor='steelblue', elinewidth=3, capsize=5, markersize=8)
    
    # Add vertical line for "No Effect" (typically 0 for mean difference, 1 for Odds Ratio)
    # We assume mean difference here (0)
    ax.axvline(x=0, color='red', linestyle='--', alpha=0.7, label='No Effect Line')

    # Formatting
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()  # top-down order
    ax.set_xlabel('Effect Size (e.g., Mean Difference or Log Odds)')
    ax.set_title('Forest Plot of Included Studies')
    
    # Calculate pooled effect size (Simple unweighted average for hackathon MVP)
    pooled_effect = effect_sizes.mean()
    ax.axvline(x=pooled_effect, color='green', linestyle='-', alpha=0.6, label=f'Pooled Effect ({pooled_effect:.2f})')
    
    ax.legend(loc='upper left')
    plt.tight_layout()
    
    return fig
