#!/usr/bin/env python3
"""
🎬 BAARLICLAW VIDEO TOOLKIT
Video-redigering og -behandling med ffmpeg
"""

import os
import sys
import subprocess
import json
import re
from typing import Optional, List, Tuple, Dict
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("VideoToolkit")

@dataclass
class VideoInfo:
    """Video metadata"""
    path: str
    duration: float
    width: int
    height: int
    fps: float
    codec: str
    bitrate: int
    audio_codec: Optional[str] = None
    audio_bitrate: Optional[int] = None

class VideoProcessor:
    """Handle video operations with ffmpeg"""
    
    def __init__(self):
        self.ffmpeg_path = self._find_ffmpeg()
        if not self.ffmpeg_path:
            logger.error("ffmpeg not found! Install with: apt-get install ffmpeg")
    
    def _find_ffmpeg(self) -> Optional[str]:
        """Find ffmpeg binary"""
        try:
            result = subprocess.run(['which', 'ffmpeg'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        # Common paths
        for path in ['/usr/bin/ffmpeg', '/usr/local/bin/ffmpeg', '/opt/ffmpeg/bin/ffmpeg']:
            if os.path.exists(path):
                return path
        return None
    
    def _run_ffmpeg(self, args: List[str], timeout: int = 300) -> Tuple[bool, str]:
        """Run ffmpeg command"""
        if not self.ffmpeg_path:
            return False, "ffmpeg not found"
        
        cmd = [self.ffmpeg_path] + args
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr
        except subprocess.TimeoutExpired:
            return False, "Timeout"
        except Exception as e:
            return False, str(e)
    
    def get_info(self, video_path: str) -> Optional[VideoInfo]:
        """Get video metadata using ffprobe"""
        ffprobe = self.ffmpeg_path.replace('ffmpeg', 'ffprobe') if self.ffmpeg_path else 'ffprobe'
        
        cmd = [
            ffprobe,
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            video_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                return None
            
            data = json.loads(result.stdout)
            
            # Find video stream
            video_stream = None
            audio_stream = None
            for stream in data.get('streams', []):
                if stream['codec_type'] == 'video' and not video_stream:
                    video_stream = stream
                elif stream['codec_type'] == 'audio' and not audio_stream:
                    audio_stream = stream
            
            if not video_stream:
                return None
            
            # Parse fps
            fps_str = video_stream.get('r_frame_rate', '0/1')
            if '/' in fps_str:
                num, den = fps_str.split('/')
                fps = float(num) / float(den) if float(den) != 0 else 0
            else:
                fps = float(fps_str)
            
            return VideoInfo(
                path=video_path,
                duration=float(data.get('format', {}).get('duration', 0)),
                width=video_stream.get('width', 0),
                height=video_stream.get('height', 0),
                fps=fps,
                codec=video_stream.get('codec_name', 'unknown'),
                bitrate=int(video_stream.get('bit_rate', 0)),
                audio_codec=audio_stream.get('codec_name') if audio_stream else None,
                audio_bitrate=int(audio_stream.get('bit_rate', 0)) if audio_stream else None
            )
            
        except Exception as e:
            logger.error(f"Failed to get video info: {e}")
            return None
    
    def trim(self, input_path: str, output_path: str, 
             start: float, duration: float) -> bool:
        """
        Trim video segment
        
        Args:
            input_path: Source video
            output_path: Output video
            start: Start time in seconds
            duration: Duration in seconds
        """
        args = [
            '-i', input_path,
            '-ss', str(start),
            '-t', str(duration),
            '-c', 'copy',  # Copy without re-encoding (fast)
            '-y',  # Overwrite output
            output_path
        ]
        
        success, error = self._run_ffmpeg(args)
        if success:
            logger.info(f"Trimmed: {output_path}")
            return True
        else:
            logger.error(f"Trim failed: {error}")
            return False
    
    def resize(self, input_path: str, output_path: str,
               width: Optional[int] = None, height: Optional[int] = None,
               maintain_aspect: bool = True) -> bool:
        """
        Resize video
        
        Args:
            input_path: Source video
            output_path: Output video
            width: New width (optional)
            height: New height (optional)
            maintain_aspect: Keep aspect ratio
        """
        if maintain_aspect and (width or height):
            if width and height:
                scale = f"{width}:{height}"
            elif width:
                scale = f"{width}:-2"  # -2 ensures even number
            else:
                scale = f"-2:{height}"
        else:
            scale = f"{width or -1}:{height or -1}"
        
        args = [
            '-i', input_path,
            '-vf', f'scale={scale}',
            '-c:a', 'copy',
            '-y',
            output_path
        ]
        
        success, error = self._run_ffmpeg(args)
        if success:
            logger.info(f"Resized: {output_path}")
            return True
        else:
            logger.error(f"Resize failed: {error}")
            return False
    
    def extract_audio(self, input_path: str, output_path: str,
                      format: str = 'mp3', bitrate: str = '192k') -> bool:
        """Extract audio from video"""
        args = [
            '-i', input_path,
            '-vn',  # No video
            '-c:a', 'libmp3lame' if format == 'mp3' else 'aac',
            '-b:a', bitrate,
            '-y',
            output_path
        ]
        
        success, error = self._run_ffmpeg(args)
        if success:
            logger.info(f"Audio extracted: {output_path}")
            return True
        else:
            logger.error(f"Audio extraction failed: {error}")
            return False
    
    def create_thumbnail(self, input_path: str, output_path: str,
                        time: float = 0) -> bool:
        """Extract thumbnail at specific time"""
        args = [
            '-i', input_path,
            '-ss', str(time),
            '-vframes', '1',
            '-q:v', '2',
            '-y',
            output_path
        ]
        
        success, error = self._run_ffmpeg(args)
        if success:
            logger.info(f"Thumbnail created: {output_path}")
            return True
        else:
            logger.error(f"Thumbnail failed: {error}")
            return False
    
    def concatenate(self, input_paths: List[str], output_path: str) -> bool:
        """Concatenate multiple videos"""
        # Create concat file
        concat_file = '/tmp/concat_list.txt'
        with open(concat_file, 'w') as f:
            for path in input_paths:
                f.write(f"file '{path}'\n")
        
        args = [
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_file,
            '-c', 'copy',
            '-y',
            output_path
        ]
        
        success, error = self._run_ffmpeg(args)
        
        # Cleanup
        try:
            os.remove(concat_file)
        except:
            pass
        
        if success:
            logger.info(f"Concatenated: {output_path}")
            return True
        else:
            logger.error(f"Concatenation failed: {error}")
            return False
    
    def add_text_overlay(self, input_path: str, output_path: str,
                        text: str, x: int = 10, y: int = 10,
                        font_size: int = 24, color: str = 'white') -> bool:
        """Add text overlay to video"""
        # Escape special characters
        escaped_text = text.replace("'", "\\'").replace(":", "\\:")
        
        drawtext = f"drawtext=text='{escaped_text}':x={x}:y={y}:fontsize={font_size}:fontcolor={color}"
        
        args = [
            '-i', input_path,
            '-vf', drawtext,
            '-c:a', 'copy',
            '-y',
            output_path
        ]
        
        success, error = self._run_ffmpeg(args)
        if success:
            logger.info(f"Text overlay added: {output_path}")
            return True
        else:
            logger.error(f"Text overlay failed: {error}")
            return False
    
    def create_short(self, input_path: str, output_path: str,
                    start: float, duration: float = 60,
                    target_resolution: Tuple[int, int] = (1080, 1920)) -> bool:
        """
        Create vertical short (TikTok/Reels/Shorts format)
        
        Args:
            input_path: Source video
            output_path: Output video
            start: Start time
            duration: Clip duration (default 60s)
            target_resolution: Output resolution (default 1080x1920 vertical)
        """
        width, height = target_resolution
        
        # Crop to vertical 9:16, then resize
        filter_complex = (
            f"crop=ih*9/16:ih,scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2"
        )
        
        args = [
            '-i', input_path,
            '-ss', str(start),
            '-t', str(duration),
            '-vf', filter_complex,
            '-c:a', 'aac',
            '-b:a', '128k',
            '-y',
            output_path
        ]
        
        success, error = self._run_ffmpeg(args)
        if success:
            logger.info(f"Short created: {output_path}")
            return True
        else:
            logger.error(f"Short creation failed: {error}")
            return False
    
    def compress(self, input_path: str, output_path: str,
                target_size_mb: Optional[float] = None,
                crf: int = 23) -> bool:
        """
        Compress video
        
        Args:
            input_path: Source video
            output_path: Output video
            target_size_mb: Target size in MB (optional)
            crf: Constant Rate Factor (lower = better quality, 18-28 range)
        """
        if target_size_mb:
            # Calculate bitrate for target size
            info = self.get_info(input_path)
            if info:
                target_bitrate = int((target_size_mb * 8 * 1024 * 1024) / info.duration)
                video_bitrate = int(target_bitrate * 0.9)  # 90% for video
                audio_bitrate = int(target_bitrate * 0.1)  # 10% for audio
                
                args = [
                    '-i', input_path,
                    '-b:v', str(video_bitrate),
                    '-b:a', str(audio_bitrate),
                    '-y',
                    output_path
                ]
            else:
                args = ['-i', input_path, '-crf', str(crf), '-y', output_path]
        else:
            args = [
                '-i', input_path,
                '-crf', str(crf),
                '-preset', 'medium',
                '-y',
                output_path
            ]
        
        success, error = self._run_ffmpeg(args)
        if success:
            logger.info(f"Compressed: {output_path}")
            return True
        else:
            logger.error(f"Compression failed: {error}")
            return False

# === CONVENIENCE FUNCTIONS ===
def quick_trim(input_path: str, output_path: str, start: float, duration: float) -> bool:
    """Quick video trim"""
    processor = VideoProcessor()
    return processor.trim(input_path, output_path, start, duration)

def quick_resize(input_path: str, output_path: str, width: int, height: int) -> bool:
    """Quick video resize"""
    processor = VideoProcessor()
    return processor.resize(input_path, output_path, width, height)

def extract_thumbnail(input_path: str, output_path: str, time: float = 0) -> bool:
    """Quick thumbnail extraction"""
    processor = VideoProcessor()
    return processor.create_thumbnail(input_path, output_path, time)

def create_vertical_short(input_path: str, output_path: str, start: float) -> bool:
    """Quick vertical short creation"""
    processor = VideoProcessor()
    return processor.create_short(input_path, output_path, start)

# === TESTING ===
if __name__ == "__main__":
    print("🎬 BaarliClaw Video Toolkit - Testing")
    print("=" * 50)
    
    processor = VideoProcessor()
    
    if not processor.ffmpeg_path:
        print("❌ ffmpeg not found - install with: apt-get install ffmpeg")
        sys.exit(1)
    
    print(f"✅ ffmpeg found: {processor.ffmpeg_path}")
    
    # Test with sample video if available
    test_videos = [
        "/tmp/test_video.mp4",
        "/root/.openclaw/workspace/assets/test.mp4"
    ]
    
    found_video = None
    for v in test_videos:
        if os.path.exists(v):
            found_video = v
            break
    
    if found_video:
        print(f"\n🧪 Testing with: {found_video}")
        
        # Test info extraction
        info = processor.get_info(found_video)
        if info:
            print(f"✅ Video info:")
            print(f"   Duration: {info.duration:.2f}s")
            print(f"   Resolution: {info.width}x{info.height}")
            print(f"   FPS: {info.fps:.2f}")
            print(f"   Codec: {info.codec}")
    else:
        print("\nℹ️ No test video found")
        print("   Install ffmpeg to use video features:")
        print("   apt-get update && apt-get install -y ffmpeg")
    
    print("\n✅ Video Toolkit ready!")
