import Link from "next/link";

export default function HomePage() {
  return (
    <main className="home">
      <h1>AI ETL Analytics Platform</h1>
      <p className="home-subtitle">
        ETL pipelines, analytics, and AI-generated insights.
      </p>
      <Link href="/dashboard" className="home-link">
        Open Analytics Dashboard →
      </Link>
    </main>
  );
}
