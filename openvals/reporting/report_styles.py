def get_report_styles():
    return """
    <style>
        :root {
            --bg: #0b1020;
            --surface: #111827;
            --surface-soft: #172033;
            --card: #ffffff;
            --muted-card: #f8fafc;
            --text: #0f172a;
            --muted: #64748b;
            --border: #e5e7eb;
            --primary: #4f46e5;
            --primary-soft: #eef2ff;
            --success: #16a34a;
            --warning: #f59e0b;
            --danger: #dc2626;
            --info: #0284c7;
        }

        * {
            box-sizing: border-box;
        }

        body {
            font-family:
                Inter,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                Arial,
                sans-serif;
            background:
                radial-gradient(
                    circle at top left,
                    #1e1b4b 0,
                    #0f172a 28%,
                    #f8fafc 28%,
                    #f8fafc 100%
                );
            margin: 0;
            padding: 36px;
            color: var(--text);
        }

        .report-shell {
            max-width: 1440px;
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
            border-radius: 28px;
            padding: 28px;
            margin-bottom: 20px;
            box-shadow: 0 24px 50px rgba(15,23,42,0.28);
        }
        .hero + .grid {
            margin-top: 28px;
        }

        .hero-top {
            display: flex;
            justify-content: space-between;
            gap: 24px;
            align-items: flex-start;
        }

        .brand-row {
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 18px;
        }

        .brand-logo {
            width: 42px;
            height: 42px;
            border-radius: 12px;
            background: white;
            object-fit: contain;
            padding: 6px;
        }

        .brand-name {
            font-size: 15px;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #c7d2fe;
            font-weight: 700;
        }

        .hero h1 {
            margin: 0;
            font-size: 38px;
            line-height: 1.1;
            letter-spacing: -0.04em;
        }

        .hero-subtitle {
            margin-top: 14px;
            color: #cbd5e1;
            max-width: 760px;
            line-height: 1.7;
            font-size: 16px;
        }

        .hero-score {
            min-width: 240px;
            background: rgba(255,255,255,0.10);
            border: 1px solid rgba(255,255,255,0.18);
            border-radius: 22px;
            padding: 20px;
            backdrop-filter: blur(12px);
        }

        .hero-score-label {
            color: #cbd5e1;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 700;
        }

        .hero-score-value {
            font-size: 46px;
            font-weight: 800;
            margin-top: 8px;
            letter-spacing: -0.04em;
        }

        .hero-score-caption {
            color: #e0e7ff;
            margin-top: 6px;
            font-size: 14px;
        }

        .meta-row {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-top: 24px;
        }

        .pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(255,255,255,0.10);
            border: 1px solid rgba(255,255,255,0.16);
            color: #e0e7ff;
            padding: 8px 12px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 600;
        }

        .grid {
            display: grid;
            gap: 16px;
            margin-bottom: 20px;
        }

        .grid-4 {
            grid-template-columns: repeat(4, minmax(0, 1fr));
        }

        .grid-3 {
            grid-template-columns: repeat(3, minmax(0, 1fr));
        }

        .grid-2 {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }

        .card {
            background: rgba(255,255,255,0.96);
            padding: 22px;
            margin-bottom: 20px;
            border-radius: 22px;
            box-shadow: 0 10px 28px rgba(15,23,42,0.08);
            border: 1px solid rgba(226,232,240,0.9);
        }

        .card h2 {
            margin: 0 0 14px 0;
            color: #0f172a;
            letter-spacing: -0.02em;
            font-size: 22px;
        }

        .card h3 {
            margin-top: 18px;
            color: #1e293b;
            font-size: 16px;
        }

        .metric-card {
            background:
                linear-gradient(
                    180deg,
                    #ffffff,
                    #f8fafc
                );
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 18px;
            min-height: 132px;
            box-shadow: 0 8px 20px rgba(15,23,42,0.05);
        }

        .metric-label {
            color: var(--muted);
            font-size: 13px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .metric-value {
            margin-top: 8px;
            font-size: 28px;
            font-weight: 800;
            color: #0f172a;
            letter-spacing: -0.04em;
        }

        .metric-note {
            margin-top: 8px;
            color: var(--muted);
            font-size: 13px;
            line-height: 1.5;
        }

        .metric-box {
            display: inline-block;
            margin-right: 14px;
            margin-top: 10px;
            padding: 16px;
            min-width: 135px;
            background: var(--muted-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            text-align: center;
        }

        .metric-box b {
            font-size: 13px;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .metric-box br + * {
            font-size: 22px;
            font-weight: 800;
        }

        .highlight {
            color: var(--primary);
            font-weight: 800;
        }

        .trust {
            font-size: 18px;
            font-weight: 800;
            margin-top: 14px;
            padding: 12px 14px;
            background: var(--primary-soft);
            border-radius: 14px;
            display: inline-block;
        }

        .deployment {
            font-size: 18px;
            font-weight: 800;
            margin-bottom: 10px;
            color: var(--primary);
        }

        .success {
            border-left: 6px solid var(--success);
        }

        .warning {
            border-left: 6px solid var(--danger);
        }

        .info {
            border-left: 6px solid var(--info);
        }

        .chart {
            width: 100%;
            max-width: 920px;
            margin-top: 18px;
            border-radius: 18px;
            border: 1px solid var(--border);
            background: white;
            padding: 8px;
        }

        table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin-top: 15px;
            overflow: hidden;
            border: 1px solid var(--border);
            border-radius: 16px;
        }

        th {
            background: #0f172a;
            color: white;
            padding: 14px;
            text-align: center;
            font-size: 13px;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        td {
            padding: 14px;
            border-bottom: 1px solid var(--border);
            text-align: center;
            background: white;
            font-size: 14px;
        }

        tr:last-child td {
            border-bottom: none;
        }

        tr:hover td {
            background: #f8fafc;
        }

        ul {
            margin-top: 8px;
            line-height: 1.8;
            color: #334155;
        }

        p {
            line-height: 1.7;
            color: #334155;
        }

        hr {
            border: none;
            border-top: 1px solid var(--border);
            margin: 22px 0;
        }

        .footer {
            text-align: center;
            margin-top: 42px;
            color: #64748b;
            font-size: 14px;
        }

        .section-label {
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 12px;
            font-weight: 800;
            margin-bottom: 8px;
        }

        @media (max-width: 960px) {
            body {
                padding: 18px;
            }

            .hero-top {
                flex-direction: column;
            }

            .hero-score {
                width: 100%;
            }

            .grid-4,
            .grid-3,
            .grid-2 {
                grid-template-columns: 1fr;
            }

            .hero h1 {
                font-size: 30px;
            }
        }
    </style>
    """