# Video bit-depth regression fixtures (#195)

These synthetic, one-frame, 64 × 64 black videos contain no third-party media.
They are checked in so scan tests need only ffprobe, without requiring encoders.
The tests use disposable libraries and databases and cover both full scans and
new-file discovery during incremental scans, persisted metadata, file details,
and bit-depth statistics.

| File | Codec | Pixel format | Expected depth | HDR classification |
| --- | --- | --- | --- | --- |
| `h264_sdr_8bit.mkv` | H.264 | `yuv420p` | 8 | unchanged (`null`, shown as SDR) |
| `hevc_hdr10_10bit.mkv` | HEVC Main 10 | `yuv420p10le` | 10 | HDR10 |
| `vp9_sdr_10bit.mkv` | VP9 Profile 2 | `yuv420p10le` | 10 | unchanged (`null`, shown as SDR) |

With FFmpeg/ffprobe 8.0, the HEVC and VP9 streams omit both
`bits_per_raw_sample` and `bits_per_sample`, reproducing the reported bug.
H.264 supplies `bits_per_raw_sample=8` and protects existing explicit metadata.
The parser unit tests also cover the missing-field case independently of the
installed ffprobe version, explicit-value precedence, invalid values, unknown
formats, and unchanged audio behavior. The optional descriptor test compares
inferred depths with ffprobe's per-component depths, rather than bits per pixel.

Recreate from this directory with FFmpeg (libx264, libx265, and libvpx-vp9):

```sh
ffmpeg -hide_banner -loglevel error -y -f lavfi \
  -i 'color=c=black:s=64x64:r=1,format=yuv420p' -frames:v 1 \
  -c:v libx264 -preset ultrafast h264_sdr_8bit.mkv

ffmpeg -hide_banner -loglevel error -y -f lavfi \
  -i 'color=c=black:s=64x64:r=1,format=yuv420p10le' -frames:v 1 \
  -c:v libx265 -preset ultrafast \
  -x265-params 'log-level=error:pools=none:frame-threads=1:wpp=0:colorprim=9:transfer=16:colormatrix=9:hdr10=1:master-display=G(13250,34500)B(7500,3000)R(34000,16000)WP(15635,16450)L(10000000,1):max-cll=1000,400' \
  hevc_hdr10_10bit.mkv

ffmpeg -hide_banner -loglevel error -y -f lavfi \
  -i 'color=c=black:s=64x64:r=1,format=yuv420p10le' -frames:v 1 \
  -c:v libvpx-vp9 -deadline realtime -cpu-used 8 vp9_sdr_10bit.mkv
```
