"use client";

import { useCallback, useEffect, useState } from "react";

import { AIInsightsPanel } from "@/components/dashboard/AIInsightsPanel";
import { EventTypeCounts } from "@/components/dashboard/EventTypeCounts";
import { RecentEventsTable } from "@/components/dashboard/RecentEventsTable";
import { SummaryCards } from "@/components/dashboard/SummaryCards";
import { analyticsService } from "@/services/analytics.service";
import type { AnalyticsSummary, SampleEvent } from "@/types/analytics";

type DashboardState =
  | { status: "loading" }
  | { status: "error"; message: string }
  | {
      status: "success";
      summary: AnalyticsSummary;
      events: SampleEvent[];
      totalEvents: number;
    };

export function Dashboard() {
  const [state, setState] = useState<DashboardState>({ status: "loading" });

  const loadDashboard = useCallback(async () => {
    setState({ status: "loading" });

    try {
      const [summary, eventsResponse] = await Promise.all([
        analyticsService.getSummary(),
        analyticsService.getEvents(1, 10),
      ]);

      setState({
        status: "success",
        summary,
        events: eventsResponse.items,
        totalEvents: eventsResponse.total,
      });
    } catch (error) {
      const message =
        error instanceof Error
          ? error.message
          : "Failed to load analytics dashboard";
      setState({ status: "error", message });
    }
  }, []);

  useEffect(() => {
    loadDashboard();
  }, [loadDashboard]);

  return (
    <main className="dashboard">
      <header className="dashboard-header">
        <div>
          <h1>Analytics Dashboard</h1>
          <p className="dashboard-subtitle">
            Live metrics from analytics.sample_events
          </p>
        </div>
        <button
          type="button"
          className="dashboard-button"
          onClick={loadDashboard}
          disabled={state.status === "loading"}
        >
          {state.status === "loading" ? "Refreshing…" : "Refresh"}
        </button>
      </header>

      {state.status === "loading" && (
        <div className="dashboard-state" role="status">
          <div className="dashboard-spinner" aria-hidden="true" />
          <p>Loading analytics…</p>
        </div>
      )}

      {state.status === "error" && (
        <div className="dashboard-state dashboard-state-error" role="alert">
          <p>{state.message}</p>
          <button
            type="button"
            className="dashboard-button"
            onClick={loadDashboard}
          >
            Retry
          </button>
        </div>
      )}

      {state.status === "success" && (
        <>
          <SummaryCards summary={state.summary} />
          <AIInsightsPanel />
          <div className="dashboard-grid">
            <EventTypeCounts counts={state.summary.by_event_type} />
            <RecentEventsTable
              events={state.events}
              total={state.totalEvents}
            />
          </div>
        </>
      )}
    </main>
  );
}
