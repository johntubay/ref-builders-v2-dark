#!/usr/bin/env bash
# Usage: ./make-hero-video.sh DJI_20261117112411_0164_D.MP4 [start_seconds] [length_seconds]
# Makes a muted, looping-friendly 1280px hero video (~1-2 MB) + poster for the homepage.
set -e
IN="$1"; SS="${2:-1}"; LEN="${3:-14}"; OUT="$(dirname "$0")/../site/assets/video"
ffmpeg -y -ss "$SS" -t "$LEN" -i "$IN" -an \
  -vf "scale=1280:-2:flags=lanczos,fps=25,fade=t=in:st=0:d=0.8,fade=t=out:st=$(echo "$LEN-0.8"|bc):d=0.8,format=yuv420p" \
  -c:v libx264 -preset veryslow -crf 30 -profile:v high -movflags +faststart "$OUT/ref-hero.mp4"
ffmpeg -y -ss 0.9 -i "$OUT/ref-hero.mp4" -vframes 1 -q:v 4 "$OUT/../img/hero-poster.jpg"
ls -lh "$OUT/ref-hero.mp4"
