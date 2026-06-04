export interface PipelineRun {
  id: number;
  pipeline_id: string;
  status: string;
  started_at: string;
  finished_at?: string | null;
  row_count?: number | null;
  error_message?: string | null;
}

export interface PipelineRunCreate {
  pipeline_id: string;
}
