#!/usr/bin/env python
# Plays MPV when instructed to by a chrome extension =]
import argparse
import sys
import urllib.parse as urlparse
from http import server
from subprocess import Popen

import psutil


class Handler(server.BaseHTTPRequestHandler):
    def respond(self, code, body=None):
        self.send_response(code)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        if body:
            self.wfile.write(bytes(body+"\n", "utf-8"))

    def do_GET(self):  # noqa: N802, PLR0915, PLR0912
        if is_running():
            print("MPV seems to already be running.")
            self.respond(400)
            return

        try:
            url = urlparse.urlparse(self.path)
            query = urlparse.parse_qs(url.query)
        except Exception:
            query = {}

        if query.get("mpv_args"):
            print("MPV ARGS:", query.get("mpv_args"))

        if "play_url" in query:
            urls = str(query["play_url"][0])

            if urls.startswith("magnet:") or urls.endswith(".torrent"):
                try:
                    pipe = Popen(["peerflix", "-k", urls, "--",
                                  "--force-window", *query.get("mpv_args", [])])
                except FileNotFoundError:
                    missing_bin("peerflix")
            elif urls.startswith(("http:", "https:")):
                try:
                    pipe = Popen(["mpv", urls, "--force-window",
                                  *query.get("mpv_args", [])])
                except FileNotFoundError:
                    missing_bin("mpv")
            else:
                self.respond(400)
                return
            self.respond(200, "playing...")

        elif "cast_url" in query:
            urls = str(query["cast_url"][0])
            if urls.startswith("magnet:") or urls.endswith(".torrent"):
                print(" === WARNING: Casting torrents not yet fully supported!")
                try:
                    with Popen(["mkchromecast", "--video",
                                "--source-url", "http://localhost:8888"]):
                        pass
                except FileNotFoundError:
                    missing_bin("mkchromecast")
                pipe.terminate()
            elif urls.startswith(("http:", "https:")):
                try:
                    pipe = Popen(["mkchromecast", "--video", "-y", urls])
                except FileNotFoundError:
                    missing_bin("mkchromecast")
            else:
                self.respond(400)
            self.respond(200, "casting...")

        elif "fairuse_url" in query:
            urls = str(query["fairuse_url"][0])
            location = query.get("location", ["~/Downloads/"])[0]

            if "%" not in location:
                location += "%(title)s.%(ext)s"

            print("downloading ", urls, "to", location)

            if urls.startswith("magnet:") or urls.endswith(".torrent"):
                msg = " === ERROR: Downloading torrents not yet supported!"
                print(msg)
                self.respond(400, msg)
            elif urls.startswith(("http:", "https:")):
                try:
                    pipe = Popen(["yt-dlp", urls, "-o", location,
                                  *query.get("ytdl_args", [])])
                except FileNotFoundError:
                    missing_bin("yt-dlp")

                self.respond(200, "downloading...")
            else:
                self.respond(400)

        else:
            self.respond(400)


def missing_bin(bin):
    print("======================")
    print(f"ERROR: {bin.upper()} does not appear to be installed correctly! " +
          'Please ensure you can launch "{bin}" in the terminal.')
    print("======================")


def is_running():
    # Check with .exe on Windows
    if sys.platform.startswith("win"):
        return any(p.name() == "mpv.exe" for p in psutil.process_iter())

    return any(p.name() == "mpv" for p in psutil.process_iter())


def start():
    parser = argparse.ArgumentParser(
        description="Plays MPV when instructed to by a browser extension.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--port",   type=int,  default=7531,
                        help="The port to listen on.")
    parser.add_argument("--public", action="store_true",
                        help="Accept traffic from other computers.")
    args = parser.parse_args()
    hostname = "0.0.0.0" if args.public else "localhost"
    httpd = server.HTTPServer((hostname, args.port), Handler)
    print("Serving on {}:{}".format(hostname, args.port))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down...")
        httpd.shutdown()


if __name__ == "__main__":
    start()

