export interface MatchResult {
  track_id: string;
  similarity: number;
  is_match: boolean;
  lyrics_snippet: string;
}

export interface SimilarityAnalysis {
  status: string;
  results: MatchResult[];
}
