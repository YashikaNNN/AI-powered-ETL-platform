export interface InsightRequest {
  query?: string;
  dataset_id?: string | null;
}

export interface InsightResponse {
  summary: string;
  model: string;
}

export interface SampleEvent {
  id: number;
  event_id: string;
  user_id: string;
  event_type: string;
  event_timestamp: string;
  amount: string;
  loaded_at: string;
}

export interface PaginatedEventsResponse {
  items: SampleEvent[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface EventTypeCount {
  event_type: string;
  count: number;
}

export interface AnalyticsSummary {
  total_events: number;
  total_revenue: string;
  by_event_type: EventTypeCount[];
}
