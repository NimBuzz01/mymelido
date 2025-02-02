interface SimilarityResult {
  song: string;
  overall_similarity: number;
  lyrics_similarity?: number;
  audio_similarity?: number;
  copyright_status: string;
}

interface SimilarSong {
  song: string;
  similarity: number;
}

export interface SimilarityAnalysis {
  most_potential_copyrighted_lyrics: SimilarityResult;
  most_potential_copyrighted_audio: SimilarityResult;
  top_5_similar_songs_based_on_lyrics: SimilarSong[];
  top_5_similar_songs_based_on_audio: SimilarSong[];
}
