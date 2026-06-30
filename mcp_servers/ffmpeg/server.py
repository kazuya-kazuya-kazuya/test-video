from mcp.server import Server
from mcp.server.stdio import stdio_server
import asyncio
import subprocess


app = Server("ffmpeg-mcp")


@app.tool()
async def probe_media(path: str) -> str:
    """ffprobeでメディア情報をJSON形式で取得します。"""
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            path,
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


@app.tool()
async def convert_to_mp4(input_path: str, output_path: str) -> str:
    """入力動画をH.264/AACのMP4に変換します。"""
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-movflags",
            "+faststart",
            output_path,
        ],
        check=True,
    )
    return output_path


if __name__ == "__main__":
    asyncio.run(stdio_server(app))
