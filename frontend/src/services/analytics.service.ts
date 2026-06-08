import { apiFetch } from "@/lib/api-client";
import type {
  AnalyticsSummary,
  InsightRequest,
  InsightResponse,
  PaginatedEventsResponse,
} from "@/types/analytics";

export const analyticsService = {
  getSummary: () => apiFetch<AnalyticsSummary>("/analytics/summary"),

  getEvents: (page = 1, pageSize = 10) =>
    apiFetch<PaginatedEventsResponse>(
      `/analytics/events?page=${page}&page_size=${pageSize}`
    ),

  generateInsight: (payload: InsightRequest) =>
    apiFetch<InsightResponse>("/analytics/insights", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
};
