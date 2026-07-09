import json
import os
import shutil


class ReportGenerator:

    def __init__(self):
        self.template_path = "templates/report.html"
        self.output_path = "output/report.html"

    # --------------------------------------------------

    def build_report(self, analysis):
        apps = self.load_processed_apps()
        html = self.load_template()

        html = html.replace("{{RESEARCH_ROWS}}", self.generate_rows(apps))
        html = html.replace("{{SUMMARY_CARDS}}", self.generate_summary(analysis))
        html = html.replace("{{BENCHMARKS}}", self.generate_benchmarks())
        html = html.replace("{{INSIGHTS}}", self.generate_insights(analysis["insights"]))
        html = html.replace("{{VERIFICATION}}", self.generate_verification(apps))
        html = html.replace("{{PIPELINE}}", self.generate_pipeline())
        html = html.replace("{{ARCHITECTURE}}", self.generate_architecture())

        os.makedirs("output", exist_ok=True)

        # Copy static assets for a styled professional report
        if os.path.exists("templates/style.css"):
            shutil.copy("templates/style.css", "output/style.css")
        if os.path.exists("templates/script.js"):
            shutil.copy("templates/script.js", "output/script.js")

        with open(self.output_path, "w", encoding="utf-8") as file:
            file.write(html)

        print("🌐 HTML report generated.")

    # --------------------------------------------------

    def load_template(self):
        with open(self.template_path, "r", encoding="utf-8") as file:
            return file.read()

    # --------------------------------------------------

    def load_processed_apps(self):
        apps = []
        folder = "data/processed"
        for filename in os.listdir(folder):
            if filename.endswith(".json"):
                with open(os.path.join(folder, filename), "r", encoding="utf-8") as file:
                    apps.append(json.load(file))
        return apps

    # --------------------------------------------------

    def generate_rows(self, apps):
        rows = ""
        for app in apps:
            rows += f"""
<tr>
<td>{app.get("app","-")}</td>
<td>{app.get("category","-")}</td>
<td>{app.get("description","-")}</td>
<td>{app.get("auth_method","-")}</td>
<td>{app.get("self_serve","-")}</td>
<td>{app.get("api_type","-")}</td>
<td>{app.get("api_coverage","-")}</td>
<td>{app.get("mcp_support","-")}</td>
<td>{app.get("buildability_verdict","-")}</td>
<td>{app.get("main_blocker","-")}</td>
<td>{app.get("confidence","-")}</td>
<td>{"✅" if app.get("verified") else "❌"}</td>
<td>
<a href="{app.get("evidence", {}).get("authentication","#")}" target="_blank">Docs</a>
</td>
<td>
<a href="{app.get("evidence", {}).get("api","#")}" target="_blank">Docs</a>
</td>
<td>
<a href="{app.get("evidence", {}).get("pricing","#")}" target="_blank">Docs</a>
</td>
</tr>
"""
        return rows

    # --------------------------------------------------

    def generate_summary(self, analysis):
        stats = analysis["statistics"]
        confidence = stats.get("average_confidence")
        conf_str = "-" if confidence is None else f"{confidence}%"
        
        total_apps = stats.get("total_apps", 0)
        verified_apps = stats.get("verified_apps", 0)
        needs_review = total_apps - verified_apps
        
        return f"""
<div class="summary-card">
    <h3>Total Applications</h3>
    <h1>{total_apps}</h1>
</div>
<div class="summary-card">
    <h3>Categories</h3>
    <h1>{len(stats.get("categories", {}))}</h1>
</div>
<div class="summary-card">
    <h3>Buildable</h3>
    <h1>{stats.get("buildability", {}).get("Yes", 0)}</h1>
</div>
<div class="summary-card">
    <h3>Average Confidence</h3>
    <h1>{conf_str}</h1>
</div>
<div class="summary-card">
    <h3>Verified Applications</h3>
    <h1>{verified_apps}</h1>
</div>
<div class="summary-card">
    <h3>Needs Review</h3>
    <h1>{needs_review}</h1>
</div>
"""

    # --------------------------------------------------

    def generate_benchmarks(self):
        return """
<div class="benchmark-card">
    <h3>Authentication Distribution</h3>
    <div id="authChart"></div>
</div>
<div class="benchmark-card">
    <h3>API Types</h3>
    <div id="apiChart"></div>
</div>
<div class="benchmark-card">
    <h3>Buildability</h3>
    <div id="buildChart"></div>
</div>
<div class="benchmark-card">
    <h3>Categories</h3>
    <div id="categoryChart"></div>
</div>
"""

    # --------------------------------------------------

    def generate_insights(self, insights):
        html = ""
        for insight in insights:
            html += f"""
<div class="insight-card">
    <div class="insight-icon">{insight["icon"]}</div>
    <h3>{insight["heading"]}</h3>
    <p>{insight["desc"]}</p>
</div>
"""
        return html

    # --------------------------------------------------

    def generate_verification(self, apps):
        verified = sum(1 for app in apps if app.get("verified"))
        failed = len(apps) - verified
        corrections = sum(app.get("corrections", 0) for app in apps)
        
        confs = [app.get("confidence", 0) for app in apps if "confidence" in app]
        avg_conf = round(sum(confs) / len(confs), 2) if confs else "-"
        
        return f"""
<div class="summary-card">
    <h3>Verified</h3>
    <h1>{verified}</h1>
</div>
<div class="summary-card">
    <h3>Failed</h3>
    <h1>{failed}</h1>
</div>
<div class="summary-card">
    <h3>Corrections</h3>
    <h1>{corrections}</h1>
</div>
<div class="summary-card">
    <h3>Confidence</h3>
    <h1>{avg_conf}%</h1>
</div>
"""

    # --------------------------------------------------

    def generate_pipeline(self):
        return """
<svg width="800" height="150" viewBox="0 0 800 150" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="white" />
    <g transform="translate(50, 50)" font-family="Inter, sans-serif" font-size="14" font-weight="600" text-anchor="middle">
        
        <!-- Nodes -->
        <rect x="0" y="0" width="100" height="50" rx="8" fill="#f3f4f6" stroke="#d1d5db" />
        <text x="50" y="30" fill="#374151">Apps.csv</text>

        <path d="M 100 25 L 140 25" stroke="#9ca3af" stroke-width="2" marker-end="url(#arrow)"/>

        <rect x="140" y="0" width="120" height="50" rx="8" fill="#eef2ff" stroke="#a5b4fc" />
        <text x="200" y="30" fill="#4338ca">Discovery</text>

        <path d="M 260 25 L 300 25" stroke="#9ca3af" stroke-width="2" marker-end="url(#arrow)"/>

        <rect x="300" y="0" width="120" height="50" rx="8" fill="#eef2ff" stroke="#a5b4fc" />
        <text x="360" y="30" fill="#4338ca">Research</text>

        <path d="M 420 25 L 460 25" stroke="#9ca3af" stroke-width="2" marker-end="url(#arrow)"/>

        <rect x="460" y="0" width="120" height="50" rx="8" fill="#dcfce7" stroke="#86efac" />
        <text x="520" y="30" fill="#166534">Verification</text>
        
        <path d="M 580 25 L 620 25" stroke="#9ca3af" stroke-width="2" marker-end="url(#arrow)"/>

        <rect x="620" y="0" width="120" height="50" rx="8" fill="#fef3c7" stroke="#fcd34d" />
        <text x="680" y="30" fill="#92400e">Analyzer</text>
        
    </g>
    <defs>
        <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
            <path d="M0,0 L0,6 L9,3 z" fill="#9ca3af" />
        </marker>
    </defs>
</svg>
"""

    # --------------------------------------------------

    def generate_architecture(self):
        return """
<svg width="800" height="400" viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="white" />
    <g transform="translate(50, 50)" font-family="Inter, sans-serif" font-size="14">
        
        <rect x="0" y="0" width="700" height="300" rx="12" fill="#fafafa" stroke="#e5e7eb" stroke-dasharray="5,5"/>
        <text x="20" y="30" font-size="16" font-weight="700" fill="#6b7280">System Boundary (Agent Workflow)</text>

        <!-- Input -->
        <g transform="translate(50, 80)">
            <rect width="100" height="140" rx="8" fill="#f3f4f6" stroke="#d1d5db" />
            <text x="50" y="75" text-anchor="middle" font-weight="600" fill="#374151">Data Layer</text>
        </g>

        <!-- Core Engines -->
        <g transform="translate(250, 60)">
            <rect width="200" height="180" rx="8" fill="#eef2ff" stroke="#a5b4fc" />
            <text x="100" y="30" text-anchor="middle" font-weight="700" fill="#4338ca">Core Processing</text>
            
            <rect x="25" y="50" width="150" height="40" rx="4" fill="white" stroke="#c7d2fe"/>
            <text x="100" y="75" text-anchor="middle" font-weight="600" fill="#374151">Gemini Pro API</text>
            
            <rect x="25" y="110" width="150" height="40" rx="4" fill="white" stroke="#c7d2fe"/>
            <text x="100" y="135" text-anchor="middle" font-weight="600" fill="#374151">HTML Templates</text>
        </g>
        
        <!-- Output -->
        <g transform="translate(550, 80)">
            <rect width="100" height="140" rx="8" fill="#f3f4f6" stroke="#d1d5db" />
            <text x="50" y="75" text-anchor="middle" font-weight="600" fill="#374151">Presentation</text>
        </g>

        <!-- Connectors -->
        <path d="M 150 150 L 250 150" stroke="#9ca3af" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M 450 150 L 550 150" stroke="#9ca3af" stroke-width="2" marker-end="url(#arrow)"/>
        
    </g>
    <defs>
        <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
            <path d="M0,0 L0,6 L9,3 z" fill="#9ca3af" />
        </marker>
    </defs>
</svg>
"""