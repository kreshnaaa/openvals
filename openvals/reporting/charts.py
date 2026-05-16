import os
import matplotlib.pyplot as plt
import numpy as np

# =========================================================
# CHART GENERATION ENGINE
# =========================================================

def ensure_chart_dir(charts_dir):

    os.makedirs(charts_dir, exist_ok=True)


# =========================================================
# RADAR CHART
# =========================================================

def generate_radar_chart(results, charts_dir):

    ensure_chart_dir(charts_dir)

    labels = [
        "Accuracy",
        "Semantic",
        "Reliability",
        "Safety",
        "Consistency"
    ]

    first_model = list(results.keys())[0]

    metrics = results[first_model]["metrics"]

    values = [
        metrics.get("accuracy", 0),
        metrics.get("semantic", 0),
        metrics.get("reliability", 0),
        metrics.get("safety", 0),
        metrics.get("consistency", 0)
    ]

    values += values[:1]

    angles = np.linspace(
        0,
        2 * np.pi,
        len(labels),
        endpoint=False
    ).tolist()

    angles += angles[:1]

    fig, ax = plt.subplots(
        figsize=(6, 6),
        subplot_kw=dict(polar=True)
    )

    ax.plot(
        angles,
        values,
        linewidth=2
    )

    ax.fill(
        angles,
        values,
        alpha=0.25
    )

    ax.set_xticks(angles[:-1])

    ax.set_xticklabels(labels)

    plt.title(
        f"{first_model} Metric Radar"
    )

    output_path = os.path.join(
        charts_dir,
        "radar_chart.png"
    )

    plt.savefig(
        output_path,
        bbox_inches="tight"
    )

    plt.close()

    return output_path


# =========================================================
# LATENCY CHART
# =========================================================

def generate_latency_chart(results, charts_dir):

    ensure_chart_dir(charts_dir)

    models = list(results.keys())

    latency = [
        results[m]["metrics"].get(
            "latency",
            0
        )
        for m in models
    ]

    plt.figure(figsize=(8, 5))

    plt.bar(models, latency)

    plt.title("Latency Comparison")

    plt.ylabel("Latency (ms)")

    plt.xlabel("Models")

    output_path = os.path.join(
        charts_dir,
        "latency_chart.png"
    )

    plt.savefig(
        output_path,
        bbox_inches="tight"
    )

    plt.close()

    return output_path


# =========================================================
# DRS CHART
# =========================================================

def generate_drs_chart(results, charts_dir):

    ensure_chart_dir(charts_dir)

    models = list(results.keys())

    drs_scores = [
        results[m].get(
            "drs_score",
            0
        )
        for m in models
    ]

    plt.figure(figsize=(8, 5))

    plt.bar(models, drs_scores)

    plt.title("DRS Score Comparison")

    plt.ylabel("DRS Score")

    plt.xlabel("Models")

    output_path = os.path.join(
        charts_dir,
        "drs_chart.png"
    )

    plt.savefig(
        output_path,
        bbox_inches="tight"
    )

    plt.close()

    return output_path


# =========================================================
# GENERATE ALL CHARTS
# =========================================================

def generate_all_charts(results, charts_dir):

    radar = generate_radar_chart(
        results,
        charts_dir
    )

    latency = generate_latency_chart(
        results,
        charts_dir
    )

    drs = generate_drs_chart(
        results,
        charts_dir
    )

    return {
        "radar_chart": radar,
        "latency_chart": latency,
        "drs_chart": drs
    }