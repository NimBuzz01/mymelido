import { Music2 } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatTrackName } from "@/lib/utils";

interface TrackInfoProps {
  trackId: string;
  genre: string;
  lyrics?: string;
}

export function TrackInfo({ trackId, genre, lyrics }: TrackInfoProps) {
  return (
    <Card className="h-full transition-all hover:shadow-sm">
      <CardHeader className="pb-2">
        <CardTitle className="flex items-center gap-2">
          <Music2 className="h-5 w-5 text-primary" />
          Original Track
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <h3 className="text-lg font-medium">{formatTrackName(trackId)}</h3>
          <Badge variant="outline" className="mt-2 capitalize">
            {genre}
          </Badge>
        </div>

        {lyrics && (
          <div className="rounded-lg border bg-card/50 p-4">
            <h4 className="mb-2 text-sm font-medium">Sample Lyrics</h4>
            <p className="text-sm italic text-muted-foreground">"{lyrics}"</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
