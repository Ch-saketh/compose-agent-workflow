import json
import os
import shutil


class ReportGenerator:

    def __init__(self):
        self.template_path = "templates/report.html"
        self.output_path = "output/report.html"

    # ---------------------------------------------------------------------------------

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

    # -------------------------------------------------------------------------------------------

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
        
        return f"""
<div class="summary-card">
    <h3>Total Applications</h3>
    <h1>{stats.get("total_apps", 0)}</h1>
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
<div>
<p>{insight}</p>
</div>
"""
        return html

    # --------------------------------------------------

    def generate_verification(self, apps):
        verified = sum(1 for app in apps if app.get("verified"))
        
        return f"""
<div class="summary-grid">
    <div class="summary-card">
        <h3>Verified Applications</h3>
        <h1>{verified}</h1>
    </div>
    <div class="summary-card">
        <h3>Needs Review</h3>
        <h1>{len(apps) - verified}</h1>
    </div>
</div>
"""

    # --------------------------------------------------

    def generate_pipeline(self):
        return """
<div>Apps.csv</div>
<span>→</span>
<div>Research Agent</div>
<span>→</span>
<div>Verification</div>
<span>→</span>
<div>Analyzer</div>
<span>→</span>
<div>HTML Report</div>
"""

    # --------------------------------------------------

    def generate_architecture(self):
        return """
<div>Apps.csv</div>
<span>→</span>
<div>Research</div>
<span>→</span>
<div>Verification</div>
<span>→</span>
<div>Analyzer</div>
<span>→</span>
<div>HTML</div>
"""