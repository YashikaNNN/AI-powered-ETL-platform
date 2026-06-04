export interface InsightRequest {
  query: string;
  dataset_id?: string | null;
}

export interface InsightResponse {
  summary: string;
  model: string;
}
