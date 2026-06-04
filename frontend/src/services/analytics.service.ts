import { apiFetch } from "@/lib/api-client";
import type { InsightRequest, InsightResponse } from "@/types/analytics";

export const analyticsService = {
  generateInsight: (payload: InsightRequest) =>
    apiFetch<InsightResponse>("/analytics/insights", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
};
