def get_report_styles():
    return """
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f7fb;
            margin: 0;
            padding: 30px;
            color: #222;
        }

        h1 {
            margin-bottom: 5px;
        }

        h2 {
            margin-top: 0;
            color: #111827;
        }

        h3 {
            margin-top: 20px;
            color: #1f2937;
        }

        .subtitle {
            color: #666;
            margin-bottom: 30px;
        }

        .card {
            background: white;
            padding: 24px;
            margin-bottom: 25px;
            border-radius: 14px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border-left: 6px solid #4f46e5;
        }

        .warning {
            border-left: 6px solid #ef4444;
        }

        .success {
            border-left: 6px solid #16a34a;
        }

        .info {
            border-left: 6px solid #0284c7;
        }

        .highlight {
            color: #0b7a32;
            font-weight: bold;
        }

        .trust {
            font-size: 20px;
            font-weight: bold;
            margin-top: 10px;
        }

        .deployment {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #2563eb;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }

        th {
            background: #111827;
            color: white;
            padding: 14px;
            text-align: center;
        }

        td {
            padding: 12px;
            border-bottom: 1px solid #e5e7eb;
            text-align: center;
            background: white;
        }

        tr:hover td {
            background: #f9fafb;
        }

        ul {
            margin-top: 8px;
            line-height: 1.7;
        }

        .metric-box {
            display: inline-block;
            margin-right: 20px;
            margin-top: 10px;
            padding: 14px;
            min-width: 120px;
            background: #f9fafb;
            border-radius: 10px;
            text-align: center;
        }

        .chart {
            width: 100%;
            max-width: 850px;
            margin-top: 20px;
            border-radius: 10px;
            border: 1px solid #e5e7eb;
        }

        .footer {
            text-align: center;
            margin-top: 40px;
            color: #777;
            font-size: 14px;
        }

        hr {
            border: none;
            border-top: 1px solid #e5e7eb;
            margin: 20px 0;
        }
    </style>
    """