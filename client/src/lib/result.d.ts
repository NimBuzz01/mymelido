export interface MatchResult {
  track_id: string;
  similarity: number;
  match: "YES" | "NO";
  lyrics: string;
}

export interface SimilarityAnalysis {
  query_track: string;
  genre: string;
  top_matches: MatchResult[];
  lyrics?: string;
}
