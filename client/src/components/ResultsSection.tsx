"use client";

import React, { useMemo } from "react";
import { AlertCircle, Music } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import type { SimilarityAnalysis } from "@/lib/result";
import { formatTrackName } from "@/lib/utils";
import { MatchCard } from "./MatchCard";
import { MatchesTable } from "./MatchesTable";
import { TrackInfo } from "./TrackInfo";

interface ResultsDashboardProps {
  results: SimilarityAnalysis;
}

const ResultsDashboard = ({ results }: ResultsDashboardProps) => {
  // Memoize the top match to prevent unnecessary recalculations
  const topMatch = useMemo(() => {
    return results.top_matches?.[0] || null;
  }, [results.top_matches]);

  // Handle the case where there are no matches
  if (!results.top_matches?.length) {
    return (
      <Alert variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertTitle>No matches found</AlertTitle>
        <AlertDescription>
          No similar tracks were found for "
          {formatTrackName(results.query_track)}". Try analyzing with different
          parameters.
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      {/* Header Section */}
      <div className="space-y-2">
        <div className="flex items-center gap-2">
          <Music className="h-6 w-6 text-primary" />
          <h1 className="text-3xl font-bold tracking-tight">Track Analysis</h1>
        </div>
        <div className="flex items-center gap-4 text-sm text-muted-foreground">
          <span className="font-medium">
            {formatTrackName(results.query_track)}
          </span>
          <span>•</span>
          <span className="capitalize">{results.genre}</span>
        </div>
      </div>

      {/* Top Match Highlight */}
      {topMatch && (
        <section aria-labelledby="top-match-heading">
          <h2 id="top-match-heading" className="mb-4 text-xl font-semibold">
            Best Match
          </h2>
          <MatchCard match={topMatch} isTopMatch={true} />
        </section>
      )}

      {/* Similarity Breakdown */}
      <section aria-labelledby="breakdown-heading">
        <h2 id="breakdown-heading" className="mb-4 text-xl font-semibold">
          Analysis Details
        </h2>
        <div className="grid gap-6 md:grid-cols-2">
          <MatchesTable matches={results.top_matches} />
          <TrackInfo
            trackId={results.query_track}
            genre={results.genre}
            lyrics={results.lyrics}
          />
        </div>
      </section>
    </div>
  );
};

export default React.memo(ResultsDashboard);
