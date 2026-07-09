import json
import os
from collections import Counter


class Analyzer:

    def analyze(self, processed_folder):

        results = []

        # ----------------------------
        # Load all processed JSON files
        # ----------------------------
        for file in os.listdir(processed_folder):

            if not file.endswith(".json"):
                continue

            filepath = os.path.join(processed_folder, file)

            with open(filepath, "r", encoding="utf-8") as f:
                results.append(json.load(f))

        print(f"\n📊 Loaded {len(results)} applications.\n")

        # ----------------------------
        # Statistics
        # ----------------------------
        auth_counter = Counter()
        api_counter = Counter()
        self_serve_counter = Counter()
        buildability_counter = Counter()
        category_counter = Counter()
        blocker_counter = Counter()

        confidence_scores = []
        verified_count = 0
        total_corrections = 0

        for app in results:

            auth_counter[app.get("auth_method", "Unknown")] += 1

            api_counter[app.get("api_type", "Unknown")] += 1

            self_serve_counter[app.get("self_serve", "Unknown")] += 1

            buildability_counter[
                app.get("buildability_verdict", "Unknown")
            ] += 1

            category_counter[
                app.get("category", "Unknown")
            ] += 1

            blocker = app.get("main_blocker")

            if blocker and blocker.lower() != "none":
                blocker_counter[blocker] += 1

            if "confidence" in app:
                confidence_scores.append(app["confidence"])

            if app.get("verified") is True:
                verified_count += 1
                
            total_corrections += app.get("corrections", 0)

        statistics = {

            "total_apps": len(results),

            "authentication": dict(auth_counter),

            "api_types": dict(api_counter),

            "self_serve": dict(self_serve_counter),

            "buildability": dict(buildability_counter),

            "categories": dict(category_counter),

            "top_blockers": dict(blocker_counter),

            "average_confidence":
                round(sum(confidence_scores) / len(confidence_scores), 2)
                if confidence_scores else None,

            "verified_apps": verified_count,
            "total_corrections": total_corrections
        }

        insights = self.generate_insights(statistics)

        return {
            "statistics": statistics,
            "insights": insights
        }

    # -------------------------------------------------

    def generate_insights(self, statistics):

        insights = []

        auth = statistics["authentication"]
        if auth:
            top_auth = max(auth, key=auth.get)
            insights.append({
                "icon": "🔑",
                "heading": "Authentication",
                "desc": f"{top_auth} is the dominant authentication method."
            })

        api = statistics["api_types"]
        if api:
            top_api = max(api, key=api.get)
            insights.append({
                "icon": "🌐",
                "heading": "API Type",
                "desc": f"{top_api} is the most common API type."
            })

        buildability = statistics["buildability"]
        if "Yes" in buildability:
            insights.append({
                "icon": "🏗️",
                "heading": "Agent Readiness",
                "desc": f"{buildability['Yes']} applications appear immediately buildable."
            })

        blockers = statistics["top_blockers"]
        if blockers:
            biggest = max(blockers, key=blockers.get)
            insights.append({
                "icon": "🚫",
                "heading": "Common Blockers",
                "desc": f"The most common blocker is '{biggest}'."
            })

        insights.append({
            "icon": "🚀",
            "heading": "Integration Potential",
            "desc": "Most applications expose public APIs, making them strong candidates for agent integrations."
        })

        insights.append({
            "icon": "💡",
            "heading": "MCP Opportunities",
            "desc": "Native MCP support appears limited, representing an opportunity for custom Composio toolkits."
        })

        return insights
