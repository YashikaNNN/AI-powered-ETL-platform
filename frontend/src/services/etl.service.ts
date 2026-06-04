import { apiFetch } from "@/lib/api-client";
import type { PipelineRun, PipelineRunCreate } from "@/types/etl";

export const etlService = {
  listRuns: () => apiFetch<PipelineRun[]>("/etl/runs"),
  triggerRun: (payload: PipelineRunCreate) =>
    apiFetch<PipelineRun>("/etl/runs", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
};
