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
  const topMatch = useMemo(() => {
    return results.matches?.[0] || null;
  }, [results.matches]);

  if (!results.matches?.length) {
    return (
      <Alert variant="default">
        <AlertCircle className="h-4 w-4" />
        <AlertTitle>All Clear</AlertTitle>
        <AlertDescription>
          No copyright issues were found for "
          {formatTrackName(results.input_metadata.filename)}". The track is
          clear.
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
            {formatTrackName(results.input_metadata.filename)}
          </span>
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
          <MatchesTable matches={results.matches} />
          <TrackInfo
            trackId={results.input_metadata.filename}
            lyrics={results.input_metadata.lyrics_snippet}
          />
        </div>
      </section>
    </div>
  );
};

export default ResultsDashboard;
