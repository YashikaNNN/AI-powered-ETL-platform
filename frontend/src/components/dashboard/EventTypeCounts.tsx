import type { EventTypeCount } from "@/types/analytics";

interface EventTypeCountsProps {
  counts: EventTypeCount[];
}

function formatEventType(eventType: string): string {
  return eventType.replace(/_/g, " ");
}

export function EventTypeCounts({ counts }: EventTypeCountsProps) {
  if (counts.length === 0) {
    return (
      <section className="dashboard-panel">
        <h2 className="dashboard-panel-title">Event Type Counts</h2>
        <p className="dashboard-muted">No events recorded yet.</p>
      </section>
    );
  }

  const maxCount = Math.max(...counts.map((c) => c.count));

  return (
    <section className="dashboard-panel">
      <h2 className="dashboard-panel-title">Event Type Counts</h2>
      <ul className="dashboard-breakdown">
        {counts.map((item) => (
          <li key={item.event_type} className="dashboard-breakdown-item">
            <div className="dashboard-breakdown-header">
              <span className="dashboard-breakdown-label">
                {formatEventType(item.event_type)}
              </span>
              <span className="dashboard-breakdown-count">{item.count}</span>
            </div>
            <div className="dashboard-breakdown-bar-track">
              <div
                className="dashboard-breakdown-bar-fill"
                style={{ width: `${(item.count / maxCount) * 100}%` }}
              />
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}
