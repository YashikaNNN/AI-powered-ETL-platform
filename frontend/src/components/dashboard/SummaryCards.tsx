import type { AnalyticsSummary } from "@/types/analytics";

interface SummaryCardsProps {
  summary: AnalyticsSummary;
}

function formatRevenue(value: string): string {
  const amount = Number.parseFloat(value);
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(Number.isNaN(amount) ? 0 : amount);
}

export function SummaryCards({ summary }: SummaryCardsProps) {
  return (
    <div className="dashboard-cards">
      <article className="dashboard-card">
        <p className="dashboard-card-label">Total Events</p>
        <p className="dashboard-card-value">{summary.total_events}</p>
      </article>
      <article className="dashboard-card">
        <p className="dashboard-card-label">Total Revenue</p>
        <p className="dashboard-card-value">
          {formatRevenue(summary.total_revenue)}
        </p>
      </article>
      <article className="dashboard-card">
        <p className="dashboard-card-label">Event Types</p>
        <p className="dashboard-card-value">
          {summary.by_event_type.length}
        </p>
      </article>
    </div>
  );
}
