import { Check, X } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import type { MatchResult } from "@/lib/result";
import { formatTrackName } from "@/lib/utils";

interface MatchCardProps {
  match: MatchResult;
  isTopMatch?: boolean;
}

export function MatchCard({ match, isTopMatch = false }: MatchCardProps) {
  const isHighConfidence = match.similarity > 0.85;
  const confidenceLabel = isHighConfidence
    ? "High Confidence"
    : "Potential Match";

  return (
    <Card
      className={
        isTopMatch
          ? "border-primary/20 transition-all hover:shadow-md"
          : "transition-all hover:shadow-sm"
      }
    >
      <CardContent className="p-5">
        <div className="flex flex-col gap-4">
          <div className="flex items-start justify-between">
            <div>
              <h3 className="text-lg font-medium">
                {formatTrackName(match.track_id)}
              </h3>
              <p className="text-sm text-muted-foreground">
                {match.is_match ? "Confirmed match" : "Potential match"}
              </p>
            </div>
            <Badge
              variant={isHighConfidence ? "destructive" : "outline"}
              className="gap-1 transition-colors"
            >
              {isHighConfidence ? (
                <Check className="h-3 w-3" />
              ) : (
                <X className="h-3 w-3" />
              )}
              {confidenceLabel}
            </Badge>
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">Similarity Score</span>
              <span className="font-mono text-sm font-semibold">
                {(match.similarity * 100).toFixed(1)}%
              </span>
            </div>
            <Progress
              value={match.similarity * 100}
              className="h-2 transition-all"
              aria-label={`Similarity score: ${(match.similarity * 100).toFixed(
                1
              )}%`}
            />
          </div>

          {match.lyrics_snippet && (
            <div className="rounded-lg border bg-card/50 p-4">
              <h4 className="mb-2 text-sm font-medium">Matching Lyrics</h4>
              <p className="text-sm italic text-muted-foreground">
                "{match.lyrics_snippet}"
              </p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
