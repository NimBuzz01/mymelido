import React from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "./ui/card";
import {
  ChartContainer,
  ChartLegend,
  ChartLegendContent,
  ChartTooltip,
  ChartTooltipContent,
} from "./ui/chart";
import { Bar, BarChart, XAxis, YAxis } from "recharts";
import { type ChartConfig } from "@/components/ui/chart";
import { SimilarityAnalysis } from "@/lib/result";

const chartConfig = {
  similarity: {
    label: "Similarity",
    color: "#8884d8",
  },
} satisfies ChartConfig;

const ResultsSection = ({ results }: { results: SimilarityAnalysis }) => {
  return (
    <>
      <h2 className="text-xl font-semibold mb-4">
        Similarity Analysis Results
      </h2>
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2 mb-4">
        <Card>
          <CardHeader>
            <CardTitle>Most Potential Copyrighted Lyrics</CardTitle>
            <CardDescription>
              Analysis results for lyrical similarity
            </CardDescription>
            <CardContent className="p-0">
              <p className="text-lg font-semibold">
                {results.most_potential_copyrighted_lyrics.song}
              </p>
              <p>
                Overall Similarity:{" "}
                {results.most_potential_copyrighted_lyrics.overall_similarity}%
              </p>
              <p>
                Lyrics Similarity:{" "}
                {results.most_potential_copyrighted_lyrics.lyrics_similarity}%
              </p>
              <p>
                Copyright Status:
                <strong>
                  {results.most_potential_copyrighted_lyrics.copyright_status}
                </strong>
              </p>
            </CardContent>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Most Potential Copyrighted Audio</CardTitle>
            <CardDescription>
              Analysis results for audio similarity
            </CardDescription>
            <CardContent className="p-0">
              <p className="text-lg font-semibold">
                {results.most_potential_copyrighted_audio.song}
              </p>
              <p>
                Overall Similarity:{" "}
                {results.most_potential_copyrighted_audio.overall_similarity}%
              </p>
              <p>
                Audio Similarity:{" "}
                {results.most_potential_copyrighted_audio.audio_similarity}%
              </p>
              <p>
                Copyright Status:
                <strong>
                  {results.most_potential_copyrighted_audio.copyright_status}
                </strong>
              </p>
            </CardContent>
          </CardHeader>
        </Card>
      </div>
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Top 5 Similar Songs Based on Lyrics</CardTitle>
            <CardContent className="p-0">
              <ChartContainer
                className="w-full min-h-[300px]"
                config={chartConfig}
              >
                <BarChart
                  accessibilityLayer
                  data={results.top_5_similar_songs_based_on_lyrics}
                  layout="vertical"
                  margin={{
                    left: 0,
                  }}
                >
                  <YAxis
                    dataKey="song"
                    type="category"
                    tickLine={false}
                    tickMargin={10}
                    axisLine={false}
                  />
                  <XAxis dataKey="similarity" type="number" />
                  <ChartTooltip
                    cursor={false}
                    content={<ChartTooltipContent hideLabel />}
                  />
                  <Bar
                    dataKey="similarity"
                    layout="vertical"
                    radius={5}
                    fill="var(--color-similarity)"
                  />
                  <ChartLegend content={<ChartLegendContent />} />
                </BarChart>
              </ChartContainer>
            </CardContent>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Top 5 Similar Songs Based on Audio</CardTitle>
            <CardContent className="p-0">
              <ChartContainer
                className="w-full min-h-[300px]"
                config={chartConfig}
              >
                <BarChart
                  accessibilityLayer
                  data={results.top_5_similar_songs_based_on_audio}
                  layout="vertical"
                  margin={{
                    left: 0,
                  }}
                >
                  <YAxis
                    dataKey="song"
                    type="category"
                    tickLine={false}
                    tickMargin={10}
                    axisLine={false}
                  />
                  <XAxis dataKey="similarity" type="number" />
                  <ChartTooltip
                    cursor={false}
                    content={<ChartTooltipContent hideLabel />}
                  />
                  <Bar
                    dataKey="similarity"
                    layout="vertical"
                    radius={5}
                    fill="var(--color-similarity)"
                  />
                  <ChartLegend content={<ChartLegendContent />} />
                </BarChart>
              </ChartContainer>
            </CardContent>
          </CardHeader>
        </Card>
      </div>
    </>
  );
};

export default ResultsSection;
