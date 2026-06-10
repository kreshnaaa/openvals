from datetime import datetime
import html
import os


# =========================================================
# SAFE HELPERS
# =========================================================

def safe_text(value):

    if value is None:
        return ""

    return html.escape(str(value))


def safe_score(value, digits=3):

    try:
        return f"{float(value):.{digits}f}"
    except Exception:
        return "0.000"


def status_badge(value, inverse=False):

    try:
        value = float(value)
    except Exception:
        value = 0.0

    if inverse:
        if value <= 0.20:
            return "🟢 Low"
        elif value <= 0.50:
            return "🟡 Medium"
        return "🔴 High"

    if value >= 0.80:
        return "🟢 High"
    elif value >= 0.60:
        return "🟡 Medium"
    return "🔴 Low"


# =========================================================
# SAMPLE CARD
# =========================================================

def build_sample_card(
    model_name,
    sample,
    index
):

    prompt = safe_text(
        sample.get(
            "prompt",
            sample.get("input", "")
        )
    )

    expected = safe_text(
        sample.get(
            "expected",
            sample.get("expected_output", "")
        )
    )

    output = safe_text(
        sample.get(
            "output",
            ""
        )
    )

    accuracy = sample.get("accuracy", 0)
    semantic = sample.get("semantic", 0)
    factuality = sample.get("factuality", 0)
    hallucination = sample.get("hallucination", 0)
    safety = sample.get("safety", 0)
    latency = sample.get("latency", 0)

    return f"""
    <div class="sample-card">

        <div class="sample-header">

            <div>
                <div class="sample-title">
                    Sample #{index}
                </div>

                <div class="sample-model">
                    Model: <b>{safe_text(model_name)}</b>
                </div>
            </div>

            <div class="sample-risk">
                HPI: {status_badge(
                    hallucination,
                    inverse=True
                )}
            </div>

        </div>

        <div class="sample-grid">

            <div class="sample-block">
                <div class="label">Prompt</div>
                <div class="text-block">
                    {prompt}
                </div>
            </div>

            <div class="sample-block">
                <div class="label">Expected Output</div>
                <div class="text-block">
                    {expected}
                </div>
            </div>

            <div class="sample-block output-block">
                <div class="label">Model Output</div>
                <div class="text-block">
                    {output}
                </div>
            </div>

        </div>

        <div class="metric-row">

            <div class="mini-metric">
                <span>Accuracy</span>
                <b>{safe_score(accuracy)}</b>
                <small>{status_badge(accuracy)}</small>
            </div>

            <div class="mini-metric">
                <span>Semantic</span>
                <b>{safe_score(semantic)}</b>
                <small>{status_badge(semantic)}</small>
            </div>

            <div class="mini-metric">
                <span>Factuality</span>
                <b>{safe_score(factuality)}</b>
                <small>{status_badge(factuality)}</small>
            </div>

            <div class="mini-metric">
                <span>Safety</span>
                <b>{safe_score(safety)}</b>
                <small>{status_badge(safety)}</small>
            </div>

            <div class="mini-metric">
                <span>HPI</span>
                <b>{safe_score(hallucination)}</b>
                <small>{status_badge(
                    hallucination,
                    inverse=True
                )}</small>
            </div>

            <div class="mini-metric">
                <span>Latency</span>
                <b>{safe_score(latency, 2)} ms</b>
                <small>Runtime</small>
            </div>

        </div>

    </div>
    """


# =========================================================
# STYLES
# =========================================================

def get_sample_report_styles():

    return """
    <style>
        :root {
            --bg: #f8fafc;
            --text: #0f172a;
            --muted: #64748b;
            --border: #e5e7eb;
            --primary: #4f46e5;
            --surface: #ffffff;
            --soft: #f1f5f9;
            --danger: #dc2626;
            --success: #16a34a;
            --warning: #f59e0b;
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            padding: 32px;
            font-family:
                Inter,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                Arial,
                sans-serif;
            background:
                linear-gradient(
                    180deg,
                    #eef2ff,
                    #f8fafc
                );
            color: var(--text);
        }

        .shell {
            max-width: 1280px;
            margin: 0 auto;
        }

        .hero {
            background:
                linear-gradient(
                    135deg,
                    #0f172a,
                    #1e1b4b,
                    #312e81
                );
            color: white;
            border-radius: 26px;
            padding: 30px;
            margin-bottom: 26px;
            box-shadow: 0 20px 50px rgba(15,23,42,0.20);
        }

        .hero h1 {
            margin: 0;
            font-size: 34px;
            letter-spacing: -0.04em;
        }

        .hero p {
            color: #cbd5e1;
            margin-top: 10px;
            max-width: 780px;
            line-height: 1.7;
        }

        .meta {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-top: 20px;
        }

        .pill {
            padding: 8px 12px;
            border-radius: 999px;
            background: rgba(255,255,255,0.10);
            border: 1px solid rgba(255,255,255,0.16);
            color: #e0e7ff;
            font-size: 13px;
            font-weight: 600;
        }

        .model-section {
            margin-bottom: 34px;
        }

        .model-title {
            margin: 0 0 14px 0;
            font-size: 22px;
            letter-spacing: -0.02em;
        }

        .sample-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 22px;
            padding: 22px;
            margin-bottom: 18px;
            box-shadow: 0 10px 28px rgba(15,23,42,0.06);
        }

        .sample-header {
            display: flex;
            justify-content: space-between;
            gap: 16px;
            align-items: center;
            margin-bottom: 18px;
        }

        .sample-title {
            font-size: 18px;
            font-weight: 800;
        }

        .sample-model {
            color: var(--muted);
            margin-top: 4px;
            font-size: 14px;
        }

        .sample-risk {
            background: var(--soft);
            border: 1px solid var(--border);
            padding: 10px 12px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 700;
        }

        .sample-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 14px;
            margin-bottom: 16px;
        }

        .output-block {
            grid-column: span 2;
        }

        .sample-block {
            border: 1px solid var(--border);
            border-radius: 16px;
            background: #f8fafc;
            padding: 14px;
        }

        .label {
            font-size: 12px;
            font-weight: 800;
            color: var(--muted);
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .text-block {
            white-space: pre-wrap;
            line-height: 1.6;
            color: #1e293b;
            font-size: 14px;
        }

        .metric-row {
            display: grid;
            grid-template-columns: repeat(6, minmax(0, 1fr));
            gap: 12px;
        }

        .mini-metric {
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 14px;
            text-align: center;
        }

        .mini-metric span {
            display: block;
            color: var(--muted);
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .mini-metric b {
            display: block;
            font-size: 22px;
            margin-top: 8px;
        }

        .mini-metric small {
            display: block;
            color: var(--muted);
            margin-top: 6px;
            font-size: 12px;
        }

        .footer {
            text-align: center;
            color: var(--muted);
            margin-top: 40px;
            font-size: 14px;
        }

        @media (max-width: 900px) {
            body {
                padding: 18px;
            }

            .sample-grid {
                grid-template-columns: 1fr;
            }

            .output-block {
                grid-column: span 1;
            }

            .metric-row {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .sample-header {
                flex-direction: column;
                align-items: flex-start;
            }
        }
    </style>
    """


# =========================================================
# GENERATE SAMPLE REPORT
# =========================================================

def generate_sample_report(
    results,
    output_file="outputs/sample_report.html"
):

    output_dir = os.path.dirname(
        os.path.abspath(output_file)
    )

    if output_dir:
        os.makedirs(
            output_dir,
            exist_ok=True
        )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    model_sections = ""

    for model_name, model_result in results.items():

        samples = model_result.get(
            "samples",
            []
        )

        cards = ""

        for index, sample in enumerate(
            samples,
            start=1
        ):

            cards += build_sample_card(
                model_name,
                sample,
                index
            )

        if not cards:

            cards = """
            <div class="sample-card">
                No sample-level records available.
            </div>
            """

        model_sections += f"""
        <div class="model-section">

            <h2 class="model-title">
                Model: {safe_text(model_name)}
            </h2>

            {cards}

        </div>
        """

    html_output = f"""
    <html>

    <head>
        <title>
            OpenVals Sample-Level Evaluation Report
        </title>

        {get_sample_report_styles()}
    </head>

    <body>

        <div class="shell">

            <div class="hero">

                <h1>
                    Sample-Level Evaluation Drilldown
                </h1>

                <p>
                    Detailed prompt-level evaluation across model outputs,
                    expected answers, factuality, hallucination probability,
                    safety, semantic alignment, and latency.
                </p>

                <div class="meta">
                    <div class="pill">
                        Generated: {timestamp}
                    </div>

                    <div class="pill">
                        Models: {len(results)}
                    </div>
                </div>

            </div>

            {model_sections}

            <div class="footer">
                Built with OpenVals • Detailed Evaluation Report
                <br><br>
                Developed by DrPinnacle
            </div>

        </div>

    </body>

    </html>
    """

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(html_output)

    print(
        f"✅ Detailed report generated: {output_file}"
    )