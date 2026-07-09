import json
from utils import load_apps, save_json, apply_verification
from discovery import DiscoveryAgent
from researcher import ResearchAgent
from verifier import VerificationAgent
from analyzer import Analyzer
from report import ReportGenerator


class ResearchPipeline:

    def __init__(self):
        print("🚀 Initializing Research Pipeline...")

        self.discovery_agent = DiscoveryAgent()
        self.research_agent = ResearchAgent()
        self.verification_agent = VerificationAgent()
        self.analyzer = Analyzer()
        self.report = ReportGenerator()

    def run(self):

        print("📂 Loading apps...")

        apps = load_apps("data/apps.csv")

        print(f"✅ Loaded {len(apps)} applications\n")

        for app in apps:

            # -----------------------
            # Discovery
            # -----------------------
            discovery_result = self.discovery_agent.discover(
                app["app"],
                app["seed_url"]
            )

            if not discovery_result:
                print("❌ Discovery failed.\n")
                continue

            # -----------------------
            # Research
            # -----------------------
            research_result = self.research_agent.research(
                discovery_result
            )

            if not research_result:
                print("❌ Research failed.\n")
                continue

            print("\n📄 Research Result:\n")
            print(research_result)

            # -----------------------
            # Verification
            # -----------------------
            verification_result = self.verification_agent.verify(
                discovery_result,
                research_result
            )

            if not verification_result:
                print("❌ Verification failed.\n")
                continue

            print("\n✅ Verification Result:\n")
            print(verification_result)

            # -----------------------
            # Save Research JSON
            # -----------------------
            filename = (
                f"data/processed/"
                f"{app['app'].lower().replace(' ', '_')}.json"
            )

            final_result = apply_verification(research_result, verification_result)
            save_json(final_result, filename)

            print(f"\n💾 Saved to {filename}\n")

        analysis = self.analyzer.analyze(
            "data/processed"
        )

        print("\n📈 Analysis\n")

        print(json.dumps(
            analysis,
            indent=4
        ))

        save_json(
            analysis,
            "output/analysis.json"
        )

        self.report.build_report(
            analysis
        )

        print("🎉 Pipeline Completed!")