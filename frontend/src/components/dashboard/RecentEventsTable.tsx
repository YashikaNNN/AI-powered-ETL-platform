import type { SampleEvent } from "@/types/analytics";

interface RecentEventsTableProps {
  events: SampleEvent[];
  total: number;
}

function formatTimestamp(value: string): string {
  return new Intl.DateTimeFormat("en-US", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function formatAmount(value: string): string {
  const amount = Number.parseFloat(value);
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(Number.isNaN(amount) ? 0 : amount);
}

export function RecentEventsTable({ events, total }: RecentEventsTableProps) {
  return (
    <section className="dashboard-panel">
      <div className="dashboard-panel-header">
        <h2 className="dashboard-panel-title">Recent Events</h2>
        <span className="dashboard-muted">{total} total</span>
      </div>

      {events.length === 0 ? (
        <p className="dashboard-muted">No events to display.</p>
      ) : (
        <div className="dashboard-table-wrap">
          <table className="dashboard-table">
            <thead>
              <tr>
                <th>Event ID</th>
                <th>User</th>
                <th>Type</th>
                <th>Timestamp</th>
                <th>Amount</th>
              </tr>
            </thead>
            <tbody>
              {events.map((event) => (
                <tr key={event.id}>
                  <td>{event.event_id}</td>
                  <td>{event.user_id}</td>
                  <td>
                    <span className="dashboard-badge">{event.event_type}</span>
                  </td>
                  <td>{formatTimestamp(event.event_timestamp)}</td>
                  <td>{formatAmount(event.amount)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
