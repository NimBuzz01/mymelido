export interface MatchResult {
  track_id: string;
  similarity: number;
  is_match: boolean;
  lyrics_snippet: string;
  is_match: boolean;
  lyrics_snippet: string;
}

export interface SimilarityAnalysis {
  input_metadata: { filename: string; lyrics_snippet: string };
  status: string;
  matches: MatchResult[];
}
