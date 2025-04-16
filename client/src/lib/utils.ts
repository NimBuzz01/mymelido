import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import type { SimilarityAnalysis } from "@/lib/result";

/**
 * Combines multiple class names using clsx and tailwind-merge
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Formats a track ID by removing prefixes and converting to title case
 * @param trackId - The raw track ID (e.g., "out_summer_vibes")
 * @returns Formatted track name (e.g., "Summer Vibes")
 */
export function formatTrackName(trackId: string): string {
  return trackId
    .replace(/^out_/, "")
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

/**
 * Formats a similarity score as a percentage
 * @param similarity - Similarity score (0-1)
 * @param decimals - Number of decimal places
 * @returns Formatted percentage string
 */
export function formatSimilarity(similarity: number, decimals = 1): string {
  return `${(similarity * 100).toFixed(decimals)}%`;
}

export function enhanceContrast(
  matches: SimilarityAnalysis
): SimilarityAnalysis {
  const enhanced = matches;

  if (enhanced.matches.length === 0) return enhanced;

  enhanced.matches.sort((a, b) => b.similarity - a.similarity);

  const topScore = enhanced.matches[0].similarity;

  for (let i = 1; i < enhanced.matches.length; i++) {
    const reductionFactor = 0.7 + 0.5 * (i / enhanced.matches.length);
    const maxReduction = topScore * 0.8;

    enhanced.matches[i].similarity = Math.max(
      enhanced.matches[i].similarity * reductionFactor,
      topScore - maxReduction - Math.random() * 0.1
    );

    if (i > 0) {
      enhanced.matches[i].similarity = Math.min(
        enhanced.matches[i].similarity,
        enhanced.matches[i - 1].similarity - 0.05
      );
    }

    enhanced.matches[i].is_match =
      enhanced.matches[i].similarity > topScore * 0.7 ? true : false;
  }

  enhanced.matches.forEach((match) => {
    match.similarity = Math.max(0, match.similarity);
  });

  return enhanced;
}
