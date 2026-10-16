# WebM and WebVTT scan fixture

`webm_vp9_opus.webm` is a synthetic five-second WebM sample with VP9 video
and Opus audio. It contains no third-party media.

The fixture can be regenerated with FFmpeg and the `libvpx-vp9` and `libopus`
encoders:

```sh
ffmpeg -hide_banner -loglevel error \
  -f lavfi -i 'color=c=black:s=64x64:r=10:d=5' \
  -f lavfi -i 'sine=frequency=1000:sample_rate=48000:duration=5' \
  -map 0:v:0 -map 1:a:0 \
  -c:v libvpx-vp9 -deadline realtime -cpu-used 8 -threads 1 -pix_fmt yuv420p \
  -c:a libopus -ac 2 -b:a 64k -application audio \
  -y webm_vp9_opus.webm
```

The scanner test copies `webm_vp9_opus.en.vtt` after the first scan to verify
that an incremental scan discovers the new sidecar for an unchanged WebM file.
