import { Check, X } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { MatchResult } from "@/lib/result";
import { formatTrackName } from "@/lib/utils";

interface MatchesTableProps {
  matches: MatchResult[];
}

export function MatchesTable({ matches }: MatchesTableProps) {
  return (
    <Card className="h-full transition-all hover:shadow-sm">
      <CardHeader className="pb-2">
        <CardTitle>Similar Tracks</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="max-h-[350px] overflow-auto rounded-md border">
          <Table>
            <TableHeader className="sticky top-0 bg-card">
              <TableRow>
                <TableHead>Track</TableHead>
                <TableHead className="text-right">Similarity</TableHead>
                <TableHead className="text-right">Match</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {matches.map((match) => (
                <TableRow
                  key={match.track_id}
                  className="transition-colors hover:bg-muted/50"
                >
                  <TableCell className="font-medium">
                    {formatTrackName(match.track_id)}
                  </TableCell>
                  <TableCell className="text-right">
                    <span className="font-mono">
                      {(match.similarity * 100).toFixed(1)}%
                    </span>
                  </TableCell>
                  <TableCell className="text-right">
                    {match.match === "YES" ? (
                      <Badge variant="destructive" className="gap-1">
                        <Check className="h-3 w-3" /> Yes
                      </Badge>
                    ) : (
                      <Badge variant="secondary" className="gap-1">
                        <X className="h-3 w-3" /> No
                      </Badge>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  );
}
